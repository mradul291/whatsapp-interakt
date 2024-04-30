# Copyright (c) 2024, Techsolvo LLP and contributors
# For license information, please see license.txt

import frappe, json, requests
from frappe.model.document import Document


class WhatsappAPI(Document):
	pass




def send_whatsapp_message(template_name, first_name, mobile_no, file_name=None, link=None):
	template = frappe.get_doc("Whatsapp Template", template_name)
	url = 'https://api.interakt.ai/v1/public/message/'
	auth_encoded = frappe.get_doc("Whatsapp Settings").secret_key
	headers = {
		'Authorization': f'Basic {auth_encoded}',
		'Content-Type': 'application/json'
	}
	header_values = [template.media_link or first_name]
	msg_variable = [first_name]
	if link and len(str(template.body_variables)) > 1:
		msg_variable.append(link)
	elif link:
		msg_variable = [link]
	print(msg_variable)
	data = {
		"fullPhoneNumber": mobile_no,
		"callbackData": "send successfully",
		"type": "Template",
		"template": {
			"name": template_name,
			"languageCode": "en",
			header_values and "headerValues": header_values,
			"bodyValues": msg_variable,
			file_name and "fileName":file_name,
		}
	}
	json_data = json.dumps(data)
	response = requests.post(url, headers=headers, data=json_data)
	print(response)
	if "20" in str(response.status_code):
		frappe.msgprint("Sent successfully")
		return response.json()
	else:
		return response.json() 

@frappe.whitelist()
def send_message(**args):
	template_name = args['template_name']
	contact_name = args['contact']
	try:
		file_name = args['file_name']
	except:
		file_name=None
	try:
		link = args['link']
	except:
		link=None
	contact_info = frappe.get_doc("Whatsapp Contact", contact_name)
	if len(contact_info.mobile_no)==10:
		if contact_info.country_code:
			mobile_no = str(contact_info.country_code) + str(contact_info.mobile_no)
		else:
			mobile_no = "91" + str(contact_info.mobile_no)
	else:
		mobile_no = contact_info.mobile_no
	data = send_whatsapp_message(template_name, contact_name, mobile_no, file_name, link)
	# print("hello world", contact_name, template_name)
	return data


	# url = 'https://api.interakt.ai/v1/public/message/'
	# auth_encoded = frappe.get_doc("Whatsapp Settings").secret_key
	# headers = {
	# 	'Authorization': f'Basic {auth_encoded}',
	# 	'Content-Type': 'application/json'
	# }
	# header_values = [header_value]
	# body_values = body_value
	# data = {
	# 	"fullPhoneNumber": mobile_number,
	# 	"callbackData": "send successfully",
	# 	"type": "Template",
	# 	"template": {
	# 		"name": template,
	# 		"languageCode": "en",
	# 		header_values and "headerValues": header_values,
	# 		"bodyValues": body_values,
	# 		"fileName": filename
	# 	}
	# }
	# json_data = json.dumps(data)
	# response = requests.post(url, headers=headers, data=json_data)
	# print(response)
	# if "20" in str(response.status_code):
	# 	frappe.msgprint("Invoice sent successfully")
	# 	return response.json()
	# else:
	# 	return response.json()