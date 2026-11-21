# reports.py
# Member 3: report and analysis functions for FreshFold Laundry

import storage  # our own file, so we can read the orders


def get_total_revenue():
    """Add up the total of every order and return the sum."""
    total = 0  # running total starts at 0
    for order in storage.get_all_orders():  # loop over every order
        try:
            total += int(order["total"])  # text "250" -> number 250
        except ValueError:
            pass  # skip an order with a bad total
    return total


def count_by_status():
    """Return a dictionary: status -> number of orders with that status."""
    counts = {}
    for status in storage.STATUSES:  # start every status at 0
        counts[status] = 0

    for order in storage.get_all_orders():  # count each order
        status = order["status"]
        if status in counts:  # ignore unknown statuses
            counts[status] += 1
    return counts


def get_popular_services():
    """Return a list of tuples (service, count), most popular first."""
    counts = {}  # service -> number of orders

    for order in storage.get_all_orders():  # loop over every order
        service = order["service"]
        counts[service] = counts.get(service, 0) + 1  # add 1 to this service

    # Turn the dictionary into a list of (service, count) tuples,
    # then sort by the count (second item), biggest first
    ranking = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return ranking


def get_summary():
    """Return one dictionary with every number the dashboard needs."""
    counts = count_by_status()  # orders per status
    total_orders = sum(counts.values())  # all orders together
    completed = counts["Ready for Delivery"]  # finished orders
    pending = total_orders - completed  # everything not finished

    ranking = get_popular_services()  # list of (service, count)
    if len(ranking) > 0:
        top_service = ranking[0][0]  # first tuple, first value
    else:
        top_service = "None yet"  # no orders at all

    summary = {
        "total_revenue": get_total_revenue(),
        "total_orders": total_orders,
        "pending": pending,
        "completed": completed,
        "status_counts": counts,
        "ranking": ranking,
        "top_service": top_service,
    }
    return summary


def generate_text_report():
    """Return a simple multi-line text report."""
    summary = get_summary()
    lines = []  # we build the report line by line
    lines.append("FRESHFOLD LAUNDRY - SUMMARY REPORT")
    lines.append("-----------------------------------")
    lines.append("Total orders   : " + str(summary["total_orders"]))
    lines.append("Total revenue  : Rs. " + str(summary["total_revenue"]))
    lines.append("Pending orders : " + str(summary["pending"]))
    lines.append("Completed      : " + str(summary["completed"]))
    lines.append("Top service    : " + summary["top_service"])
    lines.append("")
    lines.append("Orders per status:")
    for status, count in summary["status_counts"].items():
        lines.append("  " + status + ": " + str(count))
    lines.append("")
    lines.append("Service ranking:")
    position = 1
    for service, count in summary["ranking"]:
        lines.append(
            "  " + str(position) + ". " + service + " (" + str(count) + " orders)"
        )
        position += 1
    return "\n".join(lines)  # join the lines with line breaks
