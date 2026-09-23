# Copyright (c) 2026, Suba and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Attendant(Document):
	def rename_attendant(old_name,new_name):
		frapee.rename_doc("Attendant",old_name,new_name,merge=False)
	
	days = frappe.db.get_value("PawPass Settings", None, "reminder_days_before_checkout")

