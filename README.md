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
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/b15f829a-c122-485a-8203-57ee044fc418" />


2. GCP Visual to show Question 1:
   
   -How many events come from Youtube vs. Eventbrite?
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/647cfb4c-27e2-4f44-ab7b-583213c693e8" />


3. GCP Visual to show question 2:
   
   -What were the most popular event categories?
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/fc6db24d-98bf-4182-8818-c129f853660f" />


4. GCP Visual to show Question 3:

   - What is the distribution of sources across each category?
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/32a77d80-3d8a-494c-9233-c98b8b155045" />


5. Visual for the final Tableau dashboard showcasing all tableau pictures
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/4a81217d-606c-41cf-afab-bbd07b036282" />




### Query 1: Count of Events by Source
```sql
SELECT source, COUNT(*) AS event_count
FROM `your_project_id.ga_events_project.Final_Cleaned_Event_Data`
GROUP BY source
```
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/7feb45e0-705f-4676-8ad9-00aef234547a" />

### Query 2: Most Common Event Categories
```sql
SELECT category, COUNT(*) AS category_count
FROM `your_project_id.ga_events_project.Final_Cleaned_Event_Data`
GROUP BY category
ORDER BY category_count DESC
```
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/9843f11d-ce97-4e6a-855b-372191ce8ca1" />

### Query 3: Event Categories by Source
```sql
SELECT category, source, COUNT(*) AS event_count
FROM `your_project_id.ga_events_project.Final_Cleaned_Event_Data`
GROUP BY category, source
ORDER BY category
```
<img width="600" alt="Image" src="https://github.com/user-attachments/assets/ec72e174-dbd5-4953-995e-24ab8c9b2c79" />

## Project Workflow
- Day 1–3: Data Collection & Cleaning
Pulled YouTube data using API

Manually curated Eventbrite dataset

Cleaned and merged using a Python script

- Day 4: Airflow Pipeline
Created Airflow DAG to automate CSV merging + cleaning

Scheduled DAG to run daily

- Day 5–6: GCP BigQuery Integration
Uploaded merged CSV to BigQuery

Wrote SQL queries to explore event behavior

- Day 7: Tableau Dashboard
Connected BigQuery to Tableau

Built visualizations for final report


## Future Improvements
-Scrape real-time Eventbrite data with authenticated access

-Classify events using NLP

-Add interactive filters by neighborhood or time

