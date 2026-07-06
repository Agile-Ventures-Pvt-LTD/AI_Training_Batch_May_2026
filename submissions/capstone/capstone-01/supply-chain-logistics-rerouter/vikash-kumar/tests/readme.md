# Run standard logical unit tests
uv run pytest tests/ -v

# Run integration tests requiring API connection blocks
uv run pytest -m integration -v

# Pipe structural test suite outcomes directly into documentation files
uv run pytest tests/ -v > outputs/test_results.txt

uv run python src/main.py
