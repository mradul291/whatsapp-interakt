frappe.ui.form.on("Whatsapp API", {
  refresh(frm) {
    const msgButton = frm.fields_dict.send_message.$wrapper;

    // Remove existing event listeners (if any)
    msgButton.off("click");

    // Attach event listener
    msgButton.on("click", function () {
      console.log("Calling Whatsapp API");
      const template_name = frm.doc.template;
      const contact = frm.doc.contact;
      const file_name = frm.doc.file_name;
      const link = frm.doc.link_name;
      console.log(template_name, contact);
      frm.save();
      frappe.call({
        method:
          "whatsapp.whatsapp.doctype.whatsapp_api.whatsapp_api.send_message",
        args: {
          template_name: template_name,
          contact: contact,
          file_name: file_name,
          link: link,
        },
        callback: function (response) {
          console.log(response);
        },
      });
    });
  },
});
