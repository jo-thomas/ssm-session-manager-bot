import os
import json
import boto3
import helpers
from helpers import get_logger, list_active_sessions
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import parse_qs

logger = helpers.get_logger()

WEBHOOK_PARAM = os.environ.get('SLACK_WEBHOOK_PARAM', '/slack-bot-ssm/SlackWebhookURL')

def lambda_handler(event, context):
    logger.info(f"EVENT: {event}")
    session = boto3.session.Session()
    
    #Grab values from query string in event
    query_string = parse_qs(event['body'])
    logger.debug(f"QUERY_STRING: {query_string}")

    #Retrieve values from query_string
    session_id = ''.join(query_string['text']).replace('*','')
    user_name = ''.join(query_string['user_name'])
    logger.debug(f"SESSION_ID: {session_id}, USER_NAME: {user_name}")

    #Get a list of active SSM sessions 
    ssm = session.client('ssm')
    ssm_sessions = helpers.list_active_sessions(session)
    
    #If the session passed in from the event is active
    if(session_id in ssm_sessions):
        #revoke session
        terminate_resonse = ssm.terminate_session(SessionId=session_id)
        result = terminate_resonse['SessionId']
        logger.debug(f"TERMINATED_SESSION: {result}")
        
        #Format for slack message
        slack_message = {
            'text' : f'<@{user_name}> revoked Session: *{result}*\n'
        }

        #Get Webhook URL from ssm param
        webhook_url = ssm.get_parameter(Name=WEBHOOK_PARAM, WithDecryption=True)['Parameter']['Value']
        logger.debug(f"WEBHOOK_URL: {webhook_url}")

        #Send slack message to webhook, to post message to channel
        req = Request(webhook_url,json.dumps(slack_message).encode('utf-8'))
        try:
            response = urlopen(req)
            response.read()
            logger.info(f"Sucessfully sent message")
            logger.debug(f"Sent message to WEBHOOK_URL: {webhook_url}")
            body_text = f"Terminated *{result}*"
        except HTTPError as e:
            body_text = f"Request failed: {e.code} {e.reason}'"
        except URLError as e:
            body_text = f"Request failed: {e.reason}'"
    else:
        body_text = f"Session: *{session_id}* is currently not active"
    
    #Send message back to caller
    message = dict(statusCode=200,
                 isBase64Encoded=False,
                 headers={"Content-Type": "application/json"},
                 body=body_text)
                 
    return message