"""
Main entry point for running offline-transcriber as a module.
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main()) 