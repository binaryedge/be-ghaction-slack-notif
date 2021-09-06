#!/usr/local/bin/python3

import os
import json
import urllib3
from datetime import datetime

slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
service_name = os.getenv("SERVICE_NAME")
branch = os.getenv("GITHUB_REF").rsplit("/", 1)[1]
workflow = os.getenv("GITHUB_WORKFLOW")
repository = os.getenv("GITHUB_REPOSITORY")
repository_owner = os.getenv("GITHUB_REPOSITORY_OWNER")
server_url = os.getenv("GITHUB_SERVER_URL")
event_type = os.getenv("GITHUB_EVENT_NAME")
event_path = os.getenv("GITHUB_EVENT_PATH")
sha = os.getenv("GITHUB_SHA")
actor = os.getenv("GITHUB_ACTOR")

message = {
    "text": f":rocket: Running *{workflow}* on *{repository}/{branch}* :rocket:",
    "attachments": [
        {
            "color": "warning",
            "fields": [ 
                {
                    "title": "Service Name",
                    "value": service_name,
                    "short": True
                },
                {
                    "title": "Repository/Branch",
                    "value": f"<{server_url}/{repository}/tree/{branch}|{repository}/{branch}>",
                    "short": True
                },
                {
                    "title": "Author",
                    "value": f"<{server_url}/{actor}|{actor}>",
                    "short": True
                },
                {
                    "title": "Event Type",
                    "value": event_type,
                    "short": True
                },
                {
                    "title": "Action URL",
                    "value": f"<{server_url}/{repository}/commit/{sha}/checks|{workflow}>",
                    "short": True
                },
                {
                    "title": "Commit",
                    "value": f"<{server_url}/{repository}/commit/{sha}|{sha[0:6]}>",
                    "short": True
                },
                {
                    "title": "Commit Message",
                    "value": '```' + json.load(open(event_path))["commits"][-1]["message"] + '```',
                    "short": False
                }
            ],
            "footer": server_url.replace("https://", "") + "/" + repository_owner,
            "footer_icon": server_url + "/" + repository_owner + ".png?size=32",
            "ts": datetime.now().timestamp()
        }
    ]
}

pool = urllib3.PoolManager()
try:
    pool.request(
        "POST",
        slack_webhook_url,
        body=json.dumps(message).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
except urllib3.exceptions.HTTPError:
    pass
