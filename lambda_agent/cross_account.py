import boto3


def assume_role(account_id, role_name, region="ap-south-1"):
    sts_client = boto3.client("sts")

    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="agent-core-session"
    )

    credentials = response["Credentials"]

    session = boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name=region
    )

    return session


def get_s3_client(account_id, role_name):
    session = assume_role(account_id, role_name)
    return session.client("s3")


def get_sagemaker_client(account_id, role_name):
    session = assume_role(account_id, role_name)
    return session.client("sagemaker")


def get_iam_client(account_id, role_name):
    session = assume_role(account_id, role_name)
    return session.client("iam")