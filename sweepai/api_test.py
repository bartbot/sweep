import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from sweepai.api import app, handle_gitlab_issue_webhook, webhook_redirect

client = TestClient(app)

# Test data mimicking GitLab issue webhook payload
test_data_issue_open = {
    "user": {
        "username": "testuser"
    },
    "project": {
        "description": "Test project",
        "path_with_namespace": "test/test"
    },
    "object_attributes": {
        "action": "open",
        "title": "Test issue",
        "iid": 1,
        "url": "https://gitlab.com/test/test/-/issues/1",
        "description": "Test description",
        "state": "opened"
    },
    "labels": [],
    "changes": {}
}

# Test data mimicking GitLab issue webhook payload for update action
test_data_issue_update = {
    "user": {
        "username": "testuser"
    },
    "project": {
        "description": "Test project",
        "path_with_namespace": "test/test"
    },
    "object_attributes": {
        "action": "update",
        "title": "Test issue",
        "iid": 1,
        "url": "https://gitlab.com/test/test/-/issues/1",
        "description": "Test description",
        "state": "opened"
    },
    "labels": [],
    "changes": {
        "title": {
            "previous": "Old title",
            "current": "Test issue"
        },
        "description": {
            "previous": "Old description",
            "current": "Test description"
        }
    }
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
# Test data mimicking GitLab issue webhook payload for close action
test_data_issue_close = {
    "user": {
        "username": "testuser"
    },
    "project": {
        "description": "Test project",
        "path_with_namespace": "test/test"
    },
    "object_attributes": {
        "action": "close",
        "title": "Test issue",
        "iid": 1,
        "url": "https://gitlab.com/test/test/-/issues/1",
        "description": "Test description",
        "state": "closed"
    },
    "labels": [],
    "changes": {}
}
    response = client.post("/webhook/gitlab", json=test_data_issue_open, headers={"X-GitLab-Event": "Issue Hook"})
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    response = client.post("/webhook/gitlab", json=test_data_issue_update, headers={"X-GitLab-Event": "Issue Hook"})
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    response = client.post("/webhook/gitlab", json=test_data_issue_close, headers={"X-GitLab-Event": "Issue Hook"})
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    response = client.post("/webhook/gitlab", json=test_data_issue_open)
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported GitLab event"}

def test_handle_gitlab_issue_webhook():
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
