#!/usr/bin/env python3
"""
CLI script to run Google Deep Research tasks.
"""

import sys
import argparse
import time
import re
from pathlib import Path
from google_research_client import GoogleResearchClient

def sanitize_filename(text: str) -> str:
    """Create a safe filename from a string."""
    # Remove non-alphanumeric characters and replace spaces with underscores
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text).strip()
    return text[:50]  # Limit length

def loading_spinner():
    """Generator for a simple loading spinner."""
    while True:
        for char in "|/-\\":
            yield char

def main():
    parser = argparse.ArgumentParser(description="Run Google Deep Research task")
    parser.add_argument("--topic", "-t", required=True, type=str, help="Research topic or question")
    parser.add_argument("--output-dir", "-o", default="outputs/research", help="Directory for results")
    parser.add_argument("--timeout", type=int, default=1200, help="Timeout in seconds (default: 20 mins)")
    parser.add_argument("--interval", type=int, default=10, help="Polling interval in seconds")
    
    args = parser.parse_args()
    
    try:
        client = GoogleResearchClient()
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        sys.exit(1)
        
    print(f"\n🚀 Starting Deep Research on: '{args.topic}'")
    print(f"   Timeout: {args.timeout}s")
    
    try:
        interaction_id = client.start_research(args.topic)
        print(f"   Task ID: {interaction_id}")
        print("\n⏳ Researching in background (this may take several minutes)...")
        
        # Progress indication
        spinner = loading_spinner()
        
        def progress_callback(status, elapsed):
            # Clear line and show status
            sys.stdout.write(f"\r   Status: {status} [{elapsed}s] {next(spinner)}")
            sys.stdout.flush()
            
        try:
            result_data = client.poll_results(
                interaction_id,
                max_wait_time=args.timeout,
                poll_interval=args.interval,
                status_callback=progress_callback
            )
            
            print("\n\n✅ Research Complete!")
            
            # Save results
            prefix = sanitize_filename(args.topic)
            files = client.save_result(result_data, args.output_dir, prefix)
            
            print(f"\n📄 Report saved to:")
            print(f"   - {files['markdown']}")
            print(f"   - {files['json']}")
            
            # Show preview
            print("\n" + "="*60)
            preview = result_data['result'][:500] + "..." if len(result_data['result']) > 500 else result_data['result']
            print(preview)
            print("="*60 + "\n")
            
        except TimeoutError as e:
            print(f"\n\n⚠️  Timeout: {e}")
            print(f"   Task {interaction_id} may still be running in the background.")
            
        except RuntimeError as e:
            print(f"\n\n❌ Failed: {e}")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Aborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
