import os
import sys
import json
import requests

MESSAGE_USERNAME = "Github Action"
MESSAGE_EMOJI = ":rocket:"
MESSAGE_FOOTER = (
    "By <https://github.com/yohanesgultom/notify-slack-action|notify-slack-action>"
)


def action_color(status):
    """
    Get a action color based on the workflow status.
    """

    if status == "success":
        return "good"
    elif status == "failure":
        return "danger"

    return "warning"


def action_status(status):
    """
    Get a transformed status based on the workflow status.
    """

    if status == "success":
        return "SUCCESS"
    elif status == "failure":
        return "FAILED"

    return "WARNING"


def action_emoji(status):
    """
    Get an emoji based on the workflow status.
    """

    if status == "success":
        return ":heavy_check_mark:"
    elif status == "failure":
        return ":x:"

    return ":zipper_mouth_face:"


def notify_slack(job_status, notify_when):
    """
    Send message by calling Slack webhook URL
    """
    url = os.getenv("SLACK_WEBHOOK_URL")
    workflow = os.getenv("GITHUB_WORKFLOW")
    repo = os.getenv("GITHUB_REPOSITORY")
    branch = os.getenv("GITHUB_REF")
    commit = os.getenv("GITHUB_SHA")
    author = os.getenv("GITHUB_ACTOR")
    commit_message = os.getenv("COMMIT_MESSAGE")

    commit_url = f"https://github.com/{repo}/commit/{commit}"
    repo_url = f"https://github.com/{repo}/tree/{branch}"

    color = action_color(job_status)
    status_message = action_status(job_status)
    emoji = action_emoji(job_status)

    pretext = f"<{repo_url}|{repo} ({branch})>"
    text = f"{emoji} {workflow}\n\n*"
    text += f"• Status*: {status_message}\n"
    text += f"• *Author*: {author}\n• *Commit*: <{commit_url}|{commit[:7]}>"
    fallback = f"{workflow} {status_message} {repo_url} by {author}"
    if commit_message:
        text += f"\n• *Message*: {commit_message}"

    payload = {
        "username": MESSAGE_USERNAME,
        "icon_emoji": MESSAGE_EMOJI,
        "attachments": [
            {
                "text": text,
                "fallback": fallback,
                "pretext": pretext,
                "color": color,
                "mrkdwn_in": ["text"],
                "footer": MESSAGE_FOOTER,
            }
        ],
    }

    payload = json.dumps(payload)

    headers = {"Content-Type": "application/json"}

    if notify_when is None:
        notify_when = "success,failure,warnings"

    if job_status in notify_when and not TESTING:
        requests.post(url, data=payload, headers=headers)


def main():
    """
    Main method
    """
    job_status = os.getenv("INPUT_STATUS")
    notify_when = os.getenv("INPUT_NOTIFY_WHEN")
    notify_slack(job_status, notify_when)


if __name__ == "__main__":
    try:
        TESTING = sys.argv[1] == "--test"
    except IndexError:
        TESTING = False

    main()
