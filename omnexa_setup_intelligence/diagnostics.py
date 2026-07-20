# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

from __future__ import annotations

import frappe


def doctype_status():
	return {
		"setup_rule_doctype_exists": bool(frappe.db.exists("DocType", "Setup Intelligence Rule")),
		"setup_rule_table_exists": bool(frappe.db.table_exists("Setup Intelligence Rule"))
	}

