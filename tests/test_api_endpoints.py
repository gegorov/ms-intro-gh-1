import pytest
from fastapi.testclient import TestClient

def test_get_activities(client: TestClient):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # We have 9 activities
    assert "Chess Club" in data
    assert "Programming Class" in data

    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success(client: TestClient):
    """Test successful signup"""
    activity_name = "Chess Club"
    email = "test@example.com"

    # Get initial participants
    response = client.get("/activities")
    initial_participants = response.json()[activity_name]["participants"]

    # Signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    # Verify participant was added
    response = client.get("/activities")
    updated_participants = response.json()[activity_name]["participants"]
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1

def test_signup_activity_not_found(client: TestClient):
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_signup_duplicate(client: TestClient):
    """Test signup when already signed up"""
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Second signup should fail
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}

def test_remove_participant_success(client: TestClient):
    """Test successful participant removal"""
    activity_name = "Programming Class"
    email = "remove@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Remove
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    # Verify removed
    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    assert email not in participants

def test_remove_participant_activity_not_found(client: TestClient):
    """Test removal from non-existent activity"""
    response = client.delete("/activities/NonExistent/participants?email=test@example.com")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_remove_participant_not_signed_up(client: TestClient):
    """Test removal when not signed up"""
    activity_name = "Chess Club"
    email = "notsigned@example.com"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not signed up for this activity"}