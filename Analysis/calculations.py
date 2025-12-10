# Emerson 

import sqlite3

def calculations(db_name):

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # artist name, number of concerts, number of events per artists (artists.___ will be
    # will be null until we have last.fm data
    cur.execute("""
            SELECT
                artists.artist_name,
                artists.listeners,
                events.artist_name,
                COUNT(events.event_id) AS num_concerts,
                COUNT(DISTINCT venues.venue_id) AS num_venues
            FROM events
            LEFT JOIN events ON artists.artist_name = events.artist_name
            LEFT JOIN venues ON events.venue_id = venues.venue_id
            GROUP BY events.artist_name
            ORDER BY num_concerts DESC;       
            """)

    results = cur.fetchall()
    conn.close()

    return results

if __name__ == "__main__":
    db_name = "ticket_trends.sqlite"  
    print("Artist, num of concerts, and number of unique venues:")
    print(calculations("ticket_trends.sqlite"))

