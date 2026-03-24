import boto3

s3 = boto3.client("s3")
iam = boto3.client("iam")

def compliance_report():
    report = {}

    buckets = s3.list_buckets()["Buckets"]
    report["bucket_count"] = len(buckets)

    users = iam.list_users()["Users"]
    report["iam_users"] = len(users)

    return report