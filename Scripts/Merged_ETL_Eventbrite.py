import pandas as pd

df_eventbrite = pd.read_csv("Eventbrite_Events_Raw.csv")
df_eventbrite["Date(s)"] = pd.to_datetime(df_eventbrite["Date(s)"], errors="coerce")
df_eventbrite["Event_Name"] = df_eventbrite["Event_Name"].str.lower()
df_eventbrite["Description"] = df_eventbrite["Description"].str.lower()
df_eventbrite["Category"] = df_eventbrite["Category"].str.lower()
df_eventbrite["Location"] = df_eventbrite["Location"].str.lower()
df_eventbrite["Source"] = df_eventbrite["Source"].str.lower()

df_eventbrite.dropna(inplace = True)

keywords = {
    "Music": ["music", "concerts", "DJ", "Boiler Room"],
    "Tech": ["tech", "networking", "non-profit","fundraiser"],
    "Culture & Art": ["art", "Culture", "dance", "festival"],
    "Food & Social": ["food", "party", "celebration"],
    "Networking & Student Events": ["networking event", "career fair", "student networking", "tech networking", "diversity in tech", "black in tech", "young professionals", "college career day", 
                                    "HBCU networking", "#networkingevent", "#careerfair", "#blackintech", "#studentnetworking", "#diversityintech", "#youngprofessionals"],
    "Festivals & Community Events": ["atlanta festival", "atl block party", "atlanta weekend", "community event", "music festival atlanta", "black festival", "atlanta food festival", 
                                     "atlanta music festival", "day in the life festival", "#atlblockparty", "#atlfestival", "#communityevent", "#blackjoy", "#musicfestival"]
}


def assign_category(row):
    for category, wordlist in keywords.items():
         for keyword in wordlist:
          if keyword in row["Event_Name"] or row["Description"]:
                return category
    return "Other"


df_eventbrite["predicted category"] = df_eventbrite.apply(assign_category, axis=1)

df_youtube = pd.read_csv("Youtube_Data_Raw.csv", encoding="utf-8-sig")


merged_df = pd.concat([df_youtube, df_eventbrite], ignore_index=True)
merged_df.to_csv("Merged_Event_Data.csv", index=False)
print("✅ Merged CSV saved as Merged_Event_Data.csv")