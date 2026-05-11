import sys
import os


def pytest_configure(config):
    """Ensure src/ is first on sys.path so 'solitaire' resolves to src/solitaire."""
    src_path = os.path.join(os.path.dirname(__file__), "src")
    if src_path in sys.path:
        sys.path.remove(src_path)
    sys.path.insert(0, src_path)
