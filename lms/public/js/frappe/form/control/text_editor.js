import Quill from "quill";

const font_families = ['serif', 'sansserif', 'monospace'];

frappe.ui.form.ControlTextEditor = class ControlTextEditor extends frappe.ui.form.ControlTextEditor {
	make_quill_editor() {
		// Attribute customizations must be defined before initialization of Quill editor
		const Font = Quill.import("attributors/style/font");
		Font.whitelist = font_families;
		Quill.register(Font, true);

		super.make_quill_editor();
	}

	get_toolbar_options() {
		const options = super.get_toolbar_options();

		// Inserting font family option in toolbar options array
		options.splice(1, 0, [{ font: font_families }]);

		return options;
	}
};
