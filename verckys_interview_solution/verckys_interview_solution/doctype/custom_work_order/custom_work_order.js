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
          let itemsData = r.message;
          let item_table = frm.doc.required_items;

          for (let data of itemsData) {
            for (let row of item_table) {
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

    frm.add_custom_button("Select Multiple Sales Orders", () => {
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
            primary_action(data) {
                console.log("This is the data:", data);
            
                if (data.sales_orders && data.sales_orders.length) {
                    data.sales_orders.forEach(order => {
                        
                        frappe.call({
                            method: "verckys_interview_solution.services.rest.fetch_sales_order_items",
                            args: { parent: order.sales_order },
                            callback: (r) => {
                                if (r && r.message) {
                                    let itemsData = r.message;
                                    let item_table = frappe.model.add_child(frm.doc, "Required Items", "required_items");

                                    for (let data of itemsData) {
                                        
                            
                                          item_table.custom_sales_order = order.sales_order;
                                          item_table.item_code = data.item_code;
                                          item_table.required_qty = data.required_qty;
                                          item_table.source_warehouse=data.source_warehouse
                                        
                                      }
            
                                    frm.refresh_field("required_items");
                                }
                            }
                        });
                    });
                } else {
                    frappe.msgprint(__("Please select at least one Sales Order"));
                }
            
                dialog.hide();
            }
            
            
        });
        dialog.show();
    });
}

});
