from unittest.mock import MagicMock, patch

import pytest

from sweepai.api import clean_logs, download_logs, make_pr, stack_pr


@pytest.fixture
def mock_request():
    class MockRequest:
        repository = MagicMock(full_name="sweepai/sweep")
        check_run = MagicMock(run_id="123", conclusion="failure")
        installation = MagicMock(id="1")
        sender = MagicMock(login="test_user")
    return MockRequest()

@pytest.fixture
def mock_pr():
    return MagicMock(number=1, title="[Sweep GHA Fix] Fix the failing GitHub Actions")

def test_download_logs_success(mock_request):
    with patch("sweepai.api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"logs": "test logs", "error_highlights": ["error1"]}
        logs, error_highlights = download_logs(mock_request.repository.full_name, mock_request.check_run.run_id, mock_request.installation.id, highlight_errors=True)
        assert logs == "test logs"
        assert error_highlights == ["error1"]

def test_download_logs_failure(mock_request):
    with patch("sweepai.api.requests.get", side_effect=Exception("Network error")):
        with pytest.raises(Exception):
            download_logs(mock_request.repository.full_name, mock_request.check_run.run_id, mock_request.installation.id)

def test_clean_logs_success():
    logs = "test logs with error"
    error_highlights = ["error"]
    cleaned_logs, user_message = clean_logs(logs, error_highlights)
    assert "error" in cleaned_logs
    assert user_message == "Errors highlighted."

def test_clean_logs_malformed():
    logs = None
    error_highlights = None
    cleaned_logs, user_message = clean_logs(logs, error_highlights)
    assert cleaned_logs == ""
    assert user_message == "No logs available."

def test_stack_pr_success(mock_request, mock_pr):
    with patch("sweepai.api.get_github_client") as mock_client:
        mock_repo = MagicMock()
        mock_client.return_value = (None, mock_repo)
        mock_repo.get_pull.return_value = mock_pr
        stack_pr("[Sweep GHA Fix] Test", mock_pr.number, mock_request.sender.login, mock_request.repository.full_name, mock_request.installation.id, "test_tracking_id")
        mock_repo.create_pull.assert_called_once()

def test_make_pr_success(mock_request):
    with patch("sweepai.api.get_github_client") as mock_client, patch("sweepai.api.ChatLogger") as mock_logger:
        mock_repo = MagicMock()
        mock_client.return_value = (None, mock_repo)
        mock_logger.return_value.use_faster_model.return_value = False
        make_pr("[Sweep GHA Fix] Test", "Repo description", "Summary with user_message", mock_request.repository.full_name, mock_request.installation.id, None, False, mock_request.sender.login, mock_logger())
        mock_repo.create_pull.assert_called_once()
