#!/usr/bin/env python3
"""Command-line tool for fetching AlphaFold structures.

Usage:
    # Fetch single protein
    python tools/fetch_afdb.py --uniprot-id P02458

    # Fetch from list
    python tools/fetch_afdb.py --protein-list data/protein_lists/priority_20.txt

    # Show cache info
    python tools/fetch_afdb.py --cache-info
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from spinalmodes.afdb import AFDBCache, AFDBClient


def setup_logging(verbose: bool = False) -> None:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s", stream=sys.stderr)


def read_protein_list(file_path: Path) -> List[str]:
    """Read UniProt IDs from file (one per line, skip comments).

    Args:
        file_path: Path to text file with UniProt IDs

    Returns:
        List of UniProt accessions
    """
    uniprot_ids = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            uniprot_ids.append(line)
    return uniprot_ids


def fetch_proteins(
    uniprot_ids: List[str],
    cache: AFDBCache,
    client: AFDBClient,
    force_refetch: bool = False,
) -> None:
    """Fetch metadata for list of proteins.

    Args:
        uniprot_ids: List of UniProt accessions
        cache: AFDB cache instance
        client: AFDB client instance
        force_refetch: If True, refetch even if cached
    """
    print(f"Fetching {len(uniprot_ids)} proteins from AFDB...")
    print("=" * 60)

    success_count = 0
    cache_hit_count = 0
    error_count = 0

    for i, uniprot_id in enumerate(uniprot_ids, 1):
        print(f"[{i}/{len(uniprot_ids)}] {uniprot_id}...", end=" ")

        # Check cache first
        if not force_refetch and cache.is_cached(uniprot_id):
            print("✓ (cached)")
            cache_hit_count += 1
            continue

        # Fetch from API
        try:
            metadata = client.get_prediction(uniprot_id)
            if metadata:
                cache.store_metadata(uniprot_id, metadata)
                gene = metadata.get("gene", "UNKNOWN")
                version = metadata.get("model_version", "?")
                print(f"✓ {gene} (v{version})")
                success_count += 1
            else:
                print("✗ Not found in AFDB")
                error_count += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            error_count += 1

    print("\n" + "=" * 60)
    print(f"Results:")
    print(f"  Newly fetched: {success_count}")
    print(f"  Cache hits:    {cache_hit_count}")
    print(f"  Errors:        {error_count}")
    print(f"  Total:         {len(uniprot_ids)}")


def show_cache_info(cache: AFDBCache) -> None:
    """Display cache statistics.

    Args:
        cache: AFDB cache instance
    """
    info = cache.get_cache_info()

    print("Cache Information")
    print("=" * 60)
    print(f"Cache directory:  {info['cache_dir']}")
    print(f"Total proteins:   {info['n_proteins']}")
    print(f"With structures:  {info['n_with_structures']}")
    print(f"Total size:       {info['total_size_mb']:.2f} MB")
    if info["oldest_entry"]:
        print(f"Oldest entry:     {info['oldest_entry']}")
    if info["newest_entry"]:
        print(f"Newest entry:     {info['newest_entry']}")

    if info["n_proteins"] > 0:
        print(f"\nCache index: {cache.index_file}")
        print(f"  Use pandas to explore: pd.read_csv('{cache.index_file}')")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch AlphaFold structures from AFDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--uniprot-id", help="Single UniProt accession to fetch")
    input_group.add_argument(
        "--protein-list",
        type=Path,
        help="File with UniProt IDs (one per line)",
    )
    input_group.add_argument(
        "--cache-info",
        action="store_true",
        help="Show cache statistics and exit",
    )

    # Cache options
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="Cache directory (default: ~/.spinalmodes_cache/afdb)",
    )
    parser.add_argument(
        "--force-refetch",
        action="store_true",
        help="Refetch even if already cached",
    )

    # Logging
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    setup_logging(args.verbose)

    # Initialize cache
    cache = AFDBCache(cache_dir=args.cache_dir)

    # Handle cache-info command
    if args.cache_info:
        show_cache_info(cache)
        return 0

    # Require input
    if not args.uniprot_id and not args.protein_list:
        parser.error("Must provide --uniprot-id or --protein-list (or --cache-info)")

    # Initialize client
    client = AFDBClient()

    # Test connection
    if not client.test_connection():
        print("ERROR: Cannot connect to AFDB API", file=sys.stderr)
        return 1

    # Collect UniProt IDs
    if args.uniprot_id:
        uniprot_ids = [args.uniprot_id]
    else:
        if not args.protein_list.exists():
            print(f"ERROR: File not found: {args.protein_list}", file=sys.stderr)
            return 1
        uniprot_ids = read_protein_list(args.protein_list)

    # Fetch proteins
    fetch_proteins(uniprot_ids, cache, client, args.force_refetch)

    return 0


if __name__ == "__main__":
    sys.exit(main())
