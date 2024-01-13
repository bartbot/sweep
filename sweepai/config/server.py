from sweepai.config.gitlab_oauth import GitLabOAuthConfig

import os

from dotenv import load_dotenv
from loguru import logger

logger.print = logger.info

load_dotenv(dotenv_path=".env")

os.environ["TRANSFORMERS_CACHE"] = os.environ.get(
    "TRANSFORMERS_CACHE", "/tmp/cache/model"
)  # vector_db.py
os.environ["TIKTOKEN_CACHE_DIR"] = os.environ.get(
    "TIKTOKEN_CACHE_DIR", "/tmp/cache/tiktoken"
)  # utils.py

SENTENCE_TRANSFORMERS_MODEL = os.environ.get(
    "SENTENCE_TRANSFORMERS_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",  # "all-mpnet-base-v2"
)
BATCH_SIZE = int(
    os.environ.get("BATCH_SIZE", 32)
)  # Tune this to 32 for sentence-transformers/all-MiniLM-L6-v2 on CPU

TEST_BOT_NAME = "sweep-nightly[bot]"
ENV = os.environ.get("ENV", "dev")
# ENV = os.environ.get("MODAL_ENVIRONMENT", "dev")

# ENV = PREFIX
# ENVIRONMENT = PREFIX

DB_MODAL_INST_NAME = "db"
DOCS_MODAL_INST_NAME = "docs"
API_MODAL_INST_NAME = "api"
UTILS_MODAL_INST_NAME = "utils"

BOT_TOKEN_NAME = "bot-token"

# goes under Modal 'discord' secret name (optional, can leave env var blank)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
DISCORD_MEDIUM_PRIORITY_URL = os.environ.get("DISCORD_MEDIUM_PRIORITY_URL")
DISCORD_LOW_PRIORITY_URL = os.environ.get("DISCORD_LOW_PRIORITY_URL")
DISCORD_FEEDBACK_WEBHOOK_URL = os.environ.get("DISCORD_FEEDBACK_WEBHOOK_URL")

SWEEP_HEALTH_URL = os.environ.get("SWEEP_HEALTH_URL")
DISCORD_STATUS_WEBHOOK_URL = os.environ.get("DISCORD_STATUS_WEBHOOK_URL")

# GitLab OAuth settings
GITLAB_APP_ID = GitLabOAuthConfig.APP_ID
GITLAB_APP_SECRET = GitLabOAuthConfig.APP_SECRET
GITLAB_REDIRECT_URI = GitLabOAuthConfig.REDIRECT_URI

GITHUB_LABEL_NAME = os.environ.get("GITHUB_LABEL_NAME", "sweep")
GITHUB_DEFAULT_CONFIG = os.environ.get(
    "GITHUB_DEFAULT_CONFIG",
    """# Sweep AI turns bugs & feature requests into code changes (https://sweep.dev)
# For details on our config file, check out our docs at https://docs.sweep.dev/usage/config

# This setting contains a list of rules that Sweep will check for. If any of these rules are broken in a new commit, Sweep will create an pull request to fix the broken rule.
rules:
{additional_rules}

# This is the branch that Sweep will develop from and make pull requests to. Most people use 'main' or 'master' but some users also use 'dev' or 'staging'.
branch: 'main'

# By default Sweep will read the logs and outputs from your existing GitLab CI/CD pipelines. To disable this, set this to false.
gitlab_ci_enabled: True

# This is the description of your project. It will be used by sweep when creating PRs. You can tell Sweep what's unique about your project, what frameworks you use, or anything else you want.
#
# Example:
#
# description: sweepai/sweep is a python project. The main api endpoints are in sweepai/api.py. Write code that adheres to PEP8.
description: ''

# This sets whether to create pull requests as drafts. If this is set to True, then all pull requests will be created as drafts and GitHub Actions will not be triggered.
draft: False

# This is a list of directories that Sweep will not be able to edit.
blocked_dirs: []
""",
)


OPENAI_DO_HAVE_32K_MODEL_ACCESS = (
    os.environ.get("OPENAI_DO_HAVE_32K_MODEL_ACCESS", "true").lower() == "true"
)
OPENAI_USE_3_5_MODEL_ONLY = (
    os.environ.get("OPENAI_USE_3_5_MODEL_ONLY", "false").lower() == "true"
)


