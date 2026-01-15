# Bolt Report - Summary (Fallback)

**Date:** 2026-01-15
**Status:** Partial Success

## Overview
The pipeline executed with a mix of cached data and failed fetches.
- **Fetch Step:** New candidates failed to download (Network Restrictions).
- **Metrics Step:** Attempted to process cached structures.
- **Reporting:** Automated report generation failed due to missing dependencies (seaborn).

## Manual Insights
- Existing cached structures were found but metrics calculation might have encountered issues (see logs).
- Future runs require network access or local data ingestion.
