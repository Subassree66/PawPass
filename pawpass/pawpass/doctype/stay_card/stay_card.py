# Copyright (c) 2026, Suba and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, add_days, today
from frappe.model.document import Document


class StayCard(Document):
	def before_print(self,method=None,print_settings=None):
		self.print_summary = f"{self.owner_name} - {self.pet}"
	def validate(self):
		expiry_date=frappe.db.get_value("Pet",self.pet,"vaccination_expiry")
		grace_days=frappe.db.get_single_value("PawPass Settings","vaccination_grace_days")or 0
		expiry=add_days(expiry_date,grace_days)
		if getdate(expiry) <= getdate(today()):
			self.vaccination_status="Expired"
			if self.status not in ("Draft"):
				frappe.throw("Vaccination is expired")
		else:
			self.vaccination_status="Valid"
		# self.vaccination_status="Valid"

		if self.purpose in ("Boarding","Both"):
			if getdate(self.expected_checkout_date) <= getdate(self.checkin_date):
				frappe.throw("Expexted check out date must be after check in date")

		for row in self.service_lines:
			row.line_total=row.rate * row.quantity
		self.services_total=sum(row.line_total for row in self.service_lines)
		self.fianl_amount=self.services_total

	def before_submit(self):
		if not self.status == "Ready for Pickup":
			frappe.throw("Cannot be submit because the pet is not ready for pickup")
		if not self.service_lines:
			frappe.throw("Minimun one row should be add in service line")
		if self.vaccination_status != "Valid":
			frappe.throw("Cannot submit because vaccination is not vaid")

	def on_submit(self):
		frappe.db.set_value("Pet",self.pet,{
			"last_visit_date":today(),
			"total_stays":(frappe.db.get_value("Pet",self.pet,"total_stays")or 0)+1
		})
		self.create_invoice()
		frappe.enqueue("pawpass.pawpass.doctype.stay_card.stay_card.send_stay_complete_email",stay_card_name=self.name)
	
	def create_invoice(self):
		invoice=frappe.get_doc({
			"doctype":"Invoice",
			"stay_card":self.name,
			"services_total": self.services_total,
			"total_amount":self.fianl_amount,
			"payment_status":"Unpaid"
		})
		invoice.insert(ignore_permissions=True)

	def on_cancel(self):
		self.status="Cancel"
		frappe.db.set_value("Pet",self.pet,{
			"total_stays":(frappe.db.get_value("Pet",self.pet,"total_stays"))-1
		})	

		invoice=frappe.db.get_value("Invoice",{"stay_card": self.name},"name")
		if invoice:
			invoice_doc=frappe.get_doc("Invoice",invoice)
			if(invoice_doc.docstatus == 1):
				invoice_doc.cancel()


	def on_trash(self):
		if self.status not in ["Draft","Cancelled"]:
			frappe.throw("Deletion cant be performed becaus the status is not in draft or cancelled")

	# def on_update(self):
	# 	self.save()


def send_stay_complete_email(stay_card_name):
	doc=frappe.get_doc("Stay Card",stay_card_name)
	pet_owner=frappe.get_value("Pet",doc.pet,"owmer_email")
	if pet_owner:
		frappe.sendmail(pet_owner,
		subject=f"{doc.pet} is ready for pickup", message="Your pet is ready for pickup com and pickup it")	

