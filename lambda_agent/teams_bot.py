import json
import boto3
import os
import requests

bedrock_agent = boto3.client("bedrock-agent-runtime")

AGENT_ID = os.environ.get("AGENT_ID")
AGENT_ALIAS_ID = os.environ.get("AGENT_ALIAS_ID")
TEAMS_WEBHOOK = os.environ.get("TEAMS_WEBHOOK")


def send_to_teams(message):
    payload = {"text": message}
    requests.post(TEAMS_WEBHOOK, json=payload)


def lambda_handler(event, context):

    # Message coming from API Gateway / Teams
    if "body" in event:
        body = json.loads(event["body"])
        user_message = body.get("message")
    else:
        user_message = event.get("message")

    if not user_message:
        return {"statusCode": 400, "body": "No message provided"}

    # Invoke Bedrock Agent
    response = bedrock_agent.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId="teams-session",
        inputText=user_message
    )

    completion = ""

    for event in response.get("completion", []):
        if "chunk" in event:
            completion += event["chunk"]["bytes"].decode()

    # Send response back to Teams
    send_to_teams(completion)

    return {
        "statusCode": 200,
        "body": json.dumps({"response": completion})
    }