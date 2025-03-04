📌 Deel Home Task
========

In this repository, you will find the solution to my task proposed by Deel. The main requirement was to develop a simple data system that alerts the team when there is a change greater than 50% in the client's balance.

🚀 Technologies
================
- Python 3.11
- Astronomer Airflow
- Snowflake
- Docker
- dbt (version 1.9.0)

📂 Detailed Project Structure
- At folder dags/dbt/deel_home_task/ it will be find the dbt project with the task solution will be found, also incorporating best practices with dbt, a connection to Snowflake, and the structure of a data pipeline.
- At folder dags/scrits it will be our dag responsible to schedule our data pipeline every 5 minutes.
