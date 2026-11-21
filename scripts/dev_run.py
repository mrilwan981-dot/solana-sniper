"""Convenience script: run the bot with a dry-run override."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.App.bootstrap import main  # noqa: E402

if __name__ == "__main__":
    os.environ.setdefault("DRY_RUN", "true")
    main()