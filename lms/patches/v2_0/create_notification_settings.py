import frappe
from frappe.desk.doctype.notification_settings.notification_settings import create_notification_settings

def execute():
    users = frappe.get_all("User", fields=["name"])

    for user in users:
        create_notification_settings(user.name)

    frappe.cache.delete_key("users_for_mentions")
    frappe.cache.delete_key("enabled_users")
    frappe.db.commit()
