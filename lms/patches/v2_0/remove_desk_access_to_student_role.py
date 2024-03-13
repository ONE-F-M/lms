import frappe

def execute():
    has_desk_acess = frappe.db.get_value("Role", "LMS Student", "desk_access")
    if has_desk_acess:
        frappe.db.set_value("Role", "LMS Student", "desk_access", 0)
        frappe.db.commit()