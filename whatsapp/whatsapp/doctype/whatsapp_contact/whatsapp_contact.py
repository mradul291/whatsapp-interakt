# Copyright (c) 2024, Techsolvo LLP and contributors
# For license information, please see license.txt

import frappe, json, requests
from frappe.model.document import Document
import random

class WhatsappContact(Document):
    def on_update(self):
        name = self.first_name
        email = self.email_id
        mobile_no = self.mobile_no
        code = self.country_code
        dob = self.dob
        response = create_user_from_lead(name,email,mobile_no,code)
        if response:
            frappe.msgprint("Created Successfully")

@frappe.whitelist()
def create_user_from_lead(name, email, mobile_no, code="91", dob=None):
    url = 'https://api.interakt.ai/v1/public/track/users/'
    auth_encoded = frappe.get_doc("Whatsapp Settings").secret_key
    headers = {
        'Authorization': f'Basic {auth_encoded}',
        'Content-Type': 'application/json'
    }
    
    try:
        
        
        data = {"userId":random.randint(100000, 999999), 
                   "countryCode":code,
                   "phoneNumber":mobile_no,
                   "traits":{
                       "name": name,
                       "email": email,
                       dob and "dob":dob,
                          },
                }
        json_data = json.dumps(data)
        response = requests.post(url, headers=headers, data=json_data) 
        print("response", response)
        if "20" in str(response.status_code):
            return response.json()
    except Exception as e:
        frappe.throw(e)
        print(e)
        return None
