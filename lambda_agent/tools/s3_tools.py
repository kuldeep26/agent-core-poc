import boto3

s3 = boto3.client("s3")

def check_public_buckets():
    buckets = s3.list_buckets()["Buckets"]
    public_buckets = []

    for bucket in buckets:
        try:
            acl = s3.get_bucket_acl(Bucket=bucket["Name"])
            for grant in acl["Grants"]:
                if "AllUsers" in str(grant):
                    public_buckets.append(bucket["Name"])
        except:
            pass

    return {"public_buckets": public_buckets}