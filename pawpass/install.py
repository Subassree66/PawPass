import frappe
def after_install():
    Service_type = {"Overnight Boarding":1500,"Deshedding Treatment":1000,"Nail Trim":300,"Bath & Brush":800}
    for i,j in Service_type.items():
        if not frappe.db.exists("Service Type",i):
            doc = frappe.new_doc("Service Type")
            doc.service_name = i
            doc.base_rate=j
            doc.insert(ignore_permissions=True)

    if not frappe.db.exists("PawPass Settings","PawPass Shop"):
        s =frappe.get_single("PawPass Settings")
        s.shop_name = "PawPass Shop"
        s.manager_email = "manager@gmail.com"
        s.default_boarding_rate=4000
        s.vaccination_grace_days =0
        s.reminder_days_before_checkout=2
        s.save(ignore_permissions=True)
    frappe.msgprint("Successfully created the documents")