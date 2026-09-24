import frappe
def get_shop_name():
    s=frappe.get_single("PawPass Settings")
    return s.shop_name