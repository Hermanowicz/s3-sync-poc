import json
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

QUEUE_URL = os.getenv('QUEUE_URL')
SQS = boto3.client('sqs')


def producer(event, context):
    try:
        SQS.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({"key": "DO00G7CBN6N2HG9CTDXY","secret": "ULXScFVVPb6/DKONzzoMcekE3oLzcPSPumUiZsUT4tI" , "bucket": "s3-sync-target"}),
        )
    except Exception as e:
        logger.exception('Sending message to SQS queue failed!')
        message = str(e)
