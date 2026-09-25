# Copyright (c) 2026, Suba and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns=get_columns()
    data=get_data(filters)
    return columns,data,None
def get_columns():
    return [
        {
            "label": _("Attendant"), 
            "fieldname":"assigned_attendant", 
            "fieldtype":"Link", 
            "options":"Attendant"
        },
        {
            "label": _("Total Stays"), 
            "fieldname":"total_stays", 
            "fieldtype":"Int"
        },
        {
            "label": _("Completed"), 
            "fieldname":"completed_stays", 
            "fieldtype":"Int"
        },
        {
            "label": _("Average Stay Length (nights)"), 
            "fieldname":"average_stay_length", 
            "fieldtype":"Int"
        },
        {
            "label": _("Revenue"), 
            "fieldname":"revenue", 
            "fieldtype":"Currency"
        },
        {
            "label": _("Completion Rate %"), 
            "fieldname":"completion_rate", 
            "fieldtype":"Percent"
        },
    ]
def get_data(filters=None):
		filters = filters or {}
		query = f"""
			SELECT 
				assigned_attendant,
				COUNT(name) as total_stays,
				SUM(CASE 
				WHEN status='Picked Up' THEN 1 
				ELSE 0 END) as completed_stays,
				ROUND(AVG(DATEDIFF(actual_checkout_date,checkin_date)), 0) as average_stay_length,
				SUM(CASE 
				WHEN status='Picked Up' THEN fianl_amount 
				ELSE 0 END) as revenue,
				ROUND((SUM(CASE 
				WHEN status='Picked Up' THEN 1 
				ELSE 0 END) / COUNT(name)) * 100, 2) as completion_rate
			FROM 
				`tabStay Card`
			GROUP BY 
				assigned_attendant
			ORDER BY 
				assigned_attendant ASC
		"""
		return frappe.db.sql(query,filters,as_dict=True)

