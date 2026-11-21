# storage.py
# Member 3: CSV handling for FreshFold Laundry orders

import csv  # built-in tool for reading and writing CSV files
import os  # lets us check whether a file exists
from datetime import (
    datetime,
)  # gives us the current date and time  # built-in tool for reading and writing CSV files

# The file where all orders are saved
ORDERS_FILE = "orders.csv"

# The column names, in the agreed order (a list)
COLUMNS = [
    "order_id",
    "full_name",
    "phone",
    "service",
    "quantity",
    "total",
    "pickup_date",
    "pickup_time",
    "instructions",
    "status",
    "created_at",
]

# The four allowed statuses, in order (a tuple: it never changes)
STATUSES = ("Order Placed", "Processing", "In Laundry", "Ready for Delivery")


def get_all_orders():
    """Return a list of dictionaries, one per order.

    If the file is missing or empty, return an empty list.
    """
    orders = []  # start with an empty list
    try:
        # newline="" is recommended by Python when working with CSV files
        with open(ORDERS_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # reads each row as a dictionary
            for row in reader:  # loop over every row
                orders.append(row)  # add it to our list
    except FileNotFoundError:
        pass  # no file yet, so just return the empty list
    return orders


def generate_order_id():
    """Return the next order ID, like ORD1001, ORD1002, ..."""
    highest = 1000  # so the first order will be ORD1001
    for order in get_all_orders():
        # "ORD1005" -> remove the first 3 letters -> "1005" -> number 1005
        number_text = order["order_id"][3:]
        if number_text.isdigit():
            highest = max(highest, int(number_text))
    return "ORD" + str(highest + 1)


def save_order(order_dict):
    """Add one order to orders.csv.

    order_dict needs: full_name, phone, service, quantity, total,
    pickup_date, pickup_time, instructions.
    Returns the saved order (with order_id, status, created_at added).
    """
    # Add the details that the system (not the user) decides
    order_dict["order_id"] = generate_order_id()
    order_dict["status"] = STATUSES[0]  # every new order starts as "Order Placed"
    order_dict["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # If the file is missing or empty, we must write the header row first
    need_header = (not os.path.exists(ORDERS_FILE)) or os.path.getsize(ORDERS_FILE) == 0

    with open(ORDERS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        if need_header:
            writer.writeheader()  # writes the column names line
        writer.writerow(order_dict)  # writes the order as one row
    return order_dict


def get_order(order_id):
    """Return the order (a dictionary) with this ID, or None if not found."""
    order_id = order_id.strip().upper()  # clean the text the user typed
    for order in get_all_orders():
        if order["order_id"] == order_id:
            return order  # found it
    return None  # looped through all, no match


def update_status(order_id, new_status):
    """Change the status of one order. Returns True if it worked, else False."""
    # Only accept the four allowed statuses
    if new_status not in STATUSES:
        return False

    orders = get_all_orders()  # read everything
    found = False
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = new_status  # change just this order
            found = True

    if not found:
        return False

    # Write the whole file again ("w" erases the old content first)
    with open(ORDERS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(orders)  # writes all rows at once
    return True
