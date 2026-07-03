import pytest
from pathlib import Path
import sqlite3

@pytest.fixture(scope="session")
def test_db(tmp_path_factory):
    src = Path(__file__).parents[2] / "db" / "travel_data.db"
    dst = tmp_path_factory.getbasetemp() / "travel_data.db"
    dst.write_bytes(src.read_bytes())

    conn = sqlite3.connect(dst)
    conn.execute(
        """
        INSERT INTO bookings (booking_id, user_name, user_email,
                              destination, travel_dates, hotel_details)
        VALUES ('TRV-999', 'Alice Example', 'alice@example.com',
                'London, UK', '2024-10-02 to 2024-10-07', 'The Grand London')
        """
    )
    conn.commit()
    conn.close()
    return str(dst)