import os
import sqlite3

def init_db():
    try:
        # Get the current script's directory and create the full database path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, 'vulnerable.db')
        
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            ssn TEXT,
            credit_card_number TEXT,
            hobbies TEXT
        )
        ''')
        
        # Insert a test user
        cursor.execute("INSERT INTO users (username, password, ssn, credit_card_number, hobbies) VALUES (?, ?, ?, ?, ?)", 
                       ('jake', 'statefarm', '123-45-6789', '4111111111111111', 'reading, hiking'))
        
        connection.commit()
        print("Database initialized successfully at:", db_path)
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Initialize the database
init_db()
