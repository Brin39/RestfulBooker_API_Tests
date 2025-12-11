import random
import string
from datetime import datetime, timedelta


def generate_random_string(length=8):
    """
    Generate a random string of letters.
    
    Args:
        length: Length of the string (default: 8)
        
    Returns:
        Random string of specified length
    """
    return ''.join(random.choices(string.ascii_letters, k=length))


def generate_booking_data(
    firstname=None,
    lastname=None,
    totalprice=None,
    depositpaid=None,
    checkin=None,
    checkout=None,
    additionalneeds=None
):
    """
    Generate valid booking data for tests.
    All parameters are optional - random values will be used if not provided.
    
    Args:
        firstname: Guest first name
        lastname: Guest last name
        totalprice: Total price of booking
        depositpaid: Whether deposit was paid
        checkin: Check-in date (YYYY-MM-DD)
        checkout: Check-out date (YYYY-MM-DD)
        additionalneeds: Additional needs/requests
        
    Returns:
        Dictionary with booking data ready for API
    """
    # Generate dates if not provided
    today = datetime.now()
    default_checkin = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    default_checkout = (today + timedelta(days=5)).strftime("%Y-%m-%d")
    
    return {
        "firstname": firstname or generate_random_string(),
        "lastname": lastname or generate_random_string(),
        "totalprice": totalprice if totalprice is not None else random.randint(100, 1000),
        "depositpaid": depositpaid if depositpaid is not None else random.choice([True, False]),
        "bookingdates": {
            "checkin": checkin or default_checkin,
            "checkout": checkout or default_checkout
        },
        "additionalneeds": additionalneeds or "Breakfast"
    }


def generate_partial_booking_data(field_name, field_value=None):
    """
    Generate partial booking data for PATCH requests.
    
    Args:
        field_name: Name of the field to update
        field_value: Value for the field (random if not provided)
        
    Returns:
        Dictionary with single field for partial update
    """
    if field_value is not None:
        return {field_name: field_value}
    
    # Generate random value based on field name
    field_generators = {
        "firstname": lambda: generate_random_string(),
        "lastname": lambda: generate_random_string(),
        "totalprice": lambda: random.randint(100, 1000),
        "depositpaid": lambda: random.choice([True, False]),
        "additionalneeds": lambda: random.choice(["Breakfast", "Lunch", "Dinner", "Late checkout"])
    }
    
    generator = field_generators.get(field_name, lambda: generate_random_string())
    return {field_name: generator()}

