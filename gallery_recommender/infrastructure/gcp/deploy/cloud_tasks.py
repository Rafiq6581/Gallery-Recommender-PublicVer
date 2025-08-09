from google.cloud import tasks_v2
import json
from loguru import logger

import gallery_recommender.settings as settings

PROJECT_ID = settings.GCP_PROJECT_ID
LOCATION = settings.GCP_REGION
QUEUE = settings.CLOUD_TASK_QUEUE
CLOUD_RUN_URL = settings.CLOUD_RUN_TASK_HANDLER_URL

client = tasks_v2.CloudTasksClient()

def create_task(uid: str, payload: dict, create_report: bool = False):
    parent = client.queue_path(PROJECT_ID, LOCATION, QUEUE)

    body = {
        "uid": uid,
        "query": payload.get("query", {}),
        "create_report": create_report
        }

    logger.info(f"Task body: {body}")

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": f"{CLOUD_RUN_URL}/exhibition_reports",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body).encode(),
        }
    }

    response = client.create_task(request={"parent": parent, "task": task})
    return response.name


