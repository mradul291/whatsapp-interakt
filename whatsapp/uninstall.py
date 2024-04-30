import frappe
def before_uninstall():
    delete_script()


def delete_script():
    try:
        frappe.delete_doc("Client Script", "Send Invoice")
        frappe.delete_doc("Client Script", "Send Template")
        frappe.delete_doc("Client Script", "Send Template 2")
        frappe.db.commit()
    except:
        pass