# gcf-build-discord.py

"Google Cloud Function to send Google Cloud Build alerts to Discord via webhook"

import base64
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

import requests
from dateutil.parser import parse


def hello_pubsub(event: dict, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(pubsub_message)
    status = "Status"
    color = 0
    timestamp = datetime.now(timezone.utc).isoformat()
    if "status" in message:
        status = message["status"].title()
    log_message = ""
    if "id" in message:
        log_message += f'\n**Build ID:** {message["id"][:8]}'
    if "createTime" in message:
        created = parse(message["createTime"])
        timestamp = message["createTime"]
        color = 35071
        log_message += f"\n**Created:** <t:{created.timestamp()}>"
    if "startTime" in message:
        started = parse(message["startTime"])
        timestamp = message["startTime"]
        color = 16772608
        log_message += f"\n**Started:** <t:{started.timestamp()}>"
    if "finishTime" in message:
        finished = parse(message["finishTime"])
        timestamp = message["finishTime"]
        log_message += f"\n**Finished:** <t:{finished.timestamp()}>"
        color = 65297
    if "sourceProvenance" in message:
        if "resolvedRepoSource" in message["sourceProvenance"]:
            if "commitSha" in message["sourceProvenance"]["resolvedRepoSource"]:
                log_message += f"\n**Git commit**: {message['sourceProvenance']['resolvedRepoSource']['commitSha'][:7]}"
    if "logUrl" in message:
        log_message += f'\n[Stackdriver log]({message["logUrl"]})'
    post_webhook(message=log_message, timestamp=timestamp, title=status, color=color)


def post_webhook(
    message: str,
    timestamp: str,
    title: Optional[str] = "Status",
    color: Optional[int] = 0,
):
    """Post webhook to Discord
    Set an environment variable for 'WEBHOOK' to point to the URI for your channel

    Attributes
        message (str): The message to put in the embed
        timestamp (str): ISO 8601 timestamp of the event
        title (str): Stats of the build process for the embed title.  Defaults to 'Status'
        color (int): Color to use for embed highlight. Defaults to black
    Returns
        result (requests.result): Result of Requests post
    """
    url = os.environ.get("WEBHOOK")
    if not url:
        raise ValueError("No WEBHOOK env variable set")
    data: dict[str, Any] = {}
    data["embeds"] = []
    embed: dict[str, Any] = {}
    embed["title"] = f"Cloud Build {title}"
    embed["description"] = message
    embed["footer"] = {}
    embed["footer"]["text"] = f"{title}"
    embed["timestamp"] = timestamp
    embed["color"] = color
    data["embeds"].append(embed)
    result = requests.post(
        url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    return result
