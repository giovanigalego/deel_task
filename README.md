📌 Deel Home Task
========

In this repository, you will find the solution to my task proposed by Deel. The main requirement was to develop a simple data system that alerts the team when there is a change greater than 50% in the client's balance.

🚀 Technologies
================
- Python 3.11
- Astronomer Airflow
- Snowflake
- Docker
- dbt-core

📂 Detailed Project Structure
- At folder dags/dbt/deel_home_task/ it will find the dbt project with the task solution will be found, also incorporating best practices with dbt, a connection to Snowflake, and the structure of a data pipeline.
- At folder dags/scripts, our dag will be responsible for scheduling our data pipeline daily.

🔍 Observations
  - Here's the [Snowflake Reader Account](https://dqhjjug-reader_home_task.snowflakecomputing.com) to query the task result and see the structure.
  - The credentials for Snowflake Reader Account will be sent by e-mail to Bibi.
  - stg_invoices and stg_organizations are materialized as table to be able to share with the Reader Account.
  - The function that can be called anytime to send email, it's a procedure in the main Snowflake account.
  - Snowflake email procedure code it's in the file: snowflake_script/email_alert_procure.py (This code only works in Snowflake because use the Snowflake Mailing System)
