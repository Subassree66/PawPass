import frappe
def perm_check(user):
    if user == frappe.session.user:
        user = frappe.session.user
    return "(`tabToDo`.owner = {user} or `tabToDo`.assigned_by = {user})".format(user=frappe.db.escape(user))
