import os
import boto3
import base64
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

def get_logger():
    import logging

    LOGLEVEL = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
    level = logging.getLevelName(LOGLEVEL)

    logger = logging.getLogger()
    logger.setLevel(level)
    logging.getLogger('boto3').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    return logger

def list_active_sessions(session):
    ssm_client = session.client('ssm')
    paginator = ssm_client.get_paginator('describe_sessions')
    response_iterator = paginator.paginate(
        State = 'Active'
    )
    ssm_sessions = []
    for page in response_iterator:
        for session in page['Sessions']:
            ssm_sessions.append(session['SessionId'])

    return ssm_sessions