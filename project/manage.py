#!/usr/bin/env python

from django.core.management import execute_manager

try:
    import settings  # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("[33mHelp! [[34msettings.py[33m] is gone![0m\\n")
    sys.exit(1)


if __name__ == "__main__":
    execute_manager(settings)
