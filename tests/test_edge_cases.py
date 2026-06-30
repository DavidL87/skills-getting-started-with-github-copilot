from urllib.parse import quote

from src.app import activities


def test_signup_accepts_email_with_plus_alias(client, reset_activities):
    # Arrange
    activity_name = "Art Studio"
    encoded_activity = quote(activity_name, safe="")
    email = "student+robotics@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_handles_activity_name_with_spaces(client, reset_activities):
    # Arrange
    activity_name = "Science Olympiad"
    encoded_activity = quote(activity_name, safe="")
    email = "space.name@mergington.edu"

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
