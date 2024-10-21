import frappe



@frappe.whitelist()
def create_user_permission(docName,userName,doctype):
    permission_doc=frappe.get_doc({
        "doctype":"User Permission",
        "user":userName,
        "for_value":docName,
        "allow":doctype
    })
    permission_doc.save()