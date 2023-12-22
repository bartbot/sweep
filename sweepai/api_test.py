import pytest
from fastapi.testclient import TestClient

from sweepai.api import app

client = TestClient(app)

# Test data mimicking GitLab issue webhook payload
test_data = {
    "user": {
        "username": "testuser"
    },
    "project": {
        "path_with_namespace": "test/test"
    },
    "object_attributes": {
        "action": "open",
        "title": "Test issue",
        "iid": 1,
        "url": "https://gitlab.com/test/test/-/issues/1",
        "state": "opened"
    },
    "labels": [{"id": 1, "title": "test", "color": "#ffffff", "description": "test"}],
    "changes": {}
}

def test_gitlab_webhook():
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    test_data["object_attributes"]["action"] = "update"
    response = client.post("/webhook/gitlab/issue", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"status": "GitLab issue webhook processed successfully"}

    test_data["object_attributes"]["action"] = "invalid"
    response = client.post("/webhook/gitlab/issue", json=test_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported GitLab event"}
