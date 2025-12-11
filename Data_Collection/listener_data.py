# Charlotte --> last.fm api data 

import requests
import sqlite3

def listener_data(api_key):

    conn = sqlite3.connect("ticket_trends.sqlite")
    cur = conn.cursor()

    print("Fetching Last.fm listener data...")

    # Counting the existing artists 
    cur.execute("SELECT COUNT(*) FROM artists")
    current_count = cur.fetchone()[0]

    print(f"Currently have {current_count} artists stored.")
    print(f"Fetching up to 25 new tag-based artists...\n") 

    base_url = "http://ws.audioscrobbler.com/2.0/"

    # Rotating multiple tags to gather artists
    tags = ["pop", "rap", "rock", "indie", "hip-hop"]
    tag = tags[current_count % len(tags)]

    # Collecting artists by tags 
    tag_params = {
        "method": "tag.gettopartists",
        "api_key": api_key,
        "tag": tag,
        "format": "json",
        "limit": 25
    }

    response = requests.get(base_url, params=tag_params)

    if response.status_code != 200:
        print("API Error:", response.status_code)
        conn.close()
        return {}
    
    data = response.json()

    if "topartists" not in data or "artist" not in data["topartists"]:
        print("No artist data found in tag search.")
        conn.close()
        return {}
    
    tag_artists = data["topartists"]["artist"]
    updated_artists = {}

    # Helper function for fetching listener count from Last.fm
    def fetch_listener_count(artist_name):
        info_params = {
            "method": "artist.getinfo",
            "artist": artist_name,
            "api_key": api_key,
            "format": "json"
        }

        try:
            info_response = requests.get(base_url, params=info_params).json()
            listeners = int(info_response.get("artist", {}).get("stats", {}).get("listeners", 0))
            return listeners 
        except:
            return 0 

    # Update tag-based artists 
    for artist in tag_artists:
        name = artist.get("name")
        listeners = fetch_listener_count(name)

        cur.execute("""
            INSERT OR IGNORE INTO artists (artist_name, listeners)
            VALUES (?, ?)
        """, (name, listeners))

        cur.execute("""
            UPDATE artists
            SET listeners = ?
            WHERE artist_name = ? AND (listeners IS NULL OR listeners = 0)
        """, (listeners, name))

        updated_artists[name] = listeners 

    print(f"Updated {len(updated_artists)} tag-based artists.\n")

    # Fill in listener counts for ticketmaster artists 
    print("Checking Ticketmaster artists for missing listener data...")

    cur.execute("SELECT DISTINCT artist_name FROM events")
    tm_artists = [row[0] for row in cur.fetchall()]

    fill_count = 0 

    for name in tm_artists:
        if not name:
            continue 

        cur.execute("SELECT listeners FROM artists WHERE artist_name = ?", (name,))
        row = cur.fetchone() 
        current_listener_value = row[0] if row else None 

        if current_listener_value not in (None, 0):
            continue 

        listeners = fetch_listener_count(name) 

        cur.execute("""
            INSERT OR IGNORE INTO artists (artist_name, listeners)
            VALUES (?, ?)
        """, (name, listeners))

        cur.execute("""
            UPDATE artists
            SET listeners = ?
            WHERE artist_name = ?
        """, (listeners, name))

        updated_artists[name] = listeners
        fill_count += 1 

    conn.commit()
    conn.close()

    print(f"Filled in listener data for {fill_count} Ticketmaster artists.\n")
    print("Listener data collection complete.\n")

    return updated_artists

if __name__ == "__main__":
    API_KEY = "	e7daacfe434e52e4cfd7c8f6b1004d29"
    print(listener_data(API_KEY))