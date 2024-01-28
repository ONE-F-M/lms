import frappe
def execute():
    lessons = frappe.get_all("Course Lesson",{'question':['is','set'],'lms_assignment':['is','not set']},['question','file_type','title','name'])
    if lessons:
        for each in lessons:
            assignment = frappe.get_doc({
                'doctype':"LMS Assignment",
                'title':lessons[0].title,
                'question':lessons[0].question,
                'type':lessons[0].file_type
            }).insert()
            frappe.db.set_value("Course Lesson",each.name,'lms_assignment',assignment.name)
            frappe.db.commit()
        