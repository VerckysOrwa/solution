// Copyright (c) 2024, Verckys Orwa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Custom Timesheet", {
  refresh(frm) {
    let user = frappe.session.user;
    frappe.call({
      method: "frappe.client.get_value",
      args: {
        doctype: "User",
        filters: { name: user },
        fieldname: ["full_name"],
      },
      callback: function (r) {
        if (!r.exc) {
        }
        let userName = r.message.full_name;
        if (!frm.doc.user) {
          frm.set_value("user", userName);
        }
      },
    });
  },
});
