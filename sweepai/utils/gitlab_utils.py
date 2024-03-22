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

def post_mr_comment(project_id: str, mr_id: int, comment: str):
    try:
        gl = get_gitlab_client(token="your_private_token_here")
        project = gl.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)
        mr.discussions.create({'body': comment})
    except gitlab.GitlabCreateError:
        raise GitLabAPIError("Failed to post comment to the specified MR.")
    except gitlab.GitlabError as e:
        raise GitLabAPIError(f"GitLab API error: {e}")
