import json
import logging
import os

import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def producer(event, context):

    try:
        to_copy = os.popen("ls -l /mnt/ingest/out_dir").readlines()
        for line in to_copy:
            file_id = line.split()[-1]
            upload_file(file_id)
            delete_file(file_id)
    except Exception as e:
        logger.error(f"Upload to S3 failed with error: {str(e)}")


def upload_file(file_id):
    try:
        client = boto3.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id="DO00G7CBN6N2HG9CTDXY",
                        aws_secret_access_key="ULXScFVVPb6/DKONzzoMcekE3oLzcPSPumUiZsUT4tI")

        res = client.upload_file(f"out/{file_id}",
                        "s3-sync-target"
                        f"/mnt/ingest/out_dir/{file_id}")
        logger.info(res)
    except Exception as e:
        logger.error(f"Failed to upload file, with error: {str(e)}")


def delete_file(file_id):
    try:
        os.remove(f"/mnt/ingest/out_dir{file_id}")
    except Exception as e:
        logger.error(f"Failed to delete file, with error: {str(e)}")

