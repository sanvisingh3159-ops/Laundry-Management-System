# billing.py
# Pure Python logic for the FreshFold booking system (Member 2).
# There is NO Flask in this file.

import math
from datetime import date, datetime

# A dictionary of prices.
# Key = service name, Value = price in rupees
# These are SAMPLE prices. The team must make them match templates/_prices.html
PRICES = {
    "washing": 50,         # rupees per kg
    "ironing": 10,         # rupees per item
    "dry-cleaning": 100,   # rupees per item
    "wash-and-iron": 60,   # rupees per kg
}

# A set of the allowed service names.
# A set is perfect for checking "is this value allowed?"
ALLOWED_SERVICES = {"washing", "ironing", "dry-cleaning", "wash-and-iron"}


def calculate_bill(service_key, quantity):
    """Return the total bill for a service and quantity.

    service_key : text such as "washing"
    quantity    : how many kg or items (a number)
    """
    # Look up the price of this service in the dictionary
    price = PRICES[service_key]

    # Total = price multiplied by quantity
    total = price * quantity

    # Round to 2 decimal places so the bill looks neat (for example 2.5 kg)
    return round(total, 2)


def validate_booking(form_data):
    """Check the booking form data.

    form_data : a dictionary with the form fields
    Returns a tuple: (is_valid, errors)
      is_valid : True if everything is correct, otherwise False
      errors   : a list of error messages (empty if all is fine)
    """
    # An empty list to collect error messages
    errors = []

    # ---- Check 1: the name must have only letters and spaces ----
    name = form_data.get("full_name", "").strip()

    if name == "":
        errors.append("Full name is required.")
    elif not name.replace(" ", "").isalpha():
        errors.append("Name can contain only letters and spaces.")

    # ---- Check 2: the phone number must be exactly 10 digits ----
    phone = form_data.get("phone", "").strip()

    if not (phone.isdigit() and len(phone) == 10):
        errors.append("Phone number must be exactly 10 digits.")

    # ---- Check 3: the service must be one of the allowed services ----
    service = form_data.get("service", "").strip()

    if service not in ALLOWED_SERVICES:
        errors.append("Please choose a valid service.")

    # ---- Check 4: quantity must be a number greater than 0 ----
    quantity_text = form_data.get("quantity", "").strip()

    try:
        # Try to convert the text to a number
        quantity = float(quantity_text)
    except ValueError:
        # The text was not a number, for example "abc" or ""
        errors.append("Quantity must be a number.")
    else:
        # Reject odd values such as "nan" and "inf"
        if not math.isfinite(quantity):
            errors.append("Quantity must be a number.")
        elif quantity <= 0:
            errors.append("Quantity must be greater than 0.")

    # ---- Check 5: pickup date must be a real date and not in the past ----
    pickup_date_text = form_data.get("pickup_date", "").strip()

    try:
        # Convert text like "2026-11-25" into a real date
        pickup_date = datetime.strptime(pickup_date_text, "%Y-%m-%d").date()
    except ValueError:
        # The text was empty or not a proper date
        errors.append("Please choose a valid pickup date.")
    else:
        # A date smaller than today means it is in the past
        if pickup_date < date.today():
            errors.append("Pickup date cannot be in the past.")

    # ---- Check 6: pickup time must be chosen ----
    pickup_time = form_data.get("pickup_time", "").strip()

    if not pickup_time:
        errors.append("Please choose a pickup time.")

    # If the errors list is empty, the booking is valid
    is_valid = len(errors) == 0

    return (is_valid, errors)