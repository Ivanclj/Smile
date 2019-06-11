## Download data:  
src/load_my_data.py : this script download data from my GitHub repo to ../data/data1.csv

## Upload data:  
src/upload_data.py: upload data to target s3 bucket

Requirement: boto 3 installed and have configured aws environment. (Check if have ~/.aws/credential file and if have access key and secret key in the file)

Argument to be specified in bash:

--input_path: local file path.

--bucket_name: target bucket name

--output_path: output file path

## Create database in RDS/local:  
src/database.py: create table defined within script in either RDS or local based on argument

Requirement:
Have exported username, password, host and port for RDS as environment variables if want to use
RDS version.

Argument to be specified in bash:

--RDS: True to create in rds, default to create at local.

Note: there is a local logfile created by logger for information on the created table
