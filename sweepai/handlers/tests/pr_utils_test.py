from unittest.mock import MagicMock, patch

import pytest

from sweepai.handlers.pr_utils import make_pr


@pytest.fixture
def mock_dependencies():
    with patch("sweepai.handlers.pr_utils.get_github_client") as mock_github_client, \
         patch("sweepai.handlers.pr_utils.ClonedRepo") as mock_cloned_repo, \
         patch("sweepai.handlers.pr_utils.SweepBot.from_system_message_content") as mock_sweep_bot, \
         patch("sweepai.handlers.pr_utils.create_pr_changes") as mock_create_pr_changes, \
         patch("sweepai.handlers.pr_utils.logger") as mock_logger:
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_github_client.return_value = (None, mock_repo)
        mock_sweep_bot.return_value.generate_pull_request.return_value = mock_pr
        mock_create_pr_changes.return_value = {"pull_request": {"title": "Test PR", "body": "Test Body", "pr_head": "head", "pr_base": "base"}}
        yield mock_github_client, mock_cloned_repo, mock_sweep_bot, mock_create_pr_changes, mock_repo, mock_pr, mock_logger

def test_successful_pr_creation(mock_dependencies):
    _, _, _, _, mock_repo, mock_pr, _ = mock_dependencies
    mock_repo.create_pull.return_value = mock_pr
    mock_pr.add_to_assignees.return_value = None
    mock_pr.create_issue_comment.return_value = None
    mock_pr.add_to_labels.return_value = None

    result = make_pr("Test PR", "Repo Description", "Summary", "repo/full_name", "installation_id", None, True, "username", MagicMock())

    assert result == mock_pr
    mock_repo.create_pull.assert_called_once_with(title="Test PR", body=pytest.any, head="head", base="base")
    mock_pr.add_to_assignees.assert_called_once_with("username")
    mock_pr.create_issue_comment.assert_called_once()
    mock_pr.add_to_labels.assert_called_once()

def test_error_handling_during_pr_creation(mock_dependencies):
    _, _, _, _, mock_repo, _, mock_logger = mock_dependencies
    mock_repo.create_pull.side_effect = Exception("GitHub API Error")

    result = make_pr("Test PR", "Repo Description", "Summary", "repo/full_name", "installation_id", None, True, "username", MagicMock())

    assert "error" in result
    mock_logger.error.assert_called_once_with(pytest.any)

def test_correct_assignment_of_reviewers_and_labels(mock_dependencies):
    _, _, _, _, mock_repo, mock_pr, _ = mock_dependencies
    mock_repo.create_pull.return_value = mock_pr
    mock_pr.add_to_assignees.return_value = None
    mock_pr.create_issue_comment.return_value = None
    mock_pr.add_to_labels.return_value = None

    make_pr("Test PR", "Repo Description", "Summary", "repo/full_name", "installation_id", None, True, "username", MagicMock())

    mock_pr.add_to_assignees.assert_called_once_with("username")
    mock_pr.add_to_labels.assert_called_once()
