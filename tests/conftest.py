"""
Pytest configuration and shared fixtures.

This module provides common fixtures used across multiple test files
to reduce code duplication and ensure test independence.
"""
import pytest
from logic.auth_api import AuthApi
from logic.booking_api import BookingApi
from utils.test_data import generate_booking_data


@pytest.fixture
def booking_api():
    """
    Fixture providing a BookingApi instance.
    
    Returns:
        BookingApi: Fresh API client instance
    """
    return BookingApi()


@pytest.fixture
def auth_api():
    """
    Fixture providing an AuthApi instance.
    
    Returns:
        AuthApi: Fresh API client instance
    """
    return AuthApi()


@pytest.fixture
def auth_token(auth_api):
    """
    Fixture providing a valid authentication token.
    
    Args:
        auth_api: AuthApi fixture
        
    Returns:
        str: Valid authentication token
    """
    response = auth_api.create_token()
    return response.json()["token"]


@pytest.fixture
def created_booking(booking_api):
    """
    Fixture that creates a booking and returns its data.
    
    Args:
        booking_api: BookingApi fixture
        
    Returns:
        dict: Contains 'id', 'data', and 'response'
    """
    booking_data = generate_booking_data()
    response = booking_api.create_booking(booking_data)
    booking_id = response.json()["bookingid"]
    
    return {
        "id": booking_id,
        "data": booking_data,
        "response": response
    }


@pytest.fixture
def booking_with_auth(booking_api, auth_token):
    """
    Fixture that creates a booking and provides auth token.
    Useful for tests that need to modify/delete a booking.
    
    Args:
        booking_api: BookingApi fixture
        auth_token: Auth token fixture
        
    Returns:
        dict: Contains 'id', 'data', 'token', and 'api'
    """
    booking_data = generate_booking_data()
    response = booking_api.create_booking(booking_data)
    booking_id = response.json()["bookingid"]
    
    return {
        "id": booking_id,
        "data": booking_data,
        "token": auth_token,
        "api": booking_api
    }

