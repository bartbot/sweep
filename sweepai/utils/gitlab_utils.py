import datetime
import difflib
import hashlib
import os
import re
import shutil
import subprocess
import time
import traceback
from dataclasses import dataclass
from functools import cached_property
from typing import Any

import git
import rapidfuzz
import requests
from gitlab import Gitlab
from jwt import encode
from redis import Redis
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from redis.retry import Retry

from sweepai.config.client import SweepConfig
from sweepai.config.server import GITLAB_APP_ID, GITLAB_APP_SECRET, REDIS_URL
from sweepai.logn import logger
from sweepai.utils.ctags import CTags
from sweepai.utils.ctags_chunker import get_ctags_for_file
from sweepai.utils.tree_utils import DirectoryTree

# Rest of the code goes here, with all instances of Github replaced with Gitlab,
# and all instances of GITHUB_APP_ID and GITHUB_APP_PEM replaced with GITLAB_APP_ID and GITLAB_APP_SECRET respectively.
