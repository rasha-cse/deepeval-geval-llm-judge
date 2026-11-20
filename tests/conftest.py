import sys
from pathlib import Path

# Make `app` and `evals` importable when running `deepeval test run tests/`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
