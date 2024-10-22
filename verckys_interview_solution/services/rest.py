import frappe


@frappe.whitelist()
def create_user_permission(docName,userName,doctype):
    
    permission_doc = frappe.get_doc({
        "doctype": "User Permission",
        "user": userName,
        "for_value": docName,
        "allow": doctype
    })
    permission_doc.save()


@frappe.whitelist()
def create_work_order(docName,item,qty,bom_no,targetWarehouse):
    try:
        work_order_doc = frappe.get_doc({
            "doctype": "Custom Work Order",
            "production_item": item,  
            "qty_to_manufacture": float(qty),
            "sales_order": docName,
            "bom_no": bom_no,
            "fg_warehouse": targetWarehouse
        })
        work_order_doc.insert()
        work_order_doc.save()
        return work_order_doc
        
    except Exception as e:
        frappe.throw(f"Error creating Work Order: {str(e)}")
        frappe.log(e)
        
        
        
@frappe.whitelist()
def fetch_sales_order_items(parent):
    get_items=frappe.get_all("Sales Order Item",{"parent":parent},["item_code","qty","rate","amount"])
    sales_order_items=[]
    for item in get_items:
        sales_order_items.append({
            "item_code":item.item_code,
            "qty":item.qty,
            "rate":item.rate,
            "amount":item.amount
        })
    # print(f"This are the itemse\n\n\n\n{get_items}\n\n\n")
    return sales_order_items
    