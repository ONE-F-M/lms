import frappe


def execute():
    create_assignment_completion_eod_template()
    create_quiz_submission_eod_template()
    create_course_completion_eod_template()
    set_default_eod_templates()
    frappe.db.commit()

def create_assignment_completion_eod_template():
    if not frappe.db.exists("Email Template", "Daily Assignment Completion"):
        doc = frappe.new_doc("Email Template")
        doc.name = "Daily Assignment Completion"
        doc.use_html = 1
        doc.subject = "Daily Assignment Submission Information"
        template = """
        <!--
            Available data format -> 
            {
                'assignment_title': 'Assignment Title', 
                'members': [{
                    'member': 'John Doe', 
                    'assignment_submission': 'ASG-SUB-XXXXX', 
                    'assignment_title': 'Assignment Title'
                }]
            }
        -->
        <p>
            {{ _("The following trainees have submitted their assignments.") }}
        </p>
        <br>
        <table class="table table-bordered table-condensed">
            <thead>
            <tr>
            <th class="text-center">SI No.</th>
            <th class="text-center">ID Number</th>
            <th class="text-center">Trainee Name</th>
            <th class="text-center">Course Name</th>
            <th class="text-center">Assignment Topic</th>
            <th class="text-center">Submission Date</th>
            </tr>
        </thead>
        <tbody>
            {% for member in members %}
                {% set user = frappe.db.get_value("User", member.member_id, ["username"], as_dict=True) %}
                {% set course = frappe.db.get_value("LMS Course", member["course"], ["title", "name", "image"], as_dict=True) %}    
                {% set submission_date = frappe.db.get_value("LMS Assignment Submission", member["assignment_submission"], ["creation"], as_dict=True) %}    
                <tr>
                <td class="text-center">{{ loop.index }}</th>
                <td class="text-center">{{ user.username }}</th>
                <td class="text-center">{{ member['member'] }}</td>
                <td class="text-center">{{ course.title }}</td>
                <td class="text-center"><a href="app/lms-assignment-submission/{{ member['assignment_submission'] }}">{{ assignment_title }}</a></td>
                <td class="text-center">{{ frappe.format(submission_date['creation'], {'fieldtype': 'Date'}) }}</td>
                </tr>
            {% endfor %}
        </tbody>
        </table>
        """
        doc.response_html = template
        doc.insert()


def create_quiz_submission_eod_template():
    if not frappe.db.exists("Email Template", "Daily Quiz Submission"):
        doc = frappe.new_doc("Email Template")
        doc.name = "Daily Quiz Submission"
        doc.use_html = 1
        doc.subject = "Daily Quiz Submission Information"
        template = """
            <!--
                Available data format -> 
                {
                    'course': 'avsec-awareness-awareness-course', 
                    'quiz' 'Security Awareness Course Evaluation',
                    'members': [{'member': 'John Doe', 'member_id': 'johndoe@gmail.com', 'quiz_submission': '4645asa23', 'score': 87, 'result': 'PASS'}], 
                    'names': ['4645asa23']  (IDs of LMS Quiz submission)
                }
            -->
            {% set date = frappe.format_date(frappe.utils.today()) %}
            {% set course = frappe.db.get_value("LMS Course", course, ["title", "name", "image"], as_dict=True) %}    
            <p>
                {{ _("The following trainees have submitted their quiz.") }}
            </p>
            <br>
            <table class="table table-bordered table-condensed">
                <thead>
                <tr>
                <th class="text-center">SI No.</th>
                <th class="text-center">ID Number</th>
                <th class="text-center">Trainee Name</th>
                <th class="text-center">Course Name</th>
                <th class="text-center">Quiz Submission</th>
                <th class="text-center">Evaluation Score</th>
                <th class="text-center">Result</th>
                <th class="text-center">Date of Submission</th>
                </tr>
            </thead>
            <tbody>
                {% for member in members %}
                    {% set quiz = frappe.db.get_value("LMS Quiz Submission", member.quiz_submission, ["creation", "quiz"], as_dict=True) %}
                    {% set user = frappe.db.get_value("User", member.member_id, ["username"], as_dict=True) %}
                    <tr>
                    <td class="text-center">{{ loop.index }}</th>
                    <td class="text-center">{{ user.username }}</th>
                    <td class="text-center">{{ member.member }}</td>
                    <td class="text-center">{{ course.title }}</td>
                    <td class="text-center">
                        <a href="app/lms-quiz-submission/{{ member['quiz_submission'] }}">
                        {{ frappe.db.get_value("LMS Quiz", quiz.quiz, "title")}}
                        </a>
                    </td>
                    <td class="text-center">{{ member.score }}</td>
                    <td class="text-center">{{ member.result }}</td>
                    <td class="text-center">{{ frappe.format(quiz['creation'], {'fieldtype': 'Date'}) }}</td>
                    </tr>
                {% endfor %}
            </tbody>
            </table>
        """
        doc.response_html = template
        doc.insert()


def create_course_completion_eod_template():
    if not frappe.db.exists("Email Template", "Course Completion"):
        doc = frappe.new_doc("Email Template")
        doc.name = "Course Completion"
        doc.use_html = 1
        doc.subject = "Course Completion Notification"
        template = """
            <!--
                Available data format -> 
                {
                    'course': 'avsec-awareness-awareness-course', 
                    'members': ['John Doe', 'Jane Doe'], 
                    'names': ['6d20f46457', '99b4102534']  (IDs of LMS Enrollment)
                }
            -->
            {% set date = frappe.format_date(frappe.utils.today()) %}
            {% set course = frappe.db.get_value("LMS Course", course, ["title", "name", "image"], as_dict=True) %}    
            <p>
                {{ _("The following trainees have successfully completed the course {0} on {1}").format(frappe.bold(course_name), date) }}
            </p>
            <br>
            <table class="table table-bordered table-condensed">
                <thead>
                <tr>
                <th class="text-center">SI No.</th>
                <th class="text-center">ID Number</th>
                <th class="text-center">Trainee Name</th>
                <th class="text-center">Course Name</th>
                </tr>
            </thead>
            <tbody>
                {% for member in members %}
                {% set user = frappe.db.get_value("User", member, ["full_name", "username"], as_dict=True) %}    
                    <tr>
                    <td class="text-center">{{ loop.index }}</th>
                    <td class="text-center">{{ user.username }}</th>
                    <td class="text-center">{{ user.full_name }}</td>
                    <td class="text-center">{{ course.title }}</td>
                    </tr>
                {% endfor %}
            </tbody>
            </table>
        """
        doc.response_html = template
        doc.insert()


def set_default_eod_templates():
    frappe.db.set_value("LMS Settings", None, "assignment_submission_template", "Daily Assignment Completion")
    frappe.db.set_value("LMS Settings", None, "course_completion_notification_template", "Course Completion")
    frappe.db.set_value("LMS Settings", None, "quiz_submission_template", "Daily Quiz Submission")
    