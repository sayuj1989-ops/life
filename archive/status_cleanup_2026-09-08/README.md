# Historical status archive — 2026-09-08

These ten May 2026 status documents claimed readiness before later null results and integrity audits. They are retained for provenance, not current scientific guidance.

`manifest.json` records original paths, archive paths, reasons, and SHA-256 hashes. No document content was changed. Restore the ten moved files with:

```bash
python3 archive/status_cleanup_2026-09-08/restore.py
```

The restore script refuses to overwrite any existing file and checks every hash before moving. `README.before-cleanup.md` preserves the original root README; it is not automatically restored.

The legacy `DO_THIS_NOW.txt` and `SUBMISSION_READY_FINAL.md` remain at the root because `final_verification.sh` references them. The script and these documents are historical workflow material and do not establish current publication readiness.
