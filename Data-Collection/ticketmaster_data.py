# Emerson --> ticketmaster api data 

import requests
import sqlite3

def ticket_data(api_key):
    conn = sqlite3.connect("ticket_trends.sqlite")
    cur = conn.cursor()

    # count existing events so we know the correct start position
    cur.execute("SELECT COUNT(*) FROM events")
    current_count = cur.fetchone()[0]
    offset = current_count  # start pos

    print(f"Currently have {current_count} events.")    
    print(f"Fetching up to 25 new events starting at offset {offset}...\n")

    # API Request
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "size": 25,
        "page": offset // 25,
        "countryCode": "US",
        "segmentName": "Music"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "_embedded" not in data or "events" not in data["_embedded"]:
        print("No new events found.")
        conn.close()
        return

    events = data["_embedded"]["events"]
    event_dict = {}

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

            if artist_name:
                cur.execute("""
                    INSERT OR IGNORE INTO artists (artist_name, listeners)
                    VALUES (?, NULL)
                """, (artist_name,))

            # venue info
            if "venues" not in event["_embedded"]:
                continue
                
            venue = event["_embedded"]["venues"][0]
            venue_id = venue.get("id")  # get the venue_id from API
            venue_name = venue.get("name")
            city = venue.get("city", {}).get("name")
            state = venue.get("state", {}).get("stateCode")

            # INSERT venue 
            cur.execute("""
                INSERT OR IGNORE INTO venues (venue_id, venue_name, city, state)
                VALUES (?, ?, ?, ?)
            """, (venue_id, venue_name, city, state))

            # event
            cur.execute("""
                INSERT OR IGNORE INTO events
                (event_id, event_name, artist_name, date, venue_id)
                VALUES (?, ?, ?, ?, ?)
            """, (event_id, event_name, artist_name, date, venue_id))

            event_dict[event_name] = {"artist": artist_name}
        except Exception as e:
            print("ERROR:", e)

    conn.commit()
    conn.close()
    return event_dict 

if __name__ == "__main__":
    API_KEY = "lfCVtbiZSWpr7HmZUUGWa8C1chUvuvpU"

    print("\nTesting Ticketmaster API data insert...\n")
    ticket_data(API_KEY)

    conn = sqlite3.connect("ticket_trends.sqlite")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM events")
    print("Events after run:", cur.fetchone()[0])

    cur.execute("SELECT COUNT(*) FROM venues")
    print("Venues after run:", cur.fetchone()[0])

    conn.close()
