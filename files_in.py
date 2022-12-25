import json
import logging
import os

import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUEUE_URL = os.getenv('QUEUE_URL')
SQS = boto3.client('sqs')


def consumer(event, context):

    try:
        for record in event['Records']:
            logger.info(f'Message body: {record["body"]}')
            data = json.loads(record["body"])
            file_id = data["key"]
            save_file(file_id)
            delete_file(file_id)
    except Exception as e:
        message = str(e)
        logger.exception(f"reading from SQS failed, with err: {message}")


def save_file(file_id):
    try:
        client = boto3.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id="DO00G7CBN6N2HG9CTDXY",
                        aws_secret_access_key="ULXScFVVPb6/DKONzzoMcekE3oLzcPSPumUiZsUT4tI")

        res = client.download_file("s3-sync-target",
                        f"{file_id}",
                        f"/mnt/ingest/{file_id}")
        logger.info(res)
    except Exception as e:
        logger.error(f"Failed to download file, with error: {str(e)}")


def delete_file(file_id):
    try:
        client = boto3.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id="DO00G7CBN6N2HG9CTDXY",
                        aws_secret_access_key="ULXScFVVPb6/DKONzzoMcekE3oLzcPSPumUiZsUT4tI")

        res = client.delete_object(Bucket="s3-sync-target",
                        Key=f"{file_id}")
        logger.info(res)
    except Exception as e:
        logger.error(f"Failed to delete file, with error: {str(e)}")

