"""ImbaLink Desk CLI / executable entry point."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from imba_desk.cli.launcher import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
