import pandas as pd

# Load the raw merged data
df = pd.read_csv("Merged_Event_Data.csv", encoding="utf-8-sig")

# 1. Fix Source based on presence of search_term
df["Source"] = df["search_term"].apply(lambda x: "YouTube" if isinstance(x, str) and len(x.strip()) > 0 else "Eventbrite")

# 2. Fix missing titles for Eventbrite by reloading original
df_eventbrite = pd.read_csv("Eventbrite_Events_Raw.csv", encoding="utf-8-sig")

# 3. Normalize casing for consistent merging
df_eventbrite["Location"] = df_eventbrite["Location"].str.lower()
df_eventbrite["Description"] = df_eventbrite["Description"].str.lower()
df_eventbrite["Category"] = df_eventbrite["Category"].str.lower()

# 4. Update Eventbrite rows in original dataframe with proper titles
eventbrite_only = df[df["Source"] == "Eventbrite"].copy().reset_index(drop=True)
eventbrite_only["title"] = df_eventbrite["Event_Name"]
eventbrite_only["category"] = df_eventbrite["Category"]
eventbrite_only["description"] = df_eventbrite["Description"]
eventbrite_only["Location"] = df_eventbrite["Location"]
eventbrite_only["publishedAt"] = df_eventbrite["Date(s)"]

# 5. Add category for YouTube rows based on search_term
youtube_only = df[df["Source"] == "YouTube"].copy().reset_index(drop=True)
youtube_only["category"] = youtube_only["search_term"].apply(
    lambda x: "music festival" if isinstance(x, str) and "#musicfestival" in x.lower() else None
)

# 6. Combine everything together
df_cleaned = pd.concat([eventbrite_only, youtube_only], ignore_index=True)

# 7. Remove unwanted columns
#    Remove 'predicted category' if present
df_cleaned.drop(columns=["predicted category"], inplace=True, errors="ignore")

#    Remove duplicate description-like columns
duplicate_cols = [col for col in df_cleaned.columns if "description" in col.lower() and col != "description"]
df_cleaned.drop(columns=duplicate_cols, inplace=True)

# 8. Save cleaned file
df_cleaned.to_csv("Final_Cleaned_Event_Data.csv", index=False)

# 9. Print confirmation
print("Final merged file saved as 'Final_Cleaned_Event_Data.csv'")
print("Cleaned columns:", df_cleaned.columns.tolist())
print("Sample rows:")
print(df_cleaned.head(15))
