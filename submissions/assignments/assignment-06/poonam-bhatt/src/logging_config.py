import logging
import sys

def setup_logging(level=logging.WARNING):
    """Sets up a unified logger outputting to stderr (keeping stdout clean for JSON-RPC stdio)."""
    # Clear any pre-existing handlers on the root logger to avoid duplicates
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
            
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr
    )
