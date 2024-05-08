import frappe, json, requests

def send_message(mobile_number, template, customer_name, invoice_url, invoice_name):
    url = 'https://api.interakt.ai/v1/public/message/'
    auth_encoded = frappe.get_doc("Whatsapp Settings").secret_key
    if not(auth_encoded):
        frappe.throw("Update your credentials in whatsapp setting")
    headers = {
        'Authorization': f'Basic {auth_encoded}',
        'Content-Type': 'application/json'
    }
    header_values = [invoice_url]
    body_values = [customer_name]
    data = {
        "fullPhoneNumber": mobile_number,
        "callbackData": "send successfully",
        "type": "Template",
        "template": {
            "name": template,
            "languageCode": "en",
            header_values and "headerValues": header_values,
            "bodyValues": body_values,
            "fileName": invoice_name
        }
    }
    json_data = json.dumps(data)
    # return json_data
    response = requests.post(url, headers=headers, data=json_data)
    print(response)
    if "20" in str(response.status_code):
        frappe.msgprint("Invoice sent successfully")
        return response.json()
    else:
        return response.json()

@frappe.whitelist()
def send_invoice(**args):
    invoice_url = args['url']
    invoice_name = args['invoice_name']
    # print(invoice_url)
    sales_invoice = frappe.get_doc("Sales Invoice", invoice_name)
    # print(sales_invoice)
    # Get the customer linked to the Sales Invoice
    customer = frappe.get_doc("Customer", sales_invoice.customer)
    if customer.mobile_no:
        mobile_number = customer.mobile_no
        if len(mobile_number) == 10:
            mobile_number = "91" + str(mobile_number)
        customer_name = customer.customer_name
        response = send_message(mobile_number, "invoice_techsolvo", customer_name, invoice_url, invoice_name)
        return response
    else:
        frappe.throw("Mobile number not available")
        return None