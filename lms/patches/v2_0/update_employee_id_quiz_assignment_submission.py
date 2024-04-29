import frappe

def execute():
    # Update Employee IDs in LMS Quiz Submission doctype
    quiz_submissions = frappe.get_all("LMS Quiz Submission", ["name", "member"])
    for submission in quiz_submissions:
        update_record("LMS Quiz Submission", submission.name, submission.member)
    # Update Employee IDs in LMS Assignment Submission doctype
    assignment_submissions = frappe.get_all("LMS Assignment Submission", ["name", "member"])
    for submission in assignment_submissions:
        update_record("LMS Assignment Submission", submission.name, submission.member)


def update_record(doctype, docname, user):
    employee_id = frappe.get_value("User", user, "username")
    frappe.db.set_value(doctype, docname, "custom_employee_id", employee_id)

