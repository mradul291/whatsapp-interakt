import frappe
from frappe.modules.utils import sync_customizations
def after_install():
    create_script()
    create_client_script()
    create_client_script2()

def create_script():
    # Define properties of the custom doctype
    custom_doctype = {
        "doctype": "Client Script",
        "name": "Send Invoice",  # Name of the custom doctype
        "dt": "Sales Invoice",
        "script": """
            // frappe.ui.form.on('Sales Invoice', {
            // \trefresh(frm) {
            // \t\t// your code here
            // \t}
            // })
            let invoice;
            frappe.ui.form.on("Sales Invoice", {
                onload: function (frm) {
                    invoice = frm.doc.name;
                },
                refresh: function (listview) {
                    listview.page.add_menu_item(__("Send Invoice"), () => {
                        const url = window.location.href;
                        const parsedUrl = new URL(url);
                        let baseUrl =
                            parsedUrl.protocol + "//" + parsedUrl.hostname + (parsedUrl.port ? ":" + parsedUrl.port : "");
                        let invoiceUrl =
                            baseUrl +
                            "/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&name=" +
                            invoice;
                        frappe.call({
                            method: "whatsapp_interakt.whatsapp_interakt.doctype.whatsapp_api.whatsapp_invoice.send_invoice",
                            args: {
                                url: invoiceUrl,
                                invoice_name: invoice,
                            },
                            callback: function (response) {
                                frappe.msgprint("Message sent successfully");
                                console.log(response);
                            },
                        });
                    });
                },
            });
        """,
    }

    # Create the custom doctype document
    doc = frappe.get_doc(custom_doctype)
    doc.enabled = 1
    # Save the document
    doc.insert()

    # Sync customizations to reflect changes
    sync_customizations('sync')



def create_client_script():
    custom_doctype = {
        "doctype": "Client Script",
        "name": "Send Template",  # Name of the custom doctype
        "dt": "Lead",
        "script": """
            let leads;
frappe.listview_settings["Lead"] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("Send Bulk Messages"), function () {
			leads = listview.get_checked_items();
			console.log(leads);
			frappe.call({
				method: "whatsapp_interakt.whatsapp_interakt.doctype.whatsapp_template.whatsapp_template.get_all_templates",
				callback: function (response) {
					let data = response.message;
					let options = data.map((obj) => ({ label: obj.name, value: obj.name }));
					openDialogWithSelectOptions(options);
				},
			});
		});
		function openDialogWithSelectOptions(options) {
			let d = new frappe.ui.Dialog({
				title: "Enter details",
				fields: [
					{
						label: "Template",
						fieldname: "template",
						fieldtype: "Select",
						options: options,
						reqd: true,
					},
					{
						label: "Link/Filename",
						fieldname: "linkFilename",
						fieldtype: "Data",
					},
				],
				primary_action_label: __("Send"),
				primary_action: function () {
					let values = d.get_values();
					if (values.template == "codersdaily_signup_for_seminar" && !values.linkFilename) {
						frappe.msgprint({
							title: __("Notification"),
							indicator: "red",
							message: __("Link is required for this template!"),
						});
					} else {
						console.log("hey", values.template, values.linkFilename);
						d.hide();
						leads.map((lead) => {
							frappe.call({
								method: "whatsapp_interakt.whatsapp_interakt.doctype.whatsapp_api.whatsapp_lead.send_whatsapp_msg",
								args: {
									template: values.template,
									lead: lead.name,
									link: values.linkFilename,
								},
								callback: function (response) {
									// frappe.msgprint("Message sent successfully");
									console.log(response);
									// navigateToDocType(response.message);
								},
							});
						});
						frappe.msgprint("Messages added to queue");
					}
				},
			});
			d.show();
		}
	},
};

        """,
    }

    # Create the custom doctype document
    doc = frappe.get_doc(custom_doctype)
    doc.view = "List"
    doc.enabled = 1
    # Save the document
    doc.insert()

    # Sync customizations to reflect changes
    sync_customizations('sync')
def create_client_script2():
    # Define properties of the custom doctype
    custom_doctype = {
        "doctype": "Client Script",
        "name": "Send Template 2",  # Name of the custom doctype
        "dt": "Lead",
        "script": """
        let lead;
frappe.ui.form.on("Lead", {
	after_save: function (frm) {
		location.reload();
	},
	onload: function (frm) {
		lead = frm.doc.name;
	},
	refresh: function (listview) {
		listview.page.add_menu_item(__("Send whatsapp message"), () => {
			frappe.call({
				method: "whatsapp_interakt.whatsapp_interakt.doctype.whatsapp_template.whatsapp_template.get_all_templates",
				callback: function (response) {
					let data = response.message;
					let options = data.map((obj) => ({ label: obj.name, value: obj.name }));
					openDialogWithSelectOptions(options);
				},
			});
		});
		function openDialogWithSelectOptions(options) {
			let d = new frappe.ui.Dialog({
				title: "Enter details",
				fields: [
					{
						label: "Template",
						fieldname: "template",
						fieldtype: "Select",
						options: options,
						reqd: true,
					},
					{
						label: "Link/Filename",
						fieldname: "linkFilename",
						fieldtype: "Data",
					},
				],
				primary_action_label: __("Send"),
				primary_action: function () {
					let values = d.get_values();
					if (values.template == "codersdaily_signup_for_seminar" && !values.linkFilename) {
						frappe.msgprint({
							title: __("Notification"),
							indicator: "red",
							message: __("Link is required for this template!"),
						});
					} else {
						console.log("hey", values.template, values.linkFilename);

						frappe.call({
							method: "whatsapp_interakt.whatsapp_interakt.doctype.whatsapp_api.whatsapp_lead.send_whatsapp_msg",
							args: {
								template: values.template,
								lead: lead,
								link: values.linkFilename,
							},
							callback: function (response) {
								frappe.msgprint("Message sent successfully");
								console.log(response);
								// navigateToDocType(response.message);
							},
						});
						d.hide();
					}
				},
			});
			d.show();
		}
		
	}
    })
        """,
    }

    # Create the custom doctype document
    doc = frappe.get_doc(custom_doctype)
    doc.enabled = 1
    # Save the document
    doc.insert()

    # Sync customizations to reflect changes
    sync_customizations('sync')