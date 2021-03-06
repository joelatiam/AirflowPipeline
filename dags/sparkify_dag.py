
import configparser
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

S3_BUCKET = 'udacity-dend'
S3_LOGS_PATH = 'log_data'
S3_LOG_JSONPATH='log_json_path.json'
S3_SONGS_PATH = 'song_data'

default_args = {
    'owner': 'joelatiam',
    'start_date': datetime(2021, 5, 3),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('sparkify_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

records_to_check = []

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_events',
    s3_bucket=S3_BUCKET,
    s3_key=S3_LOGS_PATH,
    s3_json_format=S3_LOG_JSONPATH,
    dag=dag
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    table='staging_songs',
    s3_bucket=S3_BUCKET,
    s3_key=S3_SONGS_PATH,
    dag=dag
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    redshift_conn_id='redshift',
    table='songplays',
    select_query = SqlQueries.songplay_table_insert,
    append_data = False,
    dag=dag
)

records_to_check.append({
    'table_name': 'songplays',
    'min_records': 1,
    'not_null_columns': ['playid']
})

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    redshift_conn_id='redshift',
    table='users',
    select_query = SqlQueries.user_table_insert,
    append_data = False,
    dag=dag
)

records_to_check.append({
    'table_name': 'users',
    'min_records': 1,
    'not_null_columns': ['userid']
})

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    redshift_conn_id='redshift',
    table='songs',
    select_query = SqlQueries.song_table_insert,
    append_data = False,
    dag=dag
)

records_to_check.append({
    'table_name': 'songs',
    'min_records': 1,
    'not_null_columns': ['songid', 'title']
})

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    redshift_conn_id='redshift',
    table='artists',
    select_query = SqlQueries.artist_table_insert,
    dag=dag
)

records_to_check.append({
    'table_name': 'artists',
    'min_records': 1,
    'not_null_columns': ['artistid', 'name']
})

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    redshift_conn_id='redshift',
    table='time',
    select_query = SqlQueries.time_table_insert,
    append_data = False,
    dag=dag
)

records_to_check.append({
    'table_name': 'time',
    'min_records': 1,
    'not_null_columns': ['start_time']
})

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    redshift_conn_id='redshift',
    tables_list = records_to_check,
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> stage_events_to_redshift >> load_songplays_table
start_operator >> stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> load_user_dimension_table >> run_quality_checks
load_songplays_table >> load_song_dimension_table >> run_quality_checks
load_songplays_table >> load_artist_dimension_table >> run_quality_checks
load_songplays_table >> load_time_dimension_table >> run_quality_checks

run_quality_checks >> end_operator
