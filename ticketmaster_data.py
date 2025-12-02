import requests
import json

api_key = "hhTxipVoQr6QL7o35d9NnSwWf7h9h2vU"

def raw_ticket_data(artist_name, api_key=api_key):
    """
    Make a request to the Ticketmaster API and return the raw
    JSON data for events matching the artist.
    """

    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": api_key,
        "keyword": artist_name,
        "size": 20   # number of events to load (20 is fine)
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
    except:
        print("There was an error making the request.")
        return None
    
    return data


if __name__ == "__main__":
    # use Taylor Swift ONLY as a test artist to confirm the code works
    artist = "Taylor Swift"
    data = raw_ticket_data(artist)

    if data:
        print(json.dumps(data, indent=2))
