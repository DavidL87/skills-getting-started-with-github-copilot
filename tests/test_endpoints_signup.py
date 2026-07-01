from urllib.parse import quote

from src.app import activities


def test_signup_success_adds_participant(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    email = "new.student@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client, reset_activities):
    # Arrange
    activity_name = "Unknown Activity"
    encoded_activity = quote(activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client, reset_activities):
    # Arrange
    activity_name = "Programming Class"
    encoded_activity = quote(activity_name, safe="")
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_returns_400_when_activity_is_full(client, reset_activities):
    # Arrange
    activity_name = "Tennis Club"
    encoded_activity = quote(activity_name, safe="")
    max_participants = activities[activity_name]["max_participants"]
    activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": "late.student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
