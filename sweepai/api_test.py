import unittest
import unittest.mock

from sweepai import api


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.mock_api = unittest.mock.create_autospec(api)

    def test_webhook(self):
        self.mock_api.webhook.return_value = {"success": True}
        result = self.mock_api.webhook()
        self.assertEqual(result, {"success": True})
        self.mock_api.webhook.assert_called_once()

    def test_home(self):
        self.mock_api.home.return_value = "<h2>Sweep Webhook is up and running! To get started, copy the URL into the GitHub App settings' webhook field.</h2>"
        result = self.mock_api.home()
        self.assertEqual(result, "<h2>Sweep Webhook is up and running! To get started, copy the URL into the GitHub App settings' webhook field.</h2>")
        self.mock_api.home.assert_called_once()

    # Add more test methods as needed for each function in api.py

if __name__ == '__main__':
    unittest.main()
    def test_download_logs_with_detailed_info(self):
        mock_request = unittest.mock.Mock()
        mock_request.repository.full_name = "test/repo"
        mock_request.check_run.run_id = 123
        mock_request.installation.id = 1

        api.download_logs = unittest.mock.MagicMock(return_value=("log content", {"complex_failure_analysis": True}))
        logs, detailed_failure_info = api.download_logs(mock_request.repository.full_name, mock_request.check_run.run_id, mock_request.installation.id, detailed=True)

        self.assertEqual(logs, "log content")
        self.assertTrue(detailed_failure_info["complex_failure_analysis"])
        api.download_logs.assert_called_once_with("test/repo", 123, 1, detailed=True)
    def test_clean_logs_with_detailed_failure_info(self):
        logs = "Error: Something failed"
        detailed_failure_info = {"complex_failure_analysis": True}

        api.clean_logs = unittest.mock.MagicMock(return_value=("cleaned logs", "A summary of the failure: Something failed"))
        cleaned_logs, user_message = api.clean_logs(logs, detailed_failure_info, include_potential_causes=True)

        self.assertEqual(cleaned_logs, "cleaned logs")
        self.assertEqual(user_message, "A summary of the failure: Something failed")
        api.clean_logs.assert_called_once_with(logs, detailed_failure_info, include_potential_causes=True)
    def test_stack_pr_with_failure_logs(self):
        request = {
            "repository": {"full_name": "test/repo"},
            "check_run": {"run_id": 123},
            "installation": {"id": 1},
            "sender": {"login": "testuser"}
        }
        pr_number = 456
        repo_full_name = "test/repo"
        installation_id = 1
        tracking_id = "abc123"
        logs = "Error: Something failed"

        api.stack_pr = unittest.mock.MagicMock()
        api.stack_pr(
            request=f"[Sweep GHA Fix] The GitHub Actions run failed with the following error logs:\n\n```\n\n{logs}\n\n```\n\nHere are some suggestions to help you address the failure:\n- Review the detailed error information provided above.\n- Check our [documentation](https://docs.sweepai.com/github-actions-fixes) for common fixes.\n- Ensure all dependencies are correctly installed and up-to-date.\n\nIf you continue to experience issues, please consult the [GitHub Actions documentation](https://docs.github.com/en/actions) or reach out to our support team.\n\nTracking ID: {tracking_id}",
            pr_number=pr_number,
            username="testuser",
            repo_full_name=repo_full_name,
            installation_id=installation_id,
            tracking_id=tracking_id,
        )

        api.stack_pr.assert_called_once()
    def test_make_pr_with_detailed_analysis(self):
        title = "[Sweep GHA Fix] Fix the failing GitHub Actions"
        repo_description = "A test repository"
        summary = "The GitHub Actions run failed with the following error logs:\n\n```\nError: Something failed\n```\n\nFor a detailed analysis and potential fixes, please review the GitHub Actions run linked here: [GitHub Actions Run](https://github.com/test/repo/actions/runs/abc123).\n\nSuggestions for potential fixes include:\n- Ensuring all dependencies are correctly installed and up-to-date.\n- Reviewing the changes made in recent commits that could affect the workflow.\n- Consulting the [GitHub Actions documentation](https://docs.github.com/en/actions) for further insights."
        repo_full_name = "test/repo"
        installation_id = 1
        use_faster_model = True
        username = "testuser"

        api.make_pr = unittest.mock.MagicMock()
        api.make_pr(
            title=title,
            repo_description=repo_description,
            summary=summary,
            repo_full_name=repo_full_name,
            installation_id=installation_id,
            user_token=None,
            use_faster_model=use_faster_model,
            username=username,
            chat_logger=unittest.mock.ANY,
        )

        api.make_pr.assert_called_once()
