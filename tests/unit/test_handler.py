import json
import pytest

from src.alert_slack.helpers import get_logger, list_active_sessions

from src.alert_slack.alert_slack import lambda_handler
from src.revoke_session.revoke_session import lambda_handler

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "resource": "/revoke",
        "path": "/revoke",
        "httpMethod": "POST",
        "headers": {
            "Accept": "application/json,*/*",
            "Accept-Encoding": "gzip,deflate",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "gepknvj80g.execute-api.us-east-1.amazonaws.com",
            "User-Agent": "Slackbot 1.0 (+https://api.slack.com/robots)",
            "Via": "1.1 c396de17c1b5d58233088e40dd170cf5.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "ijLNyg2sNUehzaUFaaq7Z2jtxuTlUJiXRRSgio7e1gAi6JfahxT9sQ==",
            "X-Amzn-Trace-Id": "Root=1-60164c56-2de53e7a0a20a9e14b2e0e9f",
            "X-Forwarded-For": "34.232.63.141, 130.176.133.151",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
            "X-Slack-Request-Timestamp": "1612074070",
            "X-Slack-Signature": "v0=506cccdfc190e4f4e523f3dd829c7593b98335c621af60c1ff67aefd6908b86f"
        },
        "multiValueHeaders": {
            "Accept": [
                "application/json,*/*"
            ],
            "Accept-Encoding": [
                "gzip,deflate"
            ],
            "CloudFront-Forwarded-Proto": [
                "https"
            ],
            "CloudFront-Is-Desktop-Viewer": [
                "true"
            ],
            "CloudFront-Is-Mobile-Viewer": [
                "false"
            ],
            "CloudFront-Is-SmartTV-Viewer": [
                "false"
            ],
            "CloudFront-Is-Tablet-Viewer": [
                "false"
            ],
            "CloudFront-Viewer-Country": [
                "US"
            ],
            "Content-Type": [
                "application/x-www-form-urlencoded"
            ],
            "Host": [
                "gepknvj80g.execute-api.us-east-1.amazonaws.com"
            ],
            "User-Agent": [
                "Slackbot 1.0 (+https://api.slack.com/robots)"
            ],
            "Via": [
                "1.1 c396de17c1b5d58233088e40dd170cf5.cloudfront.net (CloudFront)"
            ],
            "X-Amz-Cf-Id": [
                "ijLNyg2sNUehzaUFaaq7Z2jtxuTlUJiXRRSgio7e1gAi6JfahxT9sQ=="
            ],
            "X-Amzn-Trace-Id": [
                "Root=1-60164c56-2de53e7a0a20a9e14b2e0e9f"
            ],
            "X-Forwarded-For": [
                "34.232.63.141, 130.176.133.151"
            ],
            "X-Forwarded-Port": [
                "443"
            ],
            "X-Forwarded-Proto": [
                "https"
            ],
            "X-Slack-Request-Timestamp": [
                "1612074070"
            ],
            "X-Slack-Signature": [
                "v0=506cccdfc190e4f4e523f3dd829c7593b98335c621af60c1ff67aefd6908b86f"
            ]
        },
        "queryStringParameters": "None",
        "multiValueQueryStringParameters": "None",
        "pathParameters": "None",
        "stageVariables": "None",
        "requestContext": {
            "resourceId": "ha6q28",
            "resourcePath": "/revoke",
            "httpMethod": "POST",
            "extendedRequestId": "aADdiE4vIAMFlJw=",
            "requestTime": "31/Jan/2021:06:21:10 +0000",
            "path": "/Prod/revoke",
            "accountId": "123456789012",
            "protocol": "HTTP/1.1",
            "stage": "Prod",
            "domainPrefix": "gepknvj80g",
            "requestTimeEpoch": 1612074070591,
            "requestId": "963310f0-4a79-40b1-a420-f531f6d597bf",
            "identity": {
                "cognitoIdentityPoolId": "None",
                "accountId": "None",
                "cognitoIdentityId": "None",
                "caller": "None",
                "sourceIp": "34.232.63.141",
                "principalOrgId": "None",
                "accessKey": "None",
                "cognitoAuthenticationType": "None",
                "cognitoAuthenticationProvider": "None",
                "userArn": "None",
                "userAgent": "Slackbot 1.0 (+https://api.slack.com/robots)",
                "user": "None"
            },
            "domainName": "gepknvj80g.execute-api.us-east-1.amazonaws.com",
            "apiId": "gepknvj80g"
        },
        "body": "token=1pHGkEVLZHecqtFODz7XG1XR&team_id=T01LL40M42Y&team_domain=thomas-workspacehq&channel_id=G01LAS5F405&channel_name=privategroup&user_id=U01LSHN8MJ5&user_name=thomasjoji91&command=%2Frevoke&text=test&api_app_id=A01LDUW3L02&is_enterprise_install=false&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT01LL40M42Y%2F1692376746133%2FztydsYP4DEUn0fahPyGOXPcB&trigger_id=1719305728704.1700136718100.b36aeb6d751d157cd766e078384cc051",
        "isBase64Encoded": "False"
    }

