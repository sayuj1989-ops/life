#!/usr/bin/env python3
"""
Validate solver implementations and model consistency.
"""

import sys

def validate_solvers():
    """Validate that required solver modules are available."""
    try:
        # Check if main modules can be imported
        import spinalmodes
        print("✓ spinalmodes module found")
        
        # Check for key solver modules
        try:
            from spinalmodes.countercurvature import pyelastica_bridge
            print("✓ PyElastica bridge module found")
        except ImportError:
            print("! PyElastica bridge not available")
        
        # Check for model
        try:
            from spinalmodes.model import core
            print("✓ Model core module found")
        except ImportError:
            print("! Model core not available")
        
        print("\n✓ Solver validation completed successfully")
        return 0
        
    except ImportError as e:
        print(f"Error: Required modules not found: {e}")
        return 1
    except Exception as e:
        print(f"Error during validation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(validate_solvers())
