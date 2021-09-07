# be-ghaction-slack-notif

Github Action to deliver notifications to a slack channel, based on a repository event.

Environment Variables:
- SLACK_WEBHOOK_URL (required): Webhook URL of the Slack Channel to send the notifications to.
- SERVICE_NAME (optional): Name of the service to display (useful when repository names aren't completely descriptive).
