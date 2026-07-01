from urllib.parse import quote

from src.app import activities


def test_unregister_success_removes_participant(client, reset_activities):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    email = "michael@mergington.edu"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client, reset_activities):
    # Arrange
    activity_name = "Unknown Activity"
    encoded_activity = quote(activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_missing_participant(client, reset_activities):
    # Arrange
    activity_name = "Programming Class"
    encoded_activity = quote(activity_name, safe="")
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
