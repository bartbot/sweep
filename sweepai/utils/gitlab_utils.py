
import datetime
import os
import shutil
import subprocess
from dataclasses import dataclass
from functools import cached_property
from time import time
from typing import Any

import gitlab
import requests
from sweepai.config.client import SweepConfig
from sweepai.logn import logger
from sweepai.utils.ctags import CTags
from sweepai.utils.github_utils import git
from sweepai.utils.str_utils import hashlib
from sweepai.utils.tree_utils import DirectoryTree

REPO_CACHE_BASE_DIR = "/tmp/cache/repos"

def get_gitlab_token(private_token: str):
    return private_token

def get_gitlab_client(oauth_token: str):
    gl = gitlab.Gitlab('https://gitlab.com', oauth_token=oauth_token, oauth_token=oauth_token)
    gl.auth()
    return gl

@dataclass
class ClonedRepoGitlab:
    repo_full_name: str
    installation_id: str
    branch: str | None = None
    token: str | None = None
    repo: Any | None = None
    git_repo: Any | None = None
    ssh_url_to_repo: str | None = None

    def __post_init__(self):
        self.token = self.token or os.environ["GITLAB_PRIVATE_TOKEN"]
        self.gl = get_gitlab_client(self.token)
        self.repo = self.gl.projects.get(self.repo_full_name)
        self.branch = self.branch or SweepConfig.get_branch(self.repo)
        self.ssh_url_to_repo = self.repo.ssh_url_to_repo
        self.clone()

    @cached_property
    def cached_dir(self):
        return os.path.join(
            REPO_CACHE_BASE_DIR,
            self.repo_full_name,
            "base",
            self.branch.replace('/', '_')
        )

    @cached_property
    def repo_dir(self):
        curr_time_str = str(time.time()).encode("utf-8")
        hash_obj = hashlib.sha256(curr_time_str)
        hash_hex = hash_obj.hexdigest()
        return os.path.join(REPO_CACHE_BASE_DIR, self.repo_full_name, hash_hex, self.branch.replace('/', '_'))

    def clone(self):
        if not os.path.exists(self.cached_dir):
            logger.info("Cloning repo using git command...")
            clone_cmd = ['git', 'clone', self.ssh_url_to_repo, self.cached_dir]
            if self.branch:
                clone_cmd.extend(['--branch', self.branch])
            subprocess.run(clone_cmd, check=True)
            logger.info("Done cloning")
            self.git_repo = git.Repo(self.cached_dir)
        else:
            logger.info("Repo already cached, pulling updates")
            self.git_repo = git.Repo(self.cached_dir)
            self.git_repo.remotes.origin.pull()

    def get_file_contents(self, file_path, ref=None):
        local_path = os.path.join(self.repo_dir, file_path)
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                contents = f.read()
            return contents
        else:
            raise FileNotFoundError(f"{local_path} does not exist.")

    def get_commit_history(self, username: str = "", limit: int = 200, time_limited: bool = True):
        commit_history = []
        commits = self.repo.commits.list(author=username, all=True)
        for commit in commits[:limit]:
            commit_detail = self.repo.commits.get(commit.id)
            commit_history.append(commit_detail)
        return commit_history

    # Additional methods like get_file_list, list_directory_tree, get_tree_and_file_list, and get_similar_file_paths would be implemented here following the same pattern as in ClonedRepo.
    def get_file_list(self):
        file_list = []
        for root, dirs, files in os.walk(self.repo_dir):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list
    def list_directory_tree(self):
        tree = DirectoryTree(self.repo_dir)
        return tree
    def get_tree_and_file_list(self):
        tree = self.list_directory_tree()
        file_list = self.get_file_list()
        return tree, file_list
    def get_similar_file_paths(self, file_path):
        similar_file_paths = []
        for root, dirs, files in os.walk(self.repo_dir):
            for file in files:
                if file_path in os.path.join(root, file):
                    similar_file_paths.append(os.path.join(root, file))
        return similar_file_paths



def get_mr_comments(project_id: str, mr_id: int):
    try:
        gl = get_gitlab_client(oauth_token="your_oauth_token_here")
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
        gl = get_gitlab_client(oauth_token=token)
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
        gl = get_gitlab_client(oauth_token="your_oauth_token_here")
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

