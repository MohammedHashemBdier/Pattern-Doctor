#!/usr/bin/env python3
"""
PATTERN DOCTOR - DESIGN PATTERN PICKER —  Entry Point
=====================================
Run with:  python3 run.py

This thin launcher imports ``main`` from cli.py and invokes it.
Keeping it separate means cli.py contains ZERO ``if`` statements
(not even the ``if __name__ == '__main__'`` guard), so the entire
codebase is free of the forbidden constructs.
"""

from cli import main

main()
