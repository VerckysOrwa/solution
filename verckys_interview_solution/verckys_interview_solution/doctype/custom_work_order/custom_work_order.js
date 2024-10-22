// Copyright (c) 2024, Verckys Orwa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Custom Work Order", {
  sales_order(frm) {
    frappe.call({
      method:
        "verckys_interview_solution.services.rest.fetch_sales_order_items",
      args: {
        parent: frm.doc.sales_order,
      },
      callback: (r) => {
        if (r) {
          console.log(r.message);
          let itemsData = r.message;
          let item_table = frm.doc.required_items;

          for (let data of itemsData) {
            for (let row of item_table) {
              console.log("this row log", row);
              row.item_code = data.item_code;
              row.required_qty = data.required_qty;
            }
          }
          frm.refresh_field("required_items");
        }
      },
    });
  },
  refresh(frm) {
    frm.add_custom_button("Select Sales Orders", () => {
        let dialog = new frappe.ui.Dialog({
            title: "Select Sales Orders",
            fields: [
                {
                    fieldname: "sales_orders",
                    fieldtype: "Table",
                    label: "Sales Orders",
                    options: "Sales Order CT",
                    fields: [
                        {
                            fieldname: "sales_order",
                            fieldtype: "Link",
                            options: "Sales Order",
                            in_list_view: 1,
                            label: "Sales Order"
                        }
                    ]
                }
            ],
            primary_action_label: "Get Items",
            
        });
        dialog.show();
    });
}

});
