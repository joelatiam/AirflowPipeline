# Sparkify's DATA PIPELINE with Airflow, AWS  S3 & Redshift

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow..

>The source data resides in **S3** and needs to be processed in Sparkify's data warehouse in **Amazon Redshift**. The source datasets consist of **JSON logs** that tell about user activity in the application and **JSON metadata** about the songs the users listen to.

### Technologies/Tools

Following are different technologies used in this project :

* [Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html) - A fully managed, petabyte-scale data warehouse service in the cloud
* [Apache Airflow](https://airflow.apache.org/) - Airflow is a platform created by the community to programmatically author, schedule and monitor workflows
* [Apache Airflow (Postgres Extension) ](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html) - Airflow Extension for Postgres Connection **(Used as well for Redshift)**
* [Apache Airflow (Amazon Extension)](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/index.html) - Airflow Extension for AWS
* [Python 3](https://www.python.org/) - Awesome programming language, easy to learn and with awesome data science libraries and communities
* [psycopg2 binary](https://www.psycopg.org/) - Popular PostgreSQL database adapter for the Python programming language
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services
*  [watchtower](https://pypi.org/project/watchtower/) - Watchtower is a log handler for Amazon Web Services CloudWatch Logs.

### Usage
This app requires the technologies mentioned above to run.

```sh
$ #cd to the project home directory/folder
$ pip3 install -r requirements.txt
$ airflow scheduler
$ airflow webserver
```

### Directory(Folder) Structure

| File/Folder | Description |
| ------ | ------ |
| dags/| Folder to contain DAG files. |
| dags/sparkify_dag.py | A module where the Dag is defined and all the tasks |
| plugins/helpers/ | Folder containing SQL queries helpers  |
| plugins/operators | Folder containing our custom Airflow Operators |
| create_tables.sql | SQL Scripts for our Redshift Tables |
| requirements.txt | File containing Python Packages used in this project |
| README.md | Information about the project    |


### Database Schema

#### Staging Tables
-  **staging_events**

| Column | Datatype | Constrainct | Description |
| ------ | ------ |------ | ------ |
| artist | varchar(256) | |  |
| auth | varchar(256) | |  |
| firstname | varchar(256) | |  |
| gender | varchar(256) | |  |
| iteminsession | int4 | |  |
| lastname | varchar(256) | |  |
| length | numeric(18,0) | |  |
| level | varchar(256) | |  |
| location | varchar(256) | |  |
| method | varchar(256) | |  |
| page | varchar(256) | |  |
| registration | numeric(18,0) | |  |
| sessionid |int4 | |  |
| song | varchar(256) | |  |
| status | int4 | |  |
| ts | int8 | |  |
| useragent | varchar(256) | |  |
| userid | int4 | |  |

-  **staging_songs**

| Column | Datatype | Constrainct | Description |
| ------ | ------ |------ | ------ |
| num_songs | int4 | |  |
| artist_id | archar(256) | |  |
| artist_latitude | numeric(18,0 | |  |
| artist_longitude | numeric(18,0 | |  |
| artist_location | varchar(256) | |  |
| artist_name | varchar(256) | |  |
| song_id | varchar(256) | |  |
| title | varchar(256) | |  |
| duration | numeric(18,0) | |  |
| year | int4 | |  |

#### Final Tables

##### Dimension Tables
-  **users**

| Column | Datatype | Constrainct | Description |
| ------ | ------ |------ | ------ |
| userid | int4 |PRIMARY KEY | This is a unique key representing each user and we opted for an BIGINT type because we are able to extract as a non decimal number format from the log file and as the number of user grows, BIGINT will be the right  Datatype|
| first_name | varchar(256) | |  |
| last_name | varchar(256) | |  |
| gender | varchar(256)) | |  |
| level | varchar(256) | |  |

-  **songs**

| Column | Datatype | Constrainct | Description |
| ------ | ------ |------ | ------ |
| songid | varchar(256) |PRIMARY KEY | This is a unique key representing each song and we opted for a varchar type because we are receiving the song ID as a string of different alphabetic characters from the song metadata |
| title | varchar(256) | NOT NULL|  |
| artist_id | varchar(256) | distkey |  |
| year | int4 | |  |
| duration | numeric(18,0) | |  |

-  **artists**

| Column | Datatype | Constrainct | Description |
| ------ | ------ |------ | ------ |
| artistid | varchar(256) |NOT NULL| |
| name | varchar(256) | |  |
| location | varchar(256) | | |
| latitude | numeric(18,0) | |  |
| longitude | numeric(18,0) | |  |

-  **time**

| Column | Datatype | Constrainct | Description |
| ------ | ------ |------ | ------ |
| start_time | timestamp |PRIMARY KEY | This is a  key representing each recorded time in postgres timestamp format wich is YYYY-MM-DD hh:mm:ss... |
| hour | int4 | |  |
| day | int4 | | |
| week | int4 | |  |
| month | varchar(256) | |  |
| year | int4 | |  |
| weekday | varchar(256) | |  |

##### Fact Tables
-  **songplays**

| Column | Datatype | Constrainct | Description |
| ------ | ------ |------ | ------ |
| playid | varchar(32) | PRIMARY KEY  | |
| start_time | timestamp | NOT NULL |  |
| userid | int4 | |  |
| level | varchar(256) | | |
| song_id | varchar(256) | | |
| artist_id | varchar(256) || |
| session_id | int4 | |  |
| location | varchar(256) | |  |
| user_agent | varchar(256) | |  |


### Contributors
**Joël Atiamutu** *[github](https://github.com/joelatiam)  [gitlab](https://gitlab.com/joelatiam)*

### Credits
[Udacity Data Engineering Programs](https://www.udacity.com/course/data-engineer-nanodegree--nd027) 
