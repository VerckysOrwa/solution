import frappe


@frappe.whitelist()
def create_user_permission(docName,userName,doctype):
    try:
        permission_doc = frappe.get_doc({
            "doctype": "User Permission",
            "user": userName,
            "for_value": docName,
            "allow": doctype
        })
        permission_doc.save()
    except Exception as e:
        frappe.log_error(f"An Errror occured while crearing user permission for {userName}: {(e)}")


@frappe.whitelist()
def create_work_order(docName,item,qty,bom_no,targetWarehouse,progressWarehouse):
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
    try:
        get_items=frappe.get_all("Sales Order Item",{"parent":parent},["item_code","qty","rate","amount"])
        sales_order_items=[]
        for item in get_items:
            sales_order_items.append({
                "item_code":item.item_code,
                "required_qty":item.qty,
                "rate":item.rate,
                "amount":item.amount,
                "source_warehouse":"Stores - DB",
                
            })
        return sales_order_items
    except Exception as e:
        frappe.log_error(f"There was an error while fetching the sales order items: {(e)}")
    
    
    
    
@frappe.whitelist(allow_guest=True,methods=["POST","PUT"])
def customer_api(customer_name, mobile_number, email_address, address_line1, address_line2, 
                city, pincode, state, country, sales_person, salutation):
    try:
        def check_sales_person_exists():
            sales_team=[]
            if not sales_person:
                return
            sales_team.append({
                "sales_person":sales_person,
                "allocated_percentage":100
            })
            return sales_team
           
        
        customer_doc = frappe.get_doc({
            "doctype": "Customer",
            "salutation": salutation,
            "customer_name": customer_name,
            "mobile_no": mobile_number,
            "email_id": email_address,
            "sales_team":check_sales_person_exists()
        })
        customer_doc.insert(ignore_permissions=True,ignore_mandatory=True)

        address_doc = frappe.get_doc({
            "doctype": "Address",
            "address_title": customer_name,
            "address_line1": address_line1,
            "address_line2": address_line2,
            "city": city,
            "email_id": email_address,  
            "pincode": pincode,
            "state": state,
            "country": country,
            "phone": mobile_number,
            "address_type": "Billing",  
            "links": [{
                "link_doctype": "Customer",
                "link_name": customer_doc.name
            }]
        })
        address_doc.insert(ignore_permissions=True)

        customer_doc.customer_primary_address = address_doc.name
        customer_doc.save()

        return {
            "success": True,
            "customer": customer_doc.name,
            "address": address_doc.name
        }

    except Exception as e:
        frappe.log_error(f"An Error occured while creating the customer: {(e)}")
        return {
            "success": False,
            "error": str(e)
        }
    