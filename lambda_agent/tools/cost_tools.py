import boto3
from datetime import date

ce = boto3.client("ce")

def monthly_cost():
    today = date.today()
    start = today.replace(day=1)

    cost = ce.get_cost_and_usage(
        TimePeriod={
            'Start': str(start),
            'End': str(today)
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )

    amount = cost["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    return {"monthly_cost": amount}