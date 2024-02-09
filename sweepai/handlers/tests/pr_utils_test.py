from unittest.mock import MagicMock, patch

import pytest

from sweepai.handlers.pr_utils import make_pr


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.create_pull.return_value = MagicMock(
        add_to_assignees=MagicMock(),
        add_to_labels=MagicMock(),
        create_issue_comment=MagicMock()
    )
    return repo

@pytest.fixture
def mock_github_client(mock_repo):
    with patch('sweepai.handlers.pr_utils.get_github_client') as mock_client:
        mock_client.return_value = (None, mock_repo)
        yield mock_client

def test_make_pr_complete_logs(mock_github_client, mock_repo):
    title = "Fix GitHub Actions"
    repo_description = "Test Repo"
    summary = "GitHub Actions failed due to XYZ"
    repo_full_name = "sweepai/test"
    installation_id = "123"
    user_token = None
    use_faster_model = False
    username = "test_user"
    chat_logger = MagicMock()
    branch_name = "main"
    rule = None

    pr = make_pr(title, repo_description, summary, repo_full_name, installation_id, user_token, use_faster_model, username, chat_logger, branch_name, rule)

    mock_repo.create_pull.assert_called_once()
    pr.add_to_assignees.assert_called_once_with(username)
    pr.add_to_labels.assert_called_once()
    assert "Fix GitHub Actions" in pr.create_pull.call_args[1]['title']
    assert "GitHub Actions failed due to XYZ" in pr.create_pull.call_args[1]['body']
    pr.create_issue_comment.assert_called()

def test_make_pr_partial_logs(mock_github_client, mock_repo):
    title = "Partial Fix for GitHub Actions"
    summary = "Partial logs available"
    pr = make_pr(title, "Partial Repo", summary, "sweepai/partial", "456", None, False, "partial_user", MagicMock(), "dev", None)

    assert "Partial Fix for GitHub Actions" in pr.create_pull.call_args[1]['title']
    assert "Partial logs available" in pr.create_pull.call_args[1]['body']
    pr.create_issue_comment.assert_called()

def test_make_pr_no_logs(mock_github_client, mock_repo):
    title = "Attempt to Fix GitHub Actions Without Logs"
    summary = "No logs were available"
    pr = make_pr(title, "No Logs Repo", summary, "sweepai/nologs", "789", None, False, "nologs_user", MagicMock(), "test", None)

    assert "Attempt to Fix GitHub Actions Without Logs" in pr.create_pull.call_args[1]['title']
    assert "No logs were available" in pr.create_pull.call_args[1]['body']
    pr.create_issue_comment.assert_called()
