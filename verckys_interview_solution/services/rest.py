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
def create_work_order(docName,item,qty,bom_no,targetWarehouse,progressWarehouse):
    print(f"\n\n\n\n{item}\n\n\n\n")
    try:
        
        
        work_order_doc = frappe.get_doc({
            "doctype": "Custom Work Order",
            "production_item": item,  
            "qty": float(qty),
            "sales_order": docName,
            "bom_no": bom_no,
            "fg_warehouse": targetWarehouse,
            "wip_warehouse": progressWarehouse,
            "required_items":fetch_sales_order_items(docName)
        })
        work_order_doc.insert()
        work_order_doc.save()
        return work_order_doc
        
    except Exception as e:
        frappe.throw(f"Error creating Work Order: {str(e)}")
        
        
        
@frappe.whitelist()
def fetch_sales_order_items(parent):
    get_items=frappe.get_all("Sales Order Item",{"parent":parent},["item_code","qty","rate","amount"])
    sales_order_items=[]
    for item in get_items:
        sales_order_items.append({
            "item_code":item.item_code,
            "required_qty":item.qty,
            "rate":item.rate,
            "amount":item.amount,
            "source_warehouse":"Stores - DB"
        })
    # print(f"This are the itemse\n\n\n\n{get_items}\n\n\n")
    return sales_order_items
    