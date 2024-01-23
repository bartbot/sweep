import datetime
import os
import shutil
import subprocess
from dataclasses import dataclass
from functools import cached_property
from time import time
from typing import Any

import gitlab

from sweepai.config.client import SweepConfig
from sweepai.logn import logger
from sweepai.utils.ctags import CTags
from sweepai.utils.github_utils import git
from sweepai.utils.str_utils import hashlib
from sweepai.utils.tree_utils import DirectoryTree

REPO_CACHE_BASE_DIR = "/tmp/cache/repos"

def get_gitlab_token(private_token: str):
    return private_token

def get_gitlab_client(private_token: str):
    gl = gitlab.Gitlab('https://gitlab.com', private_token=private_token)
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

# Unit tests for ClonedRepoGitlab would be implemented here.
