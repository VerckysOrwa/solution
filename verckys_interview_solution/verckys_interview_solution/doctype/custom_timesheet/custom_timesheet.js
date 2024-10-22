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

  after_save: (frm) => {
    let name = frm.doc.name;
    let user = frappe.session.user;
    frappe.call({
      method: "verckys_interview_solution.services.rest.create_user_permission",
      args: {
        docName: name,
        userName: user,
        doctype: "Custom Timesheet",
      },
      callback: (r) => {},
    });
  },

  validate: (frm) => {
    const currentDate = new Date();
    const inTimeDate = new Date(frm.doc.in_time);
    const outTimeDate = new Date(frm.doc.out_time);

    if (inTimeDate > currentDate) {
      frm.set_value("in_time", "");
      frappe.throw("In Time cannot be a future date");
    }

    if (outTimeDate > currentDate) {
      frm.set_value("out_time", "");
      frappe.throw("Out-time cannot be a future date");
    }

    if (inTimeDate > outTimeDate) {
      frm.set_value("out_time", "");
      frappe.throw("Out Time cannot be less than In Time");
    }
  },
});
