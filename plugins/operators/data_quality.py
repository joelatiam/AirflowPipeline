from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging

class DataQualityOperator(BaseOperator):
    """Check Data Quality Of Given Tables List"""

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 tables_list=[],
                 redshift_conn_id="",
                 *args, **kwargs):
        """
            Parameters:
            redshift_conn_id: "String"
            tables_list: List of Dictionaries with properties
                table_name: "String"
                min_records: Number
                not_null_columns: List of Strings
        """

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.tables_list = tables_list

    def execute(self, context):
        self.log.info('Start DataQualityOperator')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        error_messages = "Data quality check failed"
        
        for dict in self.tables_list:
            table = dict['table_name']
            task_name = f"Check for records in table {table}"
            min_records = 1

            if 'min_records' in dict:
                min_records = dict['min_records']

            self.log.info(task_name)

            records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")

            if len(records) >= 1 and len(records[0]) >= 1 :
                records_count = records[0][0]
                if records_count < min_records:
                    raise ValueError(
                        f"""
                        {error_messages}
                        for {task_name}
                        found ${records_count},
                        Expected a minimum of {min_records} records.
                        """
                        )
            else:
                raise ValueError(f"{error_messages}. No result for {task_name}")
            
            if 'not_null_columns' in dict:
                not_null_columns = dict['not_null_columns']

                for column in not_null_columns:
                    check_null_task_name = f"Check for null values in {table}.{column}"
                    self.log.info(check_null_task_name)
                    count_nulls = redshift.get_records(f"SELECT COUNT(*) FROM {table} WHERE {column} is null")
                    
                    if len(count_nulls) >= 1 and len(count_nulls[0]) >= 1 :
                        null_values = count_nulls[0][0]
                        if null_values > 0:
                            raise ValueError(
                                f"""
                                {error_messages}
                                for {check_null_task_name},
                                Found {null_values} null records in {table}.{column}.
                                """
                                )
                    else:
                        raise ValueError(f"{error_messages}. No result for {check_null_task_name}")



