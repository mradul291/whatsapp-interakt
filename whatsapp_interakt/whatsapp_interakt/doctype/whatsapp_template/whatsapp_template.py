# Copyright (c) 2024, Techsolvo LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WhatsappTemplate(Document):
	pass


@frappe.whitelist()
def get_all_templates():
	try:
		data = frappe.get_all('Whatsapp Template', fields=['name'])
		return data
	except Exception as e:
		frappe.log_error(frappe._('Error fetching data from doctype: {0}').format(e))
		return None