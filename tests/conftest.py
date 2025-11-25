"""Test configuration file for pytest."""
from __future__ import annotations

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src" / "python"
sys.path.insert(0, str(src_path))
