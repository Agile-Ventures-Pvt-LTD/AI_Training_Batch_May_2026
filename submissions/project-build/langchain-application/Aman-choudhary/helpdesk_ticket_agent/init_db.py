#!/usr/bin/env python3
"""Initialize the helpdesk agent database with schema and sample data."""

import sqlite3
import os
from pathlib import Path

def init_database():
    """Initialize the database with schema."""
    
    # Define paths
    current_dir = Path(__file__).parent
    db_path = current_dir / "data" / "helpdesk_agent.db"
    schema_path = current_dir / "data" / "helpdesk_agent_db_package" / "helpdesk_agent_schema.sql"
    
    # Ensure data directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if schema file exists
    if not schema_path.exists():
        print(f"ERROR: Schema file not found at {schema_path}")
        return False
    
    # Read schema
    print(f"Reading schema from: {schema_path}")
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Split into statements and organize them
    # Tables first, then indices and views
    statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
    
    # Filter out sqlite_sequence (it's a system table)
    table_stmts = [s for s in statements if s.upper().startswith('CREATE TABLE') and 'sqlite_sequence' not in s.lower()]
    other_stmts = [s for s in statements if not s.upper().startswith('CREATE TABLE') and 'sqlite_sequence' not in s.lower()]
    
    # Connect to database
    print(f"Initializing database at: {db_path}")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # First create all tables
        print("\nCreating tables...")
        for stmt in table_stmts:
            cursor.execute(stmt)
        conn.commit()
        print(f"✓ Created {len(table_stmts)} tables")
        
        # Then create indices and views
        print("\nCreating indices and views...")
        for stmt in other_stmts:
            try:
                cursor.execute(stmt)
            except Exception as e:
                # Skip errors for indices/views (might already exist)
                if "already exists" not in str(e):
                    print(f"  Warning: {e}")
        conn.commit()
        print("✓ Created indices and views")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        print(f"\n✓ Database initialized successfully!")
        print(f"✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"ERROR initializing database: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = init_database()
    exit(0 if success else 1)
