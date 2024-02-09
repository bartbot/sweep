from unittest.mock import MagicMock, patch

import pytest

from sweepai.api import clean_logs, download_logs, make_pr, on_check_suite


@pytest.fixture
def mock_github_api():
    with patch("sweepai.api.get_github_client") as mock:
        yield mock

@pytest.fixture
def mock_download_logs():
    with patch("sweepai.api.download_logs", return_value="mocked logs") as mock:
        yield mock

@pytest.fixture
def mock_clean_logs():
    with patch("sweepai.api.clean_logs", return_value=("cleaned mocked logs", "user message")) as mock:
        yield mock

@pytest.fixture
def mock_make_pr():
    with patch("sweepai.api.make_pr", return_value={"success": True}) as mock:
        yield mock

def test_detect_gha_failure(mock_github_api):
    mock_repo = MagicMock()
    mock_repo.get_commits.return_value = [MagicMock()]
    mock_repo.get_commits.return_value[0].get_statuses.return_value = [MagicMock(state="failure")]
    mock_github_api.return_value = (None, mock_repo)
    assert on_check_suite({"action": "completed", "check_run": {"conclusion": "failure"}}) is not None

def test_log_retrieval_success(mock_download_logs):
    assert download_logs("repo/full_name", "run_id", "installation_id") == "mocked logs"

def test_log_cleaning_success(mock_clean_logs):
    logs, user_message = clean_logs("mocked logs")
    assert logs == "cleaned mocked logs"
    assert user_message == "user message"

def test_pr_creation_success(mock_make_pr):
    response = make_pr("title", "repo_description", "summary", "repo_full_name", "installation_id", None, True, "username", MagicMock())
    assert response == {"success": True}

def test_log_retrieval_failure():
    with patch("sweepai.api.download_logs", side_effect=Exception("Failed to retrieve logs")):
        with pytest.raises(Exception) as excinfo:
            download_logs("repo/full_name", "run_id", "installation_id")
        assert "Failed to retrieve logs" in str(excinfo.value)

def test_pr_creation_failure(mock_make_pr):
    mock_make_pr.side_effect = Exception("Failed to create PR")
    with pytest.raises(Exception) as excinfo:
        make_pr("title", "repo_description", "summary", "repo_full_name", "installation_id", None, True, "username", MagicMock())
    assert "Failed to create PR" in str(excinfo.value)
