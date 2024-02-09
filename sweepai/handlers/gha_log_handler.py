import re
from typing import Dict, List, Tuple

import requests


class GHALogHandler:
    def __init__(self, repo_full_name: str, token: str):
        self.repo_full_name = repo_full_name
        self.token = token
        self.base_url = "https://api.github.com"

    def _construct_headers(self) -> Dict[str, str]:
        return {"Authorization": f"token {self.token}"}

    def fetch_logs(self, run_id: int) -> str:
        url = f"{self.base_url}/repos/{self.repo_full_name}/actions/runs/{run_id}/logs"
        headers = self._construct_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def parse_logs(self, logs: str) -> List[str]:
        error_patterns = [r"error: (.+)", r"failed to (.+)", r"exception: (.+)"]
        errors = []
        for pattern in error_patterns:
            matches = re.findall(pattern, logs, re.IGNORECASE)
            errors.extend(matches)
        return errors

    def diagnose_issues(self, errors: List[str]) -> List[str]:
        common_issues = {
            "timeout": "Increase the timeout in your configuration.",
            "permission denied": "Check the permissions for the affected files or directories.",
            "could not resolve host": "Check your network connection and DNS settings."
        }
        diagnoses = []
        for error in errors:
            for issue, solution in common_issues.items():
                if issue in error.lower():
                    diagnoses.append(f"Error: {error}. Possible solution: {solution}")
        return diagnoses
