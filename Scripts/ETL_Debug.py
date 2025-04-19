import pandas as pd

df_eventbrite = pd.read_csv("Eventbrite_Events_Raw.csv")

print("Columns in CSV:", df_eventbrite.columns.tolist())  # 🧠 This helps debug
