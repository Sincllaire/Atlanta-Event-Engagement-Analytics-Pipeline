import requests
import pandas as pd 
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv(dotenv_path="EBK.env")
API_KEY = os.getenv("EVENTBRITE_API_KEY")

# Define categories and search keywords
keywords = {
    "Music": ["music", "concerts", "DJ", "Boiler Room"],
    "Tech": ["tech", "networking", "non-profit", "fundraiser"],
    "Culture & Art": ["art", "Culture", "dance", "festival"],
    "Food & Social": ["food", "party", "celebration"],
    "Networking & Student Events": [
        "networking event", "career fair", "student networking", "tech networking", "diversity in tech",
        "black in tech", "young professionals", "college career day", "HBCU networking", "#networkingevent",
        "#careerfair", "#blackintech", "#studentnetworking", "#diversityintech", "#youngprofessionals"
    ],
    "Festivals & Community Events": [
        "atlanta festival", "atl block party", "atlanta weekend", "community event", "music festival atlanta",
        "black festival", "atlanta food festival", "atlanta music festival", "day in the life festival",
        "#atlblockparty", "#atlfestival", "#communityevent", "#blackjoy", "#musicfestival"
    ]
}

# Eventbrite API endpoint and headers
url = "https://www.eventbriteapi.com/v3/events/search"
headers = { "Authorization": f"Bearer {API_KEY}" }

print("Attempting to pull Eventbrite data (fallback enabled if blocked)...")

try:
    all_events = []

    for category, word_list in keywords.items():
        for keyword in word_list:
            print(f"Fetching events under this keyword: {keyword}")

            params = {
                "location.address": "Atlanta",
                "q": keyword,
                "expand": "venue",
                "page": 1
            }

            response = requests.get(url, headers=headers, params=params)
            print(f"Searching Eventbrite for: {keyword}")
            print(f"Status Code: {response.status_code}")
            print(response.json())

            if response.status_code == 404:
                print("API access denied. Skipping actual pull.")
                continue

            data = response.json()
            events = data.get("events", [])
            print(f"{keyword} — events found: {len(events)}")

            for event in events:
                all_events.append({
                    "name": event.get("name", {}).get("text"),
                    "start": event.get("start", {}).get("local"),
                    "end": event.get("end", {}).get("local"),
                    "url": event.get("url"),
                    "description": event.get("description", {}).get("text"),
                    "venue_name": event.get("venue", {}).get("name") if event.get("venue") else None,
                    "venue_address": event.get("venue", {}).get("address", {}).get("localized_address_display") if event.get("venue") else None,
                    "search_term": keyword
                })

    if all_events:
        df = pd.DataFrame(all_events)
        df.to_csv("Eventbrite_Events_Raw.csv", index=False)
        print("Saved Eventbrite_Events_Raw.csv")
    else:
        print("No events found or API inaccessible. Using local CSV manually if needed.")

except Exception as e:
    print("Error occurred during Eventbrite pull. Skipping pull.")
    print("Error:", e)

print("Reminder: Eventbrite API access requires partner-level permissions.")
print("This script runs in placeholder mode to keep your pipeline running.")
