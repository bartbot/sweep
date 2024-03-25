import gitlab


def get_gitlab_client(installation_id: int):
    # Assuming there's a mechanism to map installation_id to GitLab private tokens
    private_token = retrieve_gitlab_private_token(installation_id)
    gl = gitlab.Gitlab('https://gitlab.com', private_token=private_token)
    gl.auth()
    return gl

def retrieve_gitlab_private_token(installation_id: int) -> str:
    # Actual implementation for retrieving the GitLab private token
    # This function retrieves the GitLab private token based on the installation_id from an environment variable
    import os
    env_var_name = f"GITLAB_PRIVATE_TOKEN_{installation_id}"
    private_token = os.getenv(env_var_name)
    if not private_token:
        raise ValueError(f"GitLab private token for installation_id {installation_id} not found.")
    return private_token

def get_issues(project_id: int, client=None):
    if client is None:
        client = get_gitlab_client(installation_id=0)  # Default installation_id
    project = client.projects.get(project_id)
    issues = project.issues.list()
    return issues

def post_comment(issue_id: int, comment_body: str, project_id: int, client=None):
    if client is None:
        client = get_gitlab_client(installation_id=0)  # Default installation_id
    project = client.projects.get(project_id)
    issue = project.issues.get(issue_id)
    issue.notes.create({'body': comment_body})
