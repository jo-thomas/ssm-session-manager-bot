import os
import boto3
import base64
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

def get_logger():
    #return: logger object with logging level set

    import logging

    #Get logging level from environment variable
    LOGLEVEL = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
    level = logging.getLevelName(LOGLEVEL)

    logger = logging.getLogger()
    logger.setLevel(level)
    #Mute verbose boto3 and request library logging
    logging.getLogger('boto3').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    return logger

def list_active_sessions(session):
    #param session: boto3 session object
    #return: list of active ssm sessions

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