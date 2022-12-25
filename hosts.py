import json
import logging
import os

import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

QUEUE_URL = os.getenv('QUEUE_URL')
BOTO_LIMIT = int(os.getenv('BOTO_LIMIT'))
SQS = boto3.client('sqs')


def producer(event, context):
    try:
        for record in event['Records']:
            print("test")
            payload = record["body"]
            create_file_message(payload)
        print("*********** END OF HOSTS FUNCTION ************")
    except Exception as e:
        message = str(e)
        logger.exception(f"Reading from SQS failed, with err: {message}")


def create_file_message(payload):

    data = json.loads(payload)
    key, secret, bucket = data["key"], data["secret"], data["bucket"]


    client = boto3.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id=key,
                        aws_secret_access_key=secret)

    list = client.list_objects_v2(Bucket=bucket, MaxKeys=BOTO_LIMIT)

    logger.info(list)

    for r in list["Contents"]:
        try:
            SQS.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({"key": r["Key"],
             "size": r["Size"],
             "lastMod": str(r["LastModified"])})
             )
        except Exception as e:
            logger.exception('Sending message to SQS queue failed!')
            message = str(e)

