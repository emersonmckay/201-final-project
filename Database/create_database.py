# Charlotte 

import sqlite3

def create_database():
    """
    Creating the SQLite database with tables for
    ticket data and listener data
    """

    conn = sqlite3.connect("ticket_trends.sqlite")
    cur = conn.cursor() 

    #Artists table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_name TEXT UNIQUE,
            listeners INTEGER
        ); 
    """) 

    #Venues table 
    cur.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                venue_id TEXT PRIMARY KEY,
                venue_name TEXT,
                city TEXT,
                state TEXT
            ); 
        """)
    
    #Events table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            event_name TEXT,
            artist_name TEXT,
            date TEXT,
            venue_id TEXT,
            FOREIGN KEY (artist_name) REFERENCES artists(artist_name),
            FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
        );
    """)

    conn.commit()
    conn.close()

    print(f"Database created successfully with tables: artists, venues, and events.")

if __name__ == "__main__":
    create_database()