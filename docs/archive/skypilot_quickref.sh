#!/bin/bash
# SkyPilot Quick Reference Card
# Print this for easy access to common commands

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║           SKYPILOT MANUSCRIPT EDITING - QUICK REF            ║
╚══════════════════════════════════════════════════════════════╝

📋 COMMON COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ./sky_edit.sh test          # Test setup (5 min, $0.03)
  ./sky_edit.sh launch        # Edit manuscript (15 min, $0.08)
  ./sky_edit.sh launch-spot   # Spot instance (15 min, $0.02)
  ./sky_edit.sh status        # Check job status
  ./sky_edit.sh logs          # View real-time logs
  ./sky_edit.sh stop          # Stop all clusters
  ./sky_edit.sh cost          # Show cost estimate

🚀 FIRST TIME SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Get RunPod API key: https://www.runpod.io/console/user/settings
  2. Configure: runpod config
  3. Verify: sky check
  4. Test: ./sky_edit.sh test

💰 COST COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  On-Demand:  $0.08 per run  (guaranteed)
  Spot:       $0.02 per run  (3-6x cheaper, may be preempted)
  Test:       $0.03 per run  (quick verification)

⚡ PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Local Instella-3B:    30-45 min  (CPU, slow)
  Manual RunPod:        18-27 min  (manual setup)
  SkyPilot (this):      10-15 min  (automated)

📁 FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  manuscript_editing.yaml       # Main task (on-demand)
  manuscript_editing_spot.yaml  # Spot variant
  test_qwen.yaml                # Test task
  edit_manuscript_cloud.py      # Cloud editor
  sky_edit.sh                   # This wrapper
  edited_sections/              # Output directory

📚 DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  SKYPILOT_QUICKSTART.md        # Getting started
  SKYPILOT_ADVANCED.md          # Advanced features
  SKYPILOT_SETUP_COMPLETE.md    # Setup summary

🔧 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  "No clouds enabled"
    → Run: runpod config
    → Add API key from RunPod dashboard

  "No GPU available"
    → Try: ./sky_edit.sh launch-spot
    → Or wait a few minutes and retry

  "Job failed"
    → Check: ./sky_edit.sh logs
    → Verify: life/manuscript/ directory exists

  "Model download slow"
    → First run takes 5-10 min (downloads 60GB)
    → Subsequent runs use cached model

🎯 WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Launch:    ./sky_edit.sh launch
  2. Monitor:   ./sky_edit.sh logs (optional)
  3. Results:   Auto-downloaded to edited_sections/
  4. Cleanup:   Automatic (or ./sky_edit.sh stop)

📊 INTERACTIVE MENU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ./research_workflow.sh

  Then select:
    13. Launch SkyPilot manuscript editing
    14. Check SkyPilot job status
    15. Download SkyPilot results

🌐 CLOUD PROVIDERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  RunPod:   runpod config
  Lambda:   ~/.lambda_cloud/lambda_keys
  Vast.ai:  ~/.config/vastai/vast_api_key

  Verify:   sky check

💡 TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Use spot instances for 3-6x cost savings
  • First run downloads model (5-10 min)
  • Subsequent runs are much faster
  • Results auto-sync to edited_sections/
  • Clusters auto-stop after completion

🆘 SUPPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ./sky_edit.sh help
  sky --help
  https://docs.skypilot.co

╔══════════════════════════════════════════════════════════════╗
║  Quick Start: ./sky_edit.sh test (5 min, $0.03)              ║
╚══════════════════════════════════════════════════════════════╝
EOF
