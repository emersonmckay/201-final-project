import requests
import sqlite3

# will need to update things to match db table 

def ticket_data(api_key):
    """
    Fetches Ticketmaster music events and inserts up to 25 new records
    into the database once created.
    """

    conn = sqlite3.connect("concert_data.db")
    cur = conn.cursor()

    # count existing events so we know the correct start position
    cur.execute("SELECT COUNT(*) FROM events")
    current_count = cur.fetchone()[0]
    offset = current_count  # changed from start_pos to offset

    print(f"Currently have {current_count} events.")    
    print(f"Fetching up to 25 new events starting at offset {offset}...\n")

    # API Request
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "classificationName": "music",
        "size": 25, # size from project rubric 
        "offset": offset # start pos 
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "_embedded" not in data or "events" not in data["_embedded"]:
        print("No new events found.")
        conn.close()
        return

    events = data["_embedded"]["events"]
    added = 0

    # insert rows into pre-existing tables
    for event in events:
        try:
            event_id = event["id"]
            event_name = event.get("name")
            date = event.get("dates", {}).get("start", {}).get("localDate")

            # artist name
            artist_name = None
            if "_embedded" in event and "attractions" in event["_embedded"]:
                artist_name = event["_embedded"]["attractions"][0].get("name")

            # venue info
            if "_embedded" not in event or "venues" not in event["_embedded"]:
                continue
                
            venue = event["_embedded"]["venues"][0]
            venue_id = venue.get("id")  # Get the venue_id from API
            venue_name = venue.get("name")
            city = venue.get("city", {}).get("name")
            state = venue.get("state", {}).get("stateCode")  # Changed to stateCode
            capacity = venue.get("capacity", 0)  # Get capacity from venue

            # INSERT venue (make sure this matches Charlotte's table structure!)
            cur.execute("""
                INSERT OR IGNORE INTO venues (venue_id, venue_name, city, state, capacity)
                VALUES (?, ?, ?, ?, ?)
            """, (venue_id, venue_name, city, state, capacity))

            # INSERT event (removed capacity from here)
            cur.execute("""
                INSERT OR IGNORE INTO events
                (event_id, event_name, artist_name, date, venue_id)
                VALUES (?, ?, ?, ?, ?)
            """, (event_id, event_name, artist_name, date, venue_id))

            added += 1

        except Exception as e:
            print("Error processing event:", e)
            continue

    conn.commit()
    conn.close()
    print(f"Added {added} new events.")

if __name__ == "__main__":
    API_KEY = "hhTxipVoQr6QL7o35d9NnSwWf7h9h2vU"

    print("\nTesting Ticketmaster API data insert...\n")
    ticket_data(API_KEY)

    conn = sqlite3.connect("concert_data.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM events")
    print("Events after run:", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM venues")
    print("Venues after run:", cur.fetchone()[0])

    conn.close()
