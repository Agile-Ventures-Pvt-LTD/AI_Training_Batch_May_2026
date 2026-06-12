import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__)
        .resolve()
        .parents[1]
    )
)

from tools import (
    search_tickets,
)


def test_search():

    result = search_tickets.invoke(
        {
            "status": "Open"
        }
    )

    assert "tickets" in result