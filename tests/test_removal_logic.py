import pytest
from fastapi import HTTPException
from src.app import remove_participant, activities

def test_remove_validation_activity_exists():
    """Test that removal validates activity exists"""
    with pytest.raises(HTTPException) as exc_info:
        remove_participant("NonExistent Activity", "test@example.com")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"

def test_remove_validation_student_signed_up():
    """Test that removal validates student is signed up"""
    activity_name = "Chess Club"
    email = "not_signed@example.com"

    with pytest.raises(HTTPException) as exc_info:
        remove_participant(activity_name, email)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Student not signed up for this activity"

def test_remove_success_unit():
    """Test successful removal logic"""
    activity_name = "Gym Class"
    email = "remove_unit@example.com"

    # Ensure signed up
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    initial_count = len(activities[activity_name]["participants"])

    # Remove
    result = remove_participant(activity_name, email)
    assert result == {"message": f"Removed {email} from {activity_name}"}

    # Verify removed
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1