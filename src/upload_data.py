"""
Created on 5/11/19

@author: ivan chen

"""
import argparse
import boto3
s3 = boto3.client("s3")

def upload_data(args):
    s3.upload_file(args.input_file_path,args.bucket_name,args.output_file_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to S3")

    # add argument
    parser.add_argument("--input_file_path", help="local path for uploaded file")
    parser.add_argument("--bucket_name", help="s3 bucket name")
    parser.add_argument("--output_file_path", help="output path for uploaded file")

    args = parser.parse_args()
    upload_data(args)

