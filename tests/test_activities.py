from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

initial_activities = deepcopy(activities)
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(deepcopy(initial_activities))
    yield


def test_signup_adds_participant_and_increases_count():
    # Arrange
    activity = "Chess Club"
    email = "new_student@mergington.edu"
    original_count = len(initial_activities[activity]["participants"]) 

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == original_count + 1


def test_unregister_removes_participant():
    # Arrange
    activity = "Chess Club"
    email = initial_activities[activity]["participants"][0]
    original_count = len(initial_activities[activity]["participants"]) 

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == original_count - 1


def test_signing_up_same_email_twice_returns_400():
    # Arrange
    activity = "Tennis"
    email = "duplicate@mergington.edu"

    # Act
    first = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    second = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert first.status_code == 200
    assert second.status_code == 400
