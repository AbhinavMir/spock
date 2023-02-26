import sqlite3

def create_tables():
    # Connect to the database
    db = sqlite3.connect('spock_database.db')
    print("Connected")
    # Create the users table to store the user's public and private keys
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            public_key BLOB NOT NULL,
            private_key BLOB NOT NULL
        )
    """)
    db.commit()

    print("committed")
    # Create the signatures table to store the user's signatures
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY,
            public_key BLOB NOT NULL,
            signature BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()

    # Create the tokens table to store the web login tokens
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY,
            public_key BLOB NOT NULL,
            secret_key BLOB NOT NULL,
            timestamp INTEGER NOT NULL,
            signature BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()

    # Close the database connection
    db.close()

create_tables()