# goes under Modal 'mongodb' secret name
MONGODB_URI = os.environ.get("MONGODB_URI", None)

IS_SELF_HOSTED = MONGODB_URI is None

# goes under Modal 'redis_url' secret name (optional, can leave env var blank)
REDIS_URL = os.environ.get("REDIS_URL")
# deprecated: old logic transfer so upstream can use this
if not REDIS_URL:
    REDIS_URL = os.environ.get("redis_url", "redis://0.0.0.0:6379/0")

ORG_ID = os.environ.get("ORG_ID", None)
# goes under Modal 'posthog' secret name (optional, can leave env var blank)
POSTHOG_API_KEY = os.environ.get(
    "POSTHOG_API_KEY", "phc_CnzwIB0W548wN4wEGeRuxXqidOlEUH2AcyV2sKTku8n"
)

LOGTAIL_SOURCE_KEY = os.environ.get("LOGTAIL_SOURCE_KEY")

E2B_API_KEY = os.environ.get("E2B_API_KEY")

SUPPORT_COUNTRY = os.environ.get("GDRP_LIST", "").split(",")

WHITELISTED_REPOS = os.environ.get("WHITELISTED_REPOS", "").split(",")


os.environ["TOKENIZERS_PARALLELISM"] = "false"

ACTIVELOOP_TOKEN = os.environ.get("ACTIVELOOP_TOKEN", None)

VECTOR_EMBEDDING_SOURCE = os.environ.get(
    "VECTOR_EMBEDDING_SOURCE", "sentence-transformers"
)  # Alternate option is openai or huggingface and set the corresponding env vars

BASERUN_API_KEY = os.environ.get("BASERUN_API_KEY", None)

# Huggingface settings, only checked if VECTOR_EMBEDDING_SOURCE == "huggingface"
HUGGINGFACE_URL = os.environ.get("HUGGINGFACE_URL", None)
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN", None)

# Replicate settings, only checked if VECTOR_EMBEDDING_SOURCE == "replicate"
REPLICATE_API_KEY = os.environ.get("REPLICATE_API_KEY", None)
REPLICATE_URL = os.environ.get("REPLICATE_URL", None)
REPLICATE_DEPLOYMENT_URL = os.environ.get("REPLICATE_DEPLOYMENT_URL", None)

# Default OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

# Azure settings, only checked if OPENAI_API_TYPE == "azure"
AZURE_API_KEY = os.environ.get("AZURE_API_KEY", None)
OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE", None)
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", None)
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION", None)

OPENAI_API_ENGINE_GPT35 = os.environ.get("OPENAI_API_ENGINE_GPT35", None)
OPENAI_API_ENGINE_GPT4 = os.environ.get("OPENAI_API_ENGINE_GPT4", None)
OPENAI_API_ENGINE_GPT4_32K = os.environ.get("OPENAI_API_ENGINE_GPT4_32K", None)
MULTI_REGION_CONFIG = os.environ.get("MULTI_REGION_CONFIG", None)
if isinstance(MULTI_REGION_CONFIG, str):
    MULTI_REGION_CONFIG = MULTI_REGION_CONFIG.strip("'").replace("\\n", "\n")
    MULTI_REGION_CONFIG = [item.split(",") for item in MULTI_REGION_CONFIG.split("\n")]

WHITELISTED_USERS = os.environ.get("WHITELISTED_USERS", "").split(",")

DEBUG: bool = True
ENV = os.environ.get("ENV", "dev")

DEFAULT_GPT4_32K_MODEL = os.environ.get("DEFAULT_GPT4_32K_MODEL", "gpt-4-1106-preview")
DEFAULT_GPT35_MODEL = os.environ.get("DEFAULT_GPT35_MODEL", "gpt-3.5-turbo-1106")

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", None)
LOKI_URL = os.environ.get("LOKI_URL", None)

DEBUG: bool = True
ENV = "prod" if GITHUB_BOT_USERNAME != TEST_BOT_NAME else "dev"
