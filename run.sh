#!/bin/bash
# Code Ocean Entry Point
# This script executes the master analysis pipeline.

echo "Initializing Biological Countercurvature Analysis Pipeline..."

# Ensure results directory exists
mkdir -p ../results

# Run the master script
# We set RESULTS_DIR explicitly to ensure Code Ocean compliance
export RESULTS_DIR="../results"
python3 main.py

echo "Analysis complete. Results should be available in the results folder."
