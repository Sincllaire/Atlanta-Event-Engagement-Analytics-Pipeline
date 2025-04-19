# Atlanta Event Engagement Analytics Pipeline

This project explores the types of events people attend in Atlanta by analyzing and cleaning event data from Eventbrite and YouTube. Using a modern data pipeline approach, I automated ETL processes and visualized key insights in both BigQuery and Tableau.

---

## Project Overview

- **Goal:** Understand where people get event information, what types of events they attend, and how that differs by source (YouTube vs Eventbrite).
- **Tools Used:** Python, Apache Airflow, Google Cloud Platform (BigQuery), SQL, Tableau
- **Dataset Sources:** 
  - YouTube Data API (for vlogs & videos tagged in Atlanta)
  - Manually created Eventbrite mock dataset (API access restricted)

---

## Technologies & Tools

| Tool            | Purpose                                 |
|-----------------|-----------------------------------------|
| Python          | Data extraction, cleaning, transformation |
| Airflow         | Automating ETL pipelines                |
| GCP BigQuery    | Cloud-based data storage & SQL analysis |
| Tableau         | Final visual dashboard & storytelling   |

---

## Key Questions Explored

1. How many events came from YouTube vs Eventbrite?
2. What were the most popular event categories?
3. What is the distribution of sources across each category?

---

## Visualizations
1. Visual of  fully completed Apache Airflow DAG

2. GCP Visual to show Question 1: /n 
   -How many events come from Youtube vs. Eventbrite?
   <img width="877" alt="Image" src="https://github.com/user-attachments/assets/cfff8c92-63c7-4441-a53c-d8453b719bfe" />




### Query 1: Count of Events by Source
```sql
SELECT source, COUNT(*) AS event_count
FROM `your_project_id.ga_events_project.Final_Cleaned_Event_Data`
GROUP BY source
