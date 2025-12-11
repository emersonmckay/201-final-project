# Charlotte --> last.fm api data 

import requests
import sqlite3

def listener_data(api_key):

    conn = sqlite3.connect("ticket_trends.sqlite")
    cur = conn.cursor()

    #Counting the existing artists 
    cur.execute("SELECT COUNT(*) FROM artists")
    current_count = cur.fetchone()[0]
    starting = current_count

    print(f"Currently have {current_count} artists stored.")
    print(f"Fetching up to 25 new artists starting at {starting}...\n") 

    base_url = "http://ws.audioscrobbler.com/2.0/"

    #Using multiple tags to gather artists
    tags = ["pop", "rap", "rock", "indie", "hip-hop"]

    tag = tags[starting % len(tags)]

    params = {
        "method": "tag.gettopartists",
        "api_key": api_key,
        "tag": tag,
        "format": "json",
        "limit": 25
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print("API Error:", response.status_code)
        conn.close()
        return {}
    
    data = response.json()

    if "topartists" not in data or "artist" not in data["topartists"]:
        print("No artist data found.")
        conn.close()
        return {}
    
    artists = data["topartists"]["artist"]
    new_artist_dict = {}
    for artist in artists:
        try:
            name = artist.get("name")
            listeners = int(artist.get("listeners", 0))

            cur.execute("""
                INSERT OR IGNORE INTO artists (artist_name, listeners)
                VALUES (?, ?)
            """, (name, listeners))

            cur.execute("""
                UPDATE artists
                SET listeners = ?
                WHERE artist_name = ? AND listeners IS NULL OR listeners = 0)
            """, (listeners, name))

            new_artist_dict[name] = listeners 

        except Exception as e:
            print("Error:", e)

    conn.commit()
    conn.close()

    print(f"Added {len(new_artist_dict)} new artists.\n")
    return new_artist_dict


if __name__ == "__main__":
    API_KEY = "	e7daacfe434e52e4cfd7c8f6b1004d29"
    print(listener_data(API_KEY))