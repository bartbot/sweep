<<<<<<< sweep/replace_comment_handling_for_prs_with_gi
import gitlab


class GitLabAPIError(Exception):
    pass

def get_gitlab_client(token: str):
    try:
        gl = gitlab.Gitlab('https://gitlab.com', private_token=token)
        gl.auth()
        return gl
    except gitlab.GitlabAuthenticationError:
        raise GitLabAPIError("Authentication with GitLab failed.")
    except gitlab.GitlabError as e:
        raise GitLabAPIError(f"GitLab API error: {e}")

def get_mr_comments(project_id: str, mr_id: int):
    try:
        gl = get_gitlab_client(token="your_private_token_here")
        project = gl.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)
        discussions = mr.discussions.list()
        comments = [comment for discussion in discussions for note in discussion.attributes['notes'] for comment in note['body']]
        return comments
    except gitlab.GitlabGetError:
        raise GitLabAPIError("Failed to fetch the specified project or MR.")
    except gitlab.GitlabError as e:
        raise GitLabAPIError(f"GitLab API error: {e}")

def get_mr_details(project_id: str, mr_id: int, token: str):
    """Fetch details of a specific MR.

    Args:
        project_id (str): The ID of the project.
        mr_id (int): The ID of the merge request.
        token (str): The GitLab private token.

    Returns:
        dict: A dictionary containing MR details such as the MR's branch and other relevant information.
    """
    try:
        gl = get_gitlab_client(token=token)
        project = gl.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)
        return {
            'id': mr.id,
            'title': mr.title,
            'description': mr.description,
            'source_branch': mr.source_branch,
            'target_branch': mr.target_branch,
            'state': mr.state,
            'created_at': mr.created_at,
            'updated_at': mr.updated_at,
        }
    except gitlab.GitlabGetError:
        raise GitLabAPIError("Failed to fetch the specified project or MR.")
    except gitlab.GitlabError as e:
        raise GitLabAPIError(f"GitLab API error: {e}")

def post_mr_comment(project_id: str, mr_id: int, comment: str, token: str):
    """Post a comment on a specific MR.

    Args:
        project_id (str): The ID of the project.
        mr_id (int): The ID of the merge request.
        comment (str): The comment to post.
        token (str): The GitLab private token.
    """
    try:
        gl = get_gitlab_client(token="your_private_token_here")
        project = gl.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)
        mr.discussions.create({'body': comment})
    except gitlab.GitlabCreateError:
        raise GitLabAPIError("Failed to post comment to the specified MR.")
    except gitlab.GitlabError as e:
        raise GitLabAPIError(f"GitLab API error: {e}")
=======
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
>>>>>>> main
