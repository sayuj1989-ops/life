"""Reproduce the reduced-model controls; --live adds one public AFDB download."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from spinalmodes.recovery_two_state import simulate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    output = Path(__file__).resolve().parent
    times = np.linspace(0, 20, 201)
    impulse = simulate(times, kr=0.7, kg=0.3, initial=(0.02, 0))
    exact = 0.006 * (1 - np.exp(-times))
    zero = simulate(times, kr=0.7, kg=0.3)
    no_growth = simulate(times, kr=0.7, kg=0, forcing=0.02)
    correction = simulate(times, kr=0.7, kg=0, kh=0.2, initial=(0, 0.02))
    positive = simulate(times, kr=0.7, kg=0.3, forcing=0.02, kh=0.1)
    negative = simulate(times, kr=0.7, kg=0.3, forcing=-0.02, kh=0.1)
    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Equation and implementation verification; no patient validation',
        'units': {'time': 'years', 'curvature': '1/m', 'forcing': '1/m/year', 'rates': '1/year'},
        'assumed_rates': {'kr': 0.7, 'kg': 0.3, 'kh_correction': 0.2},
        'impulse_remodeled_max_abs_error': float(np.max(np.abs(impulse['remodeled']-exact))),
        'impulse_final_remodeled': float(impulse['remodeled'][-1]),
        'impulse_infinite_time_exact': 0.006,
        'zero_load_max_abs_curvature': float(np.max(np.abs(zero['total']))),
        'no_growth_max_abs_remodeled': float(np.max(np.abs(no_growth['remodeled']))),
        'mirror_max_abs_residual': float(np.max(np.abs(positive['total']+negative['total']))),
        'correction_final_remodeled': float(correction['remodeled'][-1]),
    }
    if args.live:
        from research.alphafold_countercurvature.src.afcc.afdb import AlphaFoldFetcher
        # Separate validation artifacts; never refresh the publication input manifest.
        fetcher = AlphaFoldFetcher(output / 'live/raw', output / 'live/manifest.csv')
        try:
            result = fetcher.fetch_protein('P48436', 'SOX9')
            report['afdb_live'] = result
            if result['status'] not in {'downloaded', 'cached'}:
                raise RuntimeError(f'Live AFDB check failed: {result}')
            report['afdb_cache_repeat'] = fetcher.fetch_protein('P48436', 'SOX9')['status']
            report['afdb_provenance'] = json.loads(fetcher.manifest.iloc[0]['notes'])
        finally:
            fetcher.session.close()
    (output / 'checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
