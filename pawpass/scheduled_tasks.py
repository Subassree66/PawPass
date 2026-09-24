def check_upcoming_checkouts():
    last_run = frappe.db.get_value("Audit Log",
        {"action": "checkout_reminder", "date": today()}, "name")
    if last_run:
        return  