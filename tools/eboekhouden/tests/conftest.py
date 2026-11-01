"""Test-only import root; no credential/network or runtime-directory setup."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
