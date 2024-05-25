from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import create_engine
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from datetime import datetime,timedelta
import datetime

from airflow.utils.dates import days_ago
from extract_load import spotify_etl

default_args = {
    'owner':'Kaz',
    'start_date': datetime.datetime(2024,5,25),
    'retries': 5,
    'retry_delay':timedelta(minutes=1)
}

dag = DAG(
    'my_spotify_dag',
    default_args=default_args,
    schedule='@daily'
)

def ETL():
    print("started")
    df=spotify_etl()
    # Connect postgresql with python
    conn = BaseHook.get_connection('postgre_spotify_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql('my_listened_song', engine, if_exists='replace')

with dag:
    create_table = PostgresOperator(
        task_id = 'create_table_task',
        postgres_conn_id='postgre_spotify_sql',
        sql = """
                create table if not exists my_listened_song(
                    song_name varchar(50),
                    artis_name varchar(50),
                    album_name varchar(50),
                    release date,
                    played_at date,
                    CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
                )
                """
    )

    run_etl = PythonOperator(
        task_id = 'run_etl_task',
        python_callable=ETL,
        dag=dag 
    )

    create_table >> run_etl