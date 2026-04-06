#!/bin/bash
export PATH="/home/jules/self_created_tools/bin:$PATH"
export GEMINI_API_KEY="dummy"

# Ensure paperbanana commands run
paperbanana generate --input research/figures/complex_mechanism_derivative_gain_trap.txt --caption "Mechanism" --output research/figures/test_generate.png
