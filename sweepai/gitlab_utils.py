import os

import requests

GITLAB_API_BASE_URL = "https://gitlab.com/api/v4"
GITLAB_APP_ID = os.environ.get("GITLAB_APP_ID")

def get_gitlab_issue(project_id, issue_id):
    url = f"{GITLAB_API_BASE_URL}/projects/{project_id}/issues/{issue_id}"
    headers = {"Private-Token": GITLAB_APP_ID}
    response = requests.get(url, headers=headers)
    return response.json()

def create_gitlab_merge_request(project_id, source_branch, target_branch, title):
    url = f"{GITLAB_API_BASE_URL}/projects/{project_id}/merge_requests"
    headers = {"Private-Token": GITLAB_APP_ID}
    data = {
        "source_branch": source_branch,
        "target_branch": target_branch,
        "title": title,
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def update_gitlab_pipeline(project_id, pipeline_id, data):
    url = f"{GITLAB_API_BASE_URL}/projects/{project_id}/pipelines/{pipeline_id}"
    headers = {"Private-Token": GITLAB_APP_ID}
    response = requests.put(url, headers=headers, data=data)
    return response.json()
