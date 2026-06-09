import json
import os
import requests
from datetime import datetime

TOKEN = os.environ["CORP_GITHUB_TOKEN"]
USERNAME = os.environ["CORP_USERNAME"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

url = "https://api.github.com/user/events"

response = requests.get(url, headers=headers)
print("STATUS:", response.status_code)
print(response.text)
exit()
events = response.json()
print("TOTAL EVENTS:", len(events))

for event in events[:20]:
    print(
        event.get("id"),
        event.get("type"),
        event.get("created_at")
    )

with open("state.json", "r") as f:
    state = json.load(f)

last_event_id = state["last_event_id"]

new_pushes = []

for event in events:
    if event["type"] == "PushEvent":
        if str(event["id"]) == str(last_event_id):
            break
        new_pushes.append(event)

if new_pushes:

    state["last_event_id"] = new_pushes[0]["id"]
    state["work_commits_detected"] += len(new_pushes)

    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)

    with open("README.md", "w") as f:
        f.write(
f"""# Work Activity Tracker

Professional commits detected: {state['work_commits_detected']}

Last activity: {datetime.utcnow()}
"""
        )

    print("UPDATE_REQUIRED")
else:
    print("NO_CHANGES")