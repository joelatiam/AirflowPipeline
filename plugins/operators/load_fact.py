from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    insert_sql = """
        INSERT INTO {}
        {}
    """

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 table="",
                 redshift_conn_id="",
                 select_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.table = table
        self.select_query = select_query
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        self.log.info('Start LoadFactOperator')

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from Staging table to Fact table")

        load_data_sql = LoadFactOperator.insert_sql.format(
            self.table,
            self.select_query
        )
        redshift.run(load_data_sql)
