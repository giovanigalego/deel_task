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
- At folder dags/dbt/deel_home_task/ you will find the dbt project with the task solution, also incorporating best practices with dbt, a connection to Snowflake, and the structure of a data pipeline.
- At folder dags/scripts, our dag will be responsible for scheduling our data pipeline daily.

🔍 Observations
  - Here's the [Snowflake Reader Account](https://dqhjjug-reader_home_task.snowflakecomputing.com) to query the task result and see the structure.
  - The credentials for Snowflake Reader Account will be sent by e-mail to Bibi.
  - stg_invoices and stg_organizations are materialized as <b>table</b> to be able to share with the Reader Account.
  - The function that can be called anytime to send email, it's a procedure in the main Snowflake account.
  - Snowflake email procedure code it's in the file: <b>snowflake_script/email_alert_procure.py</b> (This code only works in Snowflake because use the Snowflake Mailing System)



💡 Explanation Fact_Financial
  - How to achieve the 50% balance difference over day and consider only new days. I assume that there was some invoice status to be disregarded so I changed it's value to 0 and normalized the data record.
  
  ![cte_normalized](https://github.com/user-attachments/assets/695b4ae0-cfda-4fc2-949a-4e08f0ca5e0b)
  - After that I made the Balance calculation following the logic: Balance = Total Amount - Invoice Amount.
  
  ![cte_balance](https://github.com/user-attachments/assets/da9f7ad5-cc3e-4ca0-8949-f033fcbb6cd6)
  - To finish I calculated the last day balance, to divide this value by the current day and created the "send_alert" column to be easier on the email alert.
  
  ![fact_last_block](https://github.com/user-attachments/assets/befce470-8dc9-47cb-913a-9a908c0636bc)



💡 Explanation Dim_Organizations
  - I realized that there were more Organizations_ID in the <b>invoice</b> table than the <b>organization</b> table (approximately 11k).
  - To fix this difference I did the following steps.
  - I created the first CTE to return the first day for each organization (this information will be necessary in the end).

  ![cte_orgs_invoice](https://github.com/user-attachments/assets/2378af94-b8f5-4647-8a00-6af739057c02)
  - The next CTE it's <b>payments_dates</b>, I realized that the <b>first_day_payment</b> it's the first invoice with <b>PAID</b> status, so I queried this information.
  
  ![cte_payment_dates](https://github.com/user-attachments/assets/b7036305-dc92-4dcb-a9ee-c94851f70b7d)
  - The <b>orgs_current_balace</b> returns an information to enhance the Dim_Organizations, it returns the current balance for each organization.
  
  ![cte_org_cur_balance](https://github.com/user-attachments/assets/bb72562c-75d3-4f9a-a787-07811433b0d0)
  - The final block I used left join to not lose any data and use the <b>created_at</b> column queried in the first CTE, to populate the same column at my Dim_Organization table.

  ![dim_org_final_block](https://github.com/user-attachments/assets/595e4011-75d4-4b2e-b4de-a929472fcefc)



💡 Explanation Airflow
  - For the scheduler I used astronomer-airflow and to run my dbt project, astronomer-cosmos.
  - The Airflow graph itself it's simple. I'm running my dbt project before my email alert that will run every day.

  ![airflow_graph](https://github.com/user-attachments/assets/9fbc2d4e-76fa-437c-b6aa-61a90866e921)

  - After the Dag run, it will send the email.

  ![email_report](https://github.com/user-attachments/assets/3fde6e3e-8ea5-4a74-bcb6-f372540250d3)




💡 Explanation Email Alert Procedure
  - Following the requirement to have a function that when called send an email to the business team, I created this procedure using Snowpark.

  ![snowpark_email_procedure](https://github.com/user-attachments/assets/acb4a5d9-9c73-4fbd-a310-f2e8bf3d20b6)

  - This procedure, when called, will send an email containing the same information as the email sent by Airflow.

  ![snowflake_report_procedure_email](https://github.com/user-attachments/assets/42def0c2-f336-4a87-bcea-75024fe484b9)


📊 Data Observability
  - To ensure the data reliability, monitoring, I'm using [Elementary](https://www.elementary-data.com/) package.
  - Here is the Elementary [Documentation](https://docs.elementary-data.com/introduction) as well.

  ![elementary_structure](https://github.com/user-attachments/assets/573fda91-1178-4124-8827-5f79ce6e82d5)
