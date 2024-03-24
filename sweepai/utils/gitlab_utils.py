import requests
from loguru import logger


def create_gitlab_mr(token, project_id, source_branch, target_branch, title):
    url = f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"source_branch": source_branch, "target_branch": target_branch, "title": title}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        logger.info("Merge request created successfully.")
    else:
        logger.error(f"Failed to create merge request. Status code: {response.status_code}")