@pytest.fixture()
def eventbridge_event():
    """ Generates Event Bridge Event"""

    return {
        "version": "0",
        "id": "56df71a5-5044-0499-9867-488a1ca52cf4",
        "detail-type": "AWS API Call via CloudTrail",
        "source": "aws.ssm",
        "account": "123456789012",
        "time": "2021-01-31T02:31:47Z",
        "region": "us-east-1",
        "resources": [],
        "detail": {
            "eventVersion": "1.08",
            "userIdentity": {
            "type": "AssumedRole",
            "principalId": "AROAIQ6OLWNLBIR3TTEGG:jojithom",
            "arn": "arn:aws:sts::123456789012:assumed-role/Admin/jojithom",
            "accountId": "123456789012",
            "accessKeyId": "ASIAWWEJ5LNN6GCSI342",
            "sessionContext": {
                "sessionIssuer": {
                "type": "Role",
                "principalId": "AROAIQ6OLWNLBIR3TABCD",
                "arn": "arn:aws:iam::123456789012:role/Admin",
                "accountId": "123456789012",
                "userName": "Admin"
                },
                "webIdFederationData": {},
                "attributes": {
                "mfaAuthenticated": "false",
                "creationDate": "2021-01-31T02:23:51Z"
                }
            }
            },
            "eventTime": "2021-01-31T02:31:47Z",
            "eventSource": "ssm.amazonaws.com",
            "eventName": "StartSession",
            "awsRegion": "us-east-1",
            "sourceIPAddress": "72.21.198.64",
            "userAgent": "aws-internal/3 aws-sdk-java/1.11.937 Linux/4.9.230-0.1.ac.223.84.332.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.275-b01 java/1.8.0_275 vendor/Oracle_Corporation",
            "requestParameters": {
            "target": "i-023ad911b5d49dece"
            },
            "responseElements": {
            "sessionId": "jojithom-I-08ea7d78b1fd0d119",
            "tokenValue": "Value hidden due to security reasons.",
            "streamUrl": "wss://ssmmessages.us-east-1.amazonaws.com/v1/data-channel/jojithom-I-08ea7d78b1fd0d119?role=publish_subscribe"
            },
            "requestID": "fa579183-dd4c-4702-804f-140b2aa7014a",
            "eventID": "8217f18e-a892-42b6-91c8-1d42b571d440",
            "readOnly": false,
            "eventType": "AwsApiCall",
            "managementEvent": true,
            "eventCategory": "Management"
        }
    }

def test_alert_slack_lambda_handler(eventbridge_event, mocker):

    ret = revoke_session.lambda_handler(eventbridge_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    # assert "location" in data.dict_keys()

def test_revoke_session_lambda_handler(apigw_event, mocker):

    ret = revoke_session.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "Session: test is currently not active"
    # assert "location" in data.dict_keys()
