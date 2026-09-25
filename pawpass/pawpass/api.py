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
        frappe.db.sql(""" UPDATE `tabStay Card` set attendant = %s where attendant = %s and and status ='Open' """,(to_attendant,from_attendant))
        frappe.db.commit()
    except Exception as e:
        frappe.db.roolback()
        frappe.log_error(
            title="transfer_stays failed",
            message="log error in to_attendant and from_attendant"
        )
        raise
        
@frappe.whitelist()
def get_stay_summary(stay_card_name):
    stay_card=frappe.form_dict.get("stay_card_name")
    s=frappe.db.exists("Stay Card",stay_card)
    if not s:
        frappe.local.response["http_status_code"]=404
        return {"error":"Not Found"}
    doc=frappe.get_doc("Stay Card",stay_card)
    summary={
        "name":doc.name,
        "pet code":doc.pet,
        "owner name":doc.owner_name,
        "final amount":doc.fianl_amount
    }
    pet=frappe.get_doc("Pet",doc.pet)
    if frappe.session.user !="Guest":
        summary["email"]=pet.owmer_email
    return summary

@frappe.whitelist()
def reassign_attendant(stay_card,attendant):
    doc=frappe.get_doc("Stay Card",stay_card)
    doc.assigned_attendant=attendant
    doc.save()

@frappe.whitelist()
import frappe
from frappe.utils import today, add_days

def check_upcoming_checkouts():
    exist = frappe.db.get_value(
        "Audit Log",
        {
            "action": "checkout_reminder",
            "date": today()
        }, "name"
    )
    if exist:
        return
    settings = frappe.get_single("PawPass Settings")
    reminder_days = settings.reminder_days_before_checkout
    checkout_date = add_days(today(), reminder_days)
    stays = frappe.get_all(
        "Stay Card",
        filters={
            "expected_checkout_date": ["between", [today(), checkout_date]],
            "status": ["in", ["Checked In", "In Service"]]
        },
        fields=[
            "name", "pet",
            "owner_name", "owmer_email",
            "expected_checkout_date"
        ]
    )
    for stay in stays:
        if stay.owmer_email:
            frappe.sendmail(
                recipients=[stay.owmer_email],
                subject="Upcoming Checkout Reminder",
                message=f"""Hello {stay.owmer_name},your pet {stay.pet} is due for checkout on{stay.expected_checkout_date}.""")

    log = frappe.new_doc("Audit Log")
    log.doctype_name = "Stay Card"
    log.document_name = "Checkout Reminder"
    log.action = "checkout_reminder"
    log.user = frappe.session.user
    log.timestamp = frappe.utils.now_datetime()
    log.date = today()
    log.insert(ignore_permissions=True)
    

def format_value(value):
    return frappe.format_value(value,{"field_type":"Currency"})

# ad12cd0226aac58:1eb6576a94ab573