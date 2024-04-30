import frappe, requests, json
from frappe import get_doc
from whatsapp.whatsapp.doctype.whatsapp_api.whatsapp_api import send_whatsapp_message

def create_user_from_lead(lead_name):
    url = 'https://api.interakt.ai/v1/public/track/users/'
    try:
        auth_encoded = frappe.get_doc("Whatsapp Settings").secret_key
    except:
        frappe.msgprint("Update Whatsapp Credentials")
    headers = {
        'Authorization': f'Basic {auth_encoded}',
        'Content-Type': 'application/json'
    }
    
    lead = get_doc("Lead", lead_name)
    try:
        
        email = lead.email_id
        if lead.mobile_no and len(lead.mobile_no) > 10:
            mobile_no = str(lead.mobile_no)[-10:]
        else:
            mobile_no = lead.mobile_no
        if lead.middle_name:
            middle_name = " " + str(lead.middle_name) + " "
        else:
            middle_name = " "
        name = str(lead.first_name) + middle_name + str(lead.last_name)
        if lead.phone_ext:
           code = lead.phone_ext
        else:
            code = "+91"
        if lead.type:
            lead_type = lead.type
        else:
            lead_type = ""
        if lead.request_type:
            request_type = lead.request_type
        else:
            request_type = ""
        if lead.company_name:
            company_name = lead.company_name
        else:
            company_name = ""
        
        data = {"userId":lead_name, 
                   "countryCode":code,
                   "phoneNumber":mobile_no,
                   "traits":{
                       "name": name,
                       "email": email,
                       "leadType": lead_type,
                       "requestType": request_type,
                          },
                     "tags": [
            f"leads.{company_name}",
        ]}
        json_data = json.dumps(data)
        # return json_data
        response = requests.post(url, headers=headers, data=json_data) 
        print("response", response)
        if "20" in str(response.status_code):
            result = response.json()
            # print(result)
            # frappe.msgprint(result['message'])
            return {"whatsapp":str(code) + mobile_no, "username": lead.first_name}
        else: 
            return response
    except Exception as e:
        # frappe.throw(e)
        print("error", e)
        return {"whatsapp":str(code) + mobile_no, "username": lead.first_name}




def send_message(number, template, username, link=None, filename=None):
    url = 'https://api.interakt.ai/v1/public/message/'
    auth_encoded = "TmU1aV9IYTF2ZmwwSWRKSmkwX1ZVTGYzRlNwanRqNHNnRlpzT3FrWGlTSTo="
    headers = {
        'Authorization': f'Basic {auth_encoded}',
        'Content-Type': 'application/json'
    }
    header_values = None
    if template == "welcome_message_codersdaily":
        header_values = ["https://interaktprodstorage.blob.core.windows.net/mediaprodstoragecontainer/364a0496-1486-4709-ad5e-82a5718667b1/message_template_media/igEsU82RxyFQ/codersdaily%20data%20analytics%20curriculum%20%281%29.pdf?se=2029-04-10T09%3A20%3A01Z&sp=rt&sv=2019-12-12&sr=b&sig=Fv9/qH%2B1bajiqJbLBXLKCvMWAYWy6srtZ%2BE/5NJQGG4%3D"]

    if template == "thepharmadaily_master_class":
        header_values = [
            "https://interaktprodstorage.blob.core.windows.net/mediaprodstoragecontainer/364a0496-1486-4709-ad5e-82a5718667b1/message_template_media/WURaQkrSERFr/MicrosoftTeams-image%20%2841%29.png?se=2028-07-25T06%3A31%3A50Z&sp=rt&sv=2019-12-12&sr=b&sig=LWfj%2BF%2BT9uEN9RoDL06yRfgo24YwUXO9EnlLRs/OWMY%3D"
        ]
    if template == "codersdaily_signup_for_seminar":
        header_values=[username]
    body_values = [username] if template != "codersdaily_signup_for_seminar" else [link]
    data = {
        "fullPhoneNumber": number,
        "callbackData": "send successfully",
        "type": "Template",
        "template": {
            "name": template,
            "languageCode": "en",
            header_values and "headerValues": header_values,
            "bodyValues": body_values,
            filename and "fileName": filename
        }
    }
    json_data = json.dumps(data)
    response = requests.post(url, headers=headers, data=json_data)
    print("res",response)
    if "20" in str(response.status_code):
        result = response.json()
        # frappe.msgprint(result['message'])
        return response.json()
    else:
        return response.json()

@frappe.whitelist()
def send_whatsapp_msg(**args):
    template = args["template"]
    lead_name = args["lead"]
    print(lead_name)
    data = None
    try:
        data = args["link"]
    except:
        link = None
        filename = None
    if data:
        if template == "thepharmadaily_master_class" or template == "codersdaily_signup_for_seminar":
            link=data
            filename=None
        else:
            filename=data
            link=None

    response = create_user_from_lead(lead_name)
    print(response)
    if response:
        try:
            mobile_no = response['whatsapp']
            first_name = response['username']
            print("mobile", mobile_no)
            if mobile_no:
                # print("hello", mobile_no)
                response = send_whatsapp_message(template, first_name, mobile_no, filename, link)
                # response = send_message(mobile_no, template, first_name, link, filename)
                return response
            else: 
                frappe.throw("Please update your phone number")
        except:
            pass
    return response