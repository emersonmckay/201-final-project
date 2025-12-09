import sqlite3

def create_database(filename):
    # creates the database and tables

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    # create table for artists 
    cur.execute('''
                CREATE TABLE IF NOT EXISTS artists (
                artist_name TEXT PRIMARY KEY,
                listeners INTEGER)
                ''')

    # create the table for venues
    cur.execute('''
                CREATE TABLE IF NOT EXISTS venues (
                venue_id TEXT PRIMARY KEY,
                venue_name TEXT,
                city TEXT,
                state TEXT,
                capacity INTEGER)
                ''')
    
    # create a table for events 
    cur.execute('''
                CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                event_name TEXT, 
                artist_name TEXT, 
                date TEXT, 
                venue_id TEXT, 
                FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
                )
                ''')
    
    conn.commit()
    conn.close()

    print(f"Database '{filename}' created successfully!")

    if __name__ == "__main__":
        create_database('ticket_trends.sqlite')