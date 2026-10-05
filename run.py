"""Development launcher: ``python run.py`` (puts ./src on the path, then starts LUTHO)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from lutho.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
