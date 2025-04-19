from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'sinclaire',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    dag_id='events_pipeline_dag',
    default_args=default_args,
    description='Clean and merge Eventbrite and YouTube data from existing CSVs',
    start_date=datetime(2025, 4, 1),
    schedule_interval='@daily',
    catchup=False
)

# Step 1: Eventbrite Pull – just a placeholder, since data is already in CSV
def pull_eventbrite_data():
    print("Eventbrite data already available in Eventbrite_Events_Raw.csv.")

# Step 2: Transform – clean and merge the CSVs
def transform_data():
    merged_path = "/Users/sinclairehoyt/Desktop/BigDataEventsProject/Merged_Event_Data.csv"
    eventbrite_path = "/Users/sinclairehoyt/Desktop/BigDataEventsProject/Eventbrite_Events_Raw.csv"

    df = pd.read_csv(merged_path, encoding="utf-8-sig")
    df_eventbrite = pd.read_csv(eventbrite_path, encoding="utf-8-sig")

    # Check for key columns
    if "search_term" not in df.columns:
        raise ValueError("Missing 'search_term' in Merged CSV")
    if "Event_Name" not in df_eventbrite.columns:
        raise ValueError("Missing 'Event_Name' in Eventbrite CSV")

    # Fix source
    df["Source"] = df["search_term"].apply(lambda x: "YouTube" if isinstance(x, str) and len(x.strip()) > 0 else "Eventbrite")

    # Normalize eventbrite data
    df_eventbrite["Location"] = df_eventbrite["Location"].str.lower()
    df_eventbrite["Description"] = df_eventbrite["Description"].str.lower()
    df_eventbrite["Category"] = df_eventbrite["Category"].str.lower()

    eventbrite_only = df[df["Source"] == "Eventbrite"].copy().reset_index(drop=True)
    eventbrite_only["title"] = df_eventbrite["Event_Name"]
    eventbrite_only["category"] = df_eventbrite["Category"]
    eventbrite_only["description"] = df_eventbrite["Description"]
    eventbrite_only["Location"] = df_eventbrite["Location"]
    eventbrite_only["publishedAt"] = df_eventbrite["Date(s)"]

    # Clean up duplicates
    duplicate_cols = [col for col in df_eventbrite.columns if "description" in col.lower() and col != "description"]
    df_eventbrite.drop(columns=duplicate_cols, inplace=True, errors="ignore")

    # YouTube category logic
    youtube_only = df[df["Source"] == "YouTube"].copy().reset_index(drop=True)
    youtube_only["category"] = youtube_only["search_term"].apply(
        lambda x: "music festival" if isinstance(x, str) and "#musicfestival" in x.lower() else None
    )

    # Combine and clean
    df_cleaned = pd.concat([eventbrite_only, youtube_only], ignore_index=True)
    df_cleaned.drop(columns=["predicted category"], inplace=True, errors="ignore")

    # Save after everything is ready
    df_cleaned.to_csv("/Users/sinclairehoyt/Desktop/BigDataEventsProject/Final_Cleaned_Event_Data.csv", index=False)
    print("Cleaned and saved: Final_Cleaned_Event_Data.csv")

# Step 3: Load – just confirm the result
def load_data():
    final_path = "/Users/sinclairehoyt/Desktop/BigDataEventsProject/Final_Cleaned_Event_Data.csv"
    try:
        df = pd.read_csv(final_path)
        print("Loaded final cleaned data csv successfully")
        print(df.head(30))
    except:
        print("Load Failed: {e}")
        raise


# Operators
pull_eventbrite_task = PythonOperator(
    task_id='pull_eventbrite',
    python_callable=pull_eventbrite_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

# DAG Task Order
pull_eventbrite_task >> transform_task >> load_task


