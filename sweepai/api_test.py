import pytest
from fastapi.testclient import TestClient

from sweepai.api import app, handle_gitlab_issue_webhook, webhook_redirect

client = TestClient(app)

# Test data mimicking GitLab issue webhook payload
test_data_issue_open = {
    "object_kind": "issue",
    "event_type": "issue",
    "object_attributes": {
        "action": "open",
        "title": "Test issue",
        "id": 1,
        "url": "https://gitlab.com/test/test/-/issues/1",
    },
    "labels": [{"id": 1, "title": "test", "color": "#ffffff", "description": "test"}],
}

# Test data mimicking GitLab issue webhook payload for update action
test_data_issue_update = {
# Test data mimicking GitLab pipeline webhook payload
test_data_pipeline = {
    "object_kind": "pipeline",
    "object_attributes": {
        "id": 1,
        "status": "success",
        "ref": "master",
        "sha": "abc123",
        "web_url": "https://gitlab.com/test/test/pipelines/1",
    },
}

# Test data mimicking GitLab merge request webhook payload
test_data_merge_request = {
    "object_kind": "merge_request",
    "event_type": "merge_request",
    "object_attributes": {
        "id": 1,
        "target_branch": "master",
        "source_branch": "feature",
        "state": "opened",
        "title": "Test merge request",
        "url": "https://gitlab.com/test/test/-/merge_requests/1",
    },
}
    "object_kind": "issue",
    "event_type": "issue",
    "object_attributes": {
        "action": "update",
        "title": "Test issue",
        "id": 1,
        "url": "https://gitlab.com/test/test/-/issues/1",
    },
    "labels": [{"id": 1, "title": "test", "color": "#ffffff", "description": "test"}],
}

def test_webhook_redirect():
    response = client.post("/webhook", json=test_data_issue_open, headers={"X-GitLab-Event": "Issue Hook"})
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    response = client.post("/webhook", json=test_data_issue_update, headers={"X-GitLab-Event": "Issue Hook"})
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    response = client.post("/webhook", json=test_data_issue_open)
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported GitLab event"}

def test_handle_gitlab_webhook():
def test_handle_gitlab_pipeline_webhook():
    response = client.post("/webhook/gitlab/pipeline", json=test_data_pipeline)
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab pipeline webhook processed successfully"}

def test_handle_gitlab_merge_request_webhook():
    response = client.post("/webhook/gitlab/merge_request", json=test_data_merge_request)
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab merge request webhook processed successfully"}
    response = client.post("/webhook/gitlab/issue", json=test_data_issue_open)
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    response = client.post("/webhook/gitlab/issue", json=test_data_issue_update)
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    test_data_issue_invalid = test_data_issue_open.copy()
    test_data_issue_invalid["object_attributes"]["action"] = "invalid"
    response = client.post("/webhook/gitlab/issue", json=test_data_issue_invalid)
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported GitLab event"}
