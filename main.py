import base64
import json
from dateutil.parser import parse
from webhook import post_webhook


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(pubsub_message)
    status = 'Status'
    if 'status' in message:
        status = message['status'].title()
    log_message = ''
    if 'id' in message:
        log_message += f'\n**Build ID:** {message["id"][:8]}'
    if 'createTime' in message:
        created = parse(message["createTime"])
        timestamp = message["createTime"]
        color = 35071
        log_message += f'\n**Created:** {created.date()} {created.time()} UTC'
    if 'startTime' in message:
        started = parse(message["startTime"])
        timestamp = message["startTime"]
        color = 16772608
        log_message += f'\n**Started:** {started.date()} {started.time()} UTC'
    if 'finishTime' in message:
        finished = parse(message["finishTime"])
        timestamp = message["finishTime"]
        log_message += f'\n**Finished:** {finished.date()} {finished.time()} UTC'
        color = 65297
    if 'sourceProvenance' in message:
        if 'resolvedRepoSource' in message['sourceProvenance']:
            if 'commitSha' in message['sourceProvenance']['resolvedRepoSource']:
                log_message += f"\n**Git commit**: {message['sourceProvenance']['resolvedRepoSource']['commitSha'][:7]}"
    if 'logUrl' in message:
        log_message += f'\n[Stackdriver log]({message["logUrl"]})'
    post_webhook(message=log_message, timestamp=timestamp, title=status)
