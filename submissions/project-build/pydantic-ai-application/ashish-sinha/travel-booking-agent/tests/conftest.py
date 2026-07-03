import pytest
import asyncio
import os
import sqlite3

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session')
def mock_database_setup(tmp_path_factory):
    temp_directory = tmp_path_factory.mktemp("data")
    database_file = temp_directory / "travel_data.db"
    
    connection = sqlite3.connect(str(database_file))
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY,
            booking_id TEXT,
            user_name TEXT,
            user_email TEXT,
            destination TEXT,
            travel_dates TEXT,
            hotel_details TEXT
        )
    """)
    cursor.execute(""" INSERT INTO bookings(id,booking_id,user_name,user_email,destination,travel_dates,hotel_details)
                    VALUES(7,123,'Ashish Sinha','ashish@gmail.com','London, UK','July 10-26','ABC Hotel')""")
    connection.commit()
    connection.close()
    return str(database_file)