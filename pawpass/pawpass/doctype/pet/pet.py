# Copyright (c) 2026, Suba and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Pet(Document):
	def autoname(self):
		self.pet_code =self.pet_code.upper()
		self.name=make_autoname("PET-.YYYY.-.####")

	pass
