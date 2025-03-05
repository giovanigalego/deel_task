import os
from datetime import datetime
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig, DbtTaskGroup
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from airflow.operators.bash import BashOperator
from pendulum import duration
from airflow.decorators import dag


DBT_PROJECT_PATH="/usr/local/airflow/dags/dbt/deel_home_task"
DBT_EXECUTABLE_PATH="/usr/local/airflow/dags/dbt/deel_home_task"
execution_config = ExecutionConfig(dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
)

profile_config = ProfileConfig(
    profile_name="deel_home_task",
    target_name="prod",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_conn", 
        profile_args={"database": "analytics", "schema": "trusted"},
    )
)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": duration(minutes=5),
}

@dag(
    start_date=datetime(2023, 8, 1),
    schedule='@daily',
    catchup=False,
    params={"params": 'params'},
)

def financials_alert():
    financials_alert = DbtTaskGroup(
        group_id="financials_alert",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        execution_config=execution_config,
        operator_args={
            "vars": '{"params": {{ params.params }} }',
        },
        default_args={"retries": 2},
    )

    send_email = BashOperator(
        task_id='send_email',
        bash_command='python /usr/local/airflow/dags/scripts/send_email.py',
    )

    financials_alert >> send_email


financials_alert()