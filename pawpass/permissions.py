import frappe
def session_user(user):
    if not user or user=="Guest":
        return False
    if user=="Administrator":
        return ""
    roles=frappe.get_roles(user)
    if "PP Attendant" not in roles:
        return ""
    return f""" `tabStay Card`.assigned_attendant IN(SELECT name FROM `tabAttendant` WHERE user={frappe.db.escape(user)})"""

def print():
    stay_cards = frappe.get_all("Stay Card", fields=["name","assigned_attendant"])
    for sc in stay_cards:
        att = frappe.get_doc("Attendant", sc.assigned_attendant)
        print(att.attendant_name, att.phone)