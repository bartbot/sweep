from unittest.mock import Mock

import pytest
import requests
from requests.exceptions import HTTPError

from sweepai.handlers.gha_log_handler import GHALogHandler


@pytest.fixture
def gha_log_handler():
    return GHALogHandler(repo_full_name="sweepai/test-repo", token="dummy_token")

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")

def test_fetch_logs_success(gha_log_handler, mock_requests_get):
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.text = "Sample log content"
    mock_requests_get.return_value = mock_response
    assert gha_log_handler.fetch_logs(run_id=123) == "Sample log content"

def test_fetch_logs_failure(gha_log_handler, mock_requests_get):
    mock_requests_get.side_effect = HTTPError("API error")
    with pytest.raises(HTTPError):
        gha_log_handler.fetch_logs(run_id=123)

@pytest.mark.parametrize("logs,expected_errors", [
    ("error: failed to compile\nexception: missing file", ["failed to compile", "missing file"]),
    ("ERROR: could not resolve host", ["could not resolve host"]),
    ("warning: deprecated API\nerror: permission denied", ["permission denied"]),
])
def test_parse_logs(gha_log_handler, logs, expected_errors):
    assert gha_log_handler.parse_logs(logs) == expected_errors

@pytest.mark.parametrize("errors,expected_diagnoses", [
    (["timeout"], ["Error: timeout. Possible solution: Increase the timeout in your configuration."]),
    (["permission denied"], ["Error: permission denied. Possible solution: Check the permissions for the affected files or directories."]),
    (["unknown error"], []),
])
def test_diagnose_issues(gha_log_handler, errors, expected_diagnoses):
    assert gha_log_handler.diagnose_issues(errors) == expected_diagnoses
