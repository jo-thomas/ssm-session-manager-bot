import os
import json
import boto3
import helpers
from helpers import get_logger
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = helpers.get_logger()

WEBHOOK_PARAM = os.environ.get('SLACK_WEBHOOK_PARAM', '/slack-bot-ssm/SlackWebhookURL')

def lambda_handler(event,context):
    logger.info(f"EVENT: {event}")
    session = boto3.session.Session()

    #Retrieve values from event
    eventName = event['detail']['eventName']
    accountId = event['detail']['userIdentity']['accountId']
    
    userIdentityType = event['detail']['userIdentity']['type']
    
    if userIdentityType == 'AssumedRole':
        userName = event['detail']['userIdentity']['sessionContext']['sessionIssuer']['userName']
    elif userIdentityType == 'IAMUser':
        userName = event['detail']['userIdentity']['userName']

    target = event['detail']['requestParameters']['target']
    sessionId = event['detail']['responseElements']['sessionId']
    logger.debug(f"VALUES FROM EVENT: eventName: {eventName}, accountId: {accountId}, userName: {userName}, sessionId: {sessionId} ")
    
    #Format for slack message
    slack_message = {
        'text' : f'*{eventName}* in Account: *{accountId}*\n'
                 f'Session: *{sessionId}* started by User: *{userName}*\n'
                 f'on Instance: *{target}*\n'
    }
    logger.debug(f"SLACK_MESSAGE: {slack_message}")
    
    #Get Webhook URL from ssm param
    ssm = session.client('ssm')
    webhook_url = ssm.get_parameter(Name=WEBHOOK_PARAM, WithDecryption=True)['Parameter']['Value']
    logger.debug(f"WEBHOOK_URL: {webhook_url}")

    #Send slack message to webhook, to post message to channel
    req = Request(webhook_url, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to Slack")
    except HTTPError as e:
        logger.debug(f'Request failed: {e.code} {e.reason}')
    except URLError as e:
        logger.debug(f'Server Connection failed:  {e.reason}')