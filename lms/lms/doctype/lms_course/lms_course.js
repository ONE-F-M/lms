// Copyright (c) 2021, FOSS United and contributors
// For license information, please see license.txt

frappe.ui.form.on("LMS Course", {
	onload: function (frm) {
		frm.set_query("chapter", "chapters", function () {
			return {
				filters: {
					course: frm.doc.name,
				},
			};
		});

		frm.set_query("course", "related_courses", function () {
			return {
				filters: {
					published: true,
				},
			};
		});
	},
	refresh: (frm) => {
		add_web_link(frm);
		set_currency(frm);
		re_enroll_members(frm);
	},
});

const add_web_link = (frm) =>
	frm.add_web_link(`/courses/${frm.doc.name}`, "See on Website");

const set_currency = (frm) => {
	if (!frm.doc.currency)
		frappe.db
			.get_single_value("LMS Settings", "default_currency")
			.then((value) => {
				frm.set_value("currency", value);
			});
};

const re_enroll_members = (frm) => {
	if (frm.doc.allow_reenrollments) {
		frm.add_custom_button(
			__("All Members"),
			() => re_enroll_all_members(frm),
			__("Re-Enroll")
		);
		frm.add_custom_button(
			__("Single Member"),
			() => re_enroll_single_member(frm),
			__("Re-Enroll")
		);
	}
};

const re_enroll_all_members = (frm) => {
	frappe.confirm(
		"Are you sure you want to re-enroll all members?",
		() => {
			  frappe.call({
				method: "lms.lms.doctype.lms_course.lms_course.re_enroll_all_members",
				freeze: true,
				freeze_message: "Re-enrolling all members",
				args: { course: frm.doc.name },
				callback: function (r) {
				  if (r.message == "OK") {
					frappe.msgprint(
					  "All members re-enrolled successfully"
					);
				  }
				},
			  });
		},
		() => null
	);
};

const re_enroll_single_member = function (frm) {
	const dialog = new frappe.ui.Dialog({
		title: __("Re-Enroll Member"),
		fields: [
			{
				fieldtype: "Link",
				label: __("User"),
				fieldname: "user",
				options: "User",
				reqd: 1,
			},
		],
	});
	dialog.set_primary_action(__("Create"), function () {
		const data = dialog.get_values();
		if (!data) return;
		
		frappe.call({
			method: "lms.lms.doctype.lms_course.lms_course.re_enroll_single_member",
			freeze: true,
			freeze_message: "Re-enrolling member",
			args: { course: frm.doc.name, member: data.user },
			callback: function (r) {
				dialog.hide();
			  if (r.message == "OK") {
				frappe.msgprint(
				  "Member re-enrolled successfully"
				);
			  }
			},
		  });
	});
	dialog.show();
};
