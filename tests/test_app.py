"""
Backend API tests for Mergington High School FastAPI app.
Run with: pytest
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Save original state and restore after each test
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(orig))

def test_get_activities():
    # Arrange: nothing to set up, using default state

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert resp.json()["message"].startswith("Signed up")

def test_signup_duplicate():
    # Arrange
    email = activities["Chess Club"]["participants"][0]

    # Act
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student already signed up"

def test_signup_nonexistent_activity():
    # Arrange
    email = "foo@bar.com"
    activity = "Nonexistent"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"

def test_unregister_success():
    # Arrange
    email = activities["Chess Club"]["participants"][0]

    # Act
    resp = client.delete(f"/activities/Chess%20Club/unregister?email={email}")

    # Assert
    assert resp.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert resp.json()["message"].startswith("Removed")

def test_unregister_not_signed_up():
    # Arrange
    email = "notregistered@mergington.edu"

    # Act
    resp = client.delete(f"/activities/Chess%20Club/unregister?email={email}")

    # Assert
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student is not signed up"

def test_unregister_nonexistent_activity():
    # Arrange
    email = "foo@bar.com"
    activity = "Nonexistent"

    # Act
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
