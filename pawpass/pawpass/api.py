import frappe
from frappe.utils import add_days, today
from frappe.query_builder import DocType, Order
from frappe.query_builder.functions import DateAdd, Now

# @frappe.whitelist()
def get_upcoming_checkouts():
    SC = DocType("Stay Card")
    result = (
        frappe.qb.from_(SC).select(SC.name,SC.pet,SC.owner_name,SC.expected_checkout_date).where(SC.status.isin (["Checked In","In Service"]))
        .where(SC.expected_checkout_date <= add_days(today(),2)).orderby(SC.expected_checkout_date, order=frappe.qb.asc)
        .run(as_dict=True))
    return result

@frappe.whitelist()
def share_stay_card(stay_card_name,user_email):
    if not frappe.has_permission("Stay Card","read",doc=stay_card_name):
        frappe.throw("No permission to read this stay card document")
    if not frappe.db.exists("User",user_email):
        frappe.throw("No user is there in this email")
    frappe.share.add(doctype = "Stay Card",name = stay_card_name,user = user_email,read=1,write=0)
    return f"stay card{stay_card_name} is shared to {user_email} only in reading mode."

@frappe.whitelist()
def transfer_stays(from_attendant, to_attendant):
    try:
        frappe.db.sql((to_attendant,from_attendant))
        frappe.db.commit()
    except Exception as e:
        frappe.db.roolback()
        frappe.log_error(
            title="transfer_stays failed",message="log error in to_attendant and from_attendant"
        )

