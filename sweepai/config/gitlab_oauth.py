import os


class GitLabOAuthConfig:
    APP_ID = os.environ.get("GITLAB_APP_ID", "default_app_id")
    APP_SECRET = os.environ.get("GITLAB_APP_SECRET", "default_app_secret")
    REDIRECT_URI = os.environ.get("GITLAB_REDIRECT_URI", "http://localhost/oauth-redirect")
