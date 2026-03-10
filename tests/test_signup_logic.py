import pytest
from fastapi import HTTPException
from src.app import signup_for_activity, activities

def test_signup_validation_activity_exists():
    """Test that signup validates activity exists"""
    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity("NonExistent Activity", "test@example.com")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"

def test_signup_validation_not_already_signed_up():
    """Test that signup validates student is not already signed up"""
    activity_name = "Chess Club"
    email = "existing@example.com"

    # Ensure clean state - remove if exists
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # First signup should succeed
    result = signup_for_activity(activity_name, email)
    assert result == {"message": f"Signed up {email} for {activity_name}"}

    # Second signup should fail
    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity(activity_name, email)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Student already signed up for this activity"

    # Clean up
    activities[activity_name]["participants"].remove(email)

def test_signup_success_unit():
    """Test successful signup logic"""
    activity_name = "Programming Class"
    email = "unit_test@example.com"

    # Ensure clean state
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    initial_count = len(activities[activity_name]["participants"])

    # Signup
    result = signup_for_activity(activity_name, email)
    assert result == {"message": f"Signed up {email} for {activity_name}"}

    # Verify added
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1

    # Clean up
    activities[activity_name]["participants"].remove(email)