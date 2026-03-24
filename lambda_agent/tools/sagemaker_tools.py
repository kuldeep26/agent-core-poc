import boto3

sm = boto3.client("sagemaker")

def restart_failed_pipelines():
    pipelines = sm.list_pipelines()["PipelineSummaries"]
    restarted = []

    for p in pipelines:
        executions = sm.list_pipeline_executions(
            PipelineName=p["PipelineName"]
        )["PipelineExecutionSummaries"]

        for exe in executions:
            if exe["PipelineExecutionStatus"] == "Failed":
                sm.start_pipeline_execution(
                    PipelineName=p["PipelineName"]
                )
                restarted.append(p["PipelineName"])

    return {"restarted": restarted}


def stop_idle_endpoints():
    endpoints = sm.list_endpoints()["Endpoints"]
    stopped = []

    for ep in endpoints:
        if ep["EndpointStatus"] == "InService":
            sm.delete_endpoint(EndpointName=ep["EndpointName"])
            stopped.append(ep["EndpointName"])

    return {"stopped": stopped}