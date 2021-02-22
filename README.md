# ssm-session-manager-bot

This project contains source code and supporting files for a SSM session manager bot. 
This project will configure a slack bot that:
* Alerts when a StartSession command is invoked on a EC2
* Provides a endpoint to Revoke a session based on id

## Initial Slack Bot setup

1. Create a **slack bot**, [tutorial](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace)

2. Create a **webhook** for the channel to associate with the bot, [tutorial](https://api.slack.com/messaging/webhooks)

3. Create a **slash command** called, /revoke  [tutorial](https://api.slack.com/interactivity/slash-commands)

## Initial AWS setup

1. Install AWS CLI, [tutorial](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)

2. Install AWS SAM CLI, [tutorial](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

3. Create a secure string SSM parameter for Webhook Url
```bash
aws ssm put-parameter --name "/slack-bot-ssm/SlackWebhookURL" --value "<PROVIDE WEBHOOK URL HERE>" --type "SecureString" --key-id alias/aws/ssm
```

## Deploy SSM Manager Bot

1. SAM Deploy
```bash
# Use sam guided deploy on the first run to ensure configurations are set properly
sam deploy --guided --template template.yaml

or 

#Use samconfig.toml file for a us-east-1 deployment
sam deploy samconfig.toml
```

2. Update slack app with RevokeSessionApi endpoint
* Navigate to cloudformation console and select "ssm-slackbot" stack
* View outputs and copy RevokeSessionApi value
* Update the Request Url on slash command /revoke to point to RevokeSessionApi
```bash
#CLI Command to get stack outputs
aws cloudformation describe-stacks --stack-name ssm-slackbot --query Stacks[].Outputs[].[OutputKey,OutputValue]
```

## Trigger SSM Manager Bot
**Note:** ec2 instances must setup to use session manager - [Session Manager Setup](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started.html)

1. Navigate to EC2 management console
2. Select Instance
3. Click Connect, Session Manager
4. Click Connect

The slack channel should receive a message
```bash
StartSession in Account: XXXXXXXXXXX
Session: test-user-076873a6149f50448 started by User: test-user
on Instance: i-0231234abcdefghij
```

Use the /revoke command and specify Session ID
```bash
/revoke test-user-076873a6149f50448
```

Example Response:
```bash
Terminated test-user-076873a6149f50448
```

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
ssm-session-manager-bot$ pip install -r tests/requirements.txt --user
# unit test
ssm-session-manager-bot$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
ssm-session-manager-bot$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

## Cleanup

To delete the ssm-manager-bot created, delete the stack from console or use aws cli.

```bash
aws cloudformation delete-stack --stack-name ssm-slackbot
```
