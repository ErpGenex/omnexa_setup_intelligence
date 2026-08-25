# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

from __future__ import annotations

import frappe

SUPPORTED_FRAPPE_MAJOR = 15


def enforce_supported_frappe_version():
	"""Fail fast when running on unsupported Frappe major versions."""
	version_text = (getattr(frappe, "__version__", "") or "").strip()
	if not version_text:
		return

	major_token = version_text.split(".", 1)[0]
	try:
		major = int(major_token)
	except ValueError:
		return

	if major != SUPPORTED_FRAPPE_MAJOR:
		frappe.throw(
			f"Unsupported Frappe version '{version_text}' for omnexa_setup_intelligence. "
			"Supported range is >=15.0,<16.0.",
			frappe.ValidationError,
		)


def after_install():
	seed_default_rules()


def after_migrate():
	# idempotent
	seed_default_rules()


def seed_default_rules():
	"""Seed a minimal, high-value rule set (idempotent)."""
	if not _ensure_rule_doctype_ready():
		return

	rules = [
		{
			"workspace": "Sales",
			"module": "Sales",
			"governance_code": "SI-GOV-SALES-CUSTOMER-MASTER",
			"title": "Customer master is empty",
			"message": "Create at least one Customer to start Sales transactions.",
			"severity": "high",
			"blocking": 1,
			"company_scoped": 1,
			"condition_dsl": "count.Customer == 0",
			"action_type": "route",
			"action_value": "/app/customer",
			"order": 10
	},
		{
			"workspace": "Sales",
			"module": "Sales",
			"governance_code": "SI-GOV-SALES-FIRST-INVOICE",
			"title": "Sales process not started",
			"message": "No Sales Invoice exists yet. Post at least one invoice to validate revenue flow.",
			"severity": "medium",
			"blocking": 0,
			"company_scoped": 1,
			"condition_dsl": "count.Sales Invoice == 0",
			"action_type": "route",
			"action_value": "/app/sales-invoice",
			"order": 20
	},
		{
			"workspace": "Inventory",
			"module": "Inventory",
			"governance_code": "SI-GOV-INV-WAREHOUSE",
			"title": "No warehouses defined",
			"message": "Define at least one Warehouse to enable stock operations and valuation.",
			"severity": "high",
			"blocking": 1,
			"company_scoped": 1,
			"condition_dsl": "count.Warehouse == 0",
			"action_type": "route",
			"action_value": "/app/warehouse",
			"order": 10
	},
		{
			"workspace": "Inventory",
			"module": "Inventory",
			"governance_code": "SI-GOV-INV-ITEM-MASTER",
			"title": "Item master is empty",
			"message": "Create Items before you can buy, sell, or manage stock.",
			"severity": "high",
			"blocking": 1,
			"company_scoped": 1,
			"condition_dsl": "count.Item == 0",
			"action_type": "route",
			"action_value": "/app/item",
			"order": 20
	},
		{
			"workspace": "Accounts",
			"module": "Accounts",
			"governance_code": "SI-GOV-ACC-SUPPLIER-MASTER",
			"title": "Supplier master is empty",
			"message": "Create at least one Supplier to start procurement and payables flow.",
			"severity": "medium",
			"blocking": 0,
			"company_scoped": 1,
			"condition_dsl": "count.Supplier == 0",
			"action_type": "route",
			"action_value": "/app/supplier",
			"order": 20
	},
		{
			"workspace": "Accounts",
			"module": "Accounts",
			"governance_code": "SI-GOV-ACC-DEFAULT-COMPANY",
			"title": "Default company is not set",
			"message": "Set a default company in System Settings to ensure company-scoped setup works correctly.",
			"severity": "medium",
			"blocking": 0,
			"company_scoped": 0,
			"condition_dsl": "settings.Global Defaults.default_company is empty",
			"action_type": "settings",
			"action_value": "System Settings",
			"order": 30
	},
		{
			"workspace": "Accounts",
			"module": "Accounts",
			"governance_code": "SI-GOV-ACC-FIRST-PINV",
			"title": "Procurement accounting not started",
			"message": "No Purchase Invoice exists yet. Post one to validate payables and expense recognition.",
			"severity": "medium",
			"blocking": 0,
			"company_scoped": 1,
			"condition_dsl": "count.Purchase Invoice == 0",
			"action_type": "route",
			"action_value": "/app/purchase-invoice",
			"order": 40
	},
	]

	for r in rules:
		existing = frappe.db.get_value(
			"Setup Intelligence Rule",
			{"workspace": r["workspace"], "title": r["title"]},
			"name",
		)
		if existing:
			doc = _safe_get_doc("Setup Intelligence Rule", existing)
			if not doc:
				continue
			doc.update(r)
			doc.save(ignore_permissions=True)
		else:
			doc = _safe_get_doc({"doctype": "Setup Intelligence Rule", **r})
			if not doc:
				continue
			doc.insert(ignore_permissions=True)

	seed_activity_rule_packs()


ACTIVITY_RULE_PACKS: dict[str, list[dict]] = {
	"Healthcare": [
		{
			"workspace": "Healthcare",
			"module": "Healthcare",
			"governance_code": "SI-GOV-HC-PATIENT-MASTER",
			"title": "Healthcare patient master is empty",
			"message": "Register at least one Healthcare Patient before clinical workflows.",
			"severity": "high",
			"blocking": 1,
			"company_scoped": 1,
			"condition_dsl": "count.Healthcare Patient == 0",
			"action_type": "route",
			"action_value": "/app/healthcare-patient",
			"order": 10,
		},
	],
	"Hotel Assets": [
		{
			"workspace": "Assets",
			"module": "Fixed Assets",
			"governance_code": "SI-GOV-HOTEL-ASSET-REGISTER",
			"title": "Fixed asset register is empty",
			"message": "Create hotel room and equipment assets to enable maintenance and RFID tracking.",
			"severity": "high",
			"blocking": 1,
			"company_scoped": 1,
			"condition_dsl": "count.Asset == 0",
			"action_type": "route",
			"action_value": "/app/asset",
			"order": 10,
		},
	],
	"Construction": [
		{
			"workspace": "Projects",
			"module": "Construction",
			"governance_code": "SI-GOV-CON-PROJECT-MASTER",
			"title": "No construction projects defined",
			"message": "Create a Project to track contracts, BOQ, and site progress.",
			"severity": "high",
			"blocking": 1,
			"company_scoped": 1,
			"condition_dsl": "count.Project == 0",
			"action_type": "route",
			"action_value": "/app/project",
			"order": 10,
		},
	],
	"Financial Services": [
		{
			"workspace": "Accounts",
			"module": "Finance",
			"governance_code": "SI-GOV-FIN-CUSTOMER-MASTER",
			"title": "Finance customer portfolio is empty",
			"message": "Onboard at least one Customer before loan or treasury operations.",
			"severity": "high",
			"blocking": 1,
			"company_scoped": 1,
			"condition_dsl": "count.Customer == 0",
			"action_type": "route",
			"action_value": "/app/customer",
			"order": 5,
		},
	],
	"Education": [
		{
			"workspace": "Education",
			"module": "Education",
			"governance_code": "SI-GOV-EDU-CUSTOMER-MASTER",
			"title": "Student/parent billing master is empty",
			"message": "Create Customers (students or guardians) before fee billing.",
			"severity": "medium",
			"blocking": 0,
			"company_scoped": 1,
			"condition_dsl": "count.Customer == 0",
			"action_type": "route",
			"action_value": "/app/customer",
			"order": 10,
		},
	],
}


def _condition_doctype(condition_dsl: str) -> str | None:
	if not condition_dsl or not condition_dsl.startswith("count."):
		return None
	return condition_dsl[len("count.") :].split("==")[0].strip()


def seed_activity_rule_packs():
	"""Seed vertical setup rules per company business activity (idempotent)."""
	if not _ensure_rule_doctype_ready():
		return

	installed = set(frappe.get_installed_apps() or [])
	for company in frappe.get_all("Company", pluck="name"):
		try:
			from omnexa_core.omnexa_core.activity_labels import resolve_company_activity_raw

			activity = resolve_company_activity_raw(company)
		except Exception:
			continue
		pack = ACTIVITY_RULE_PACKS.get(activity) or []
		for rule in pack:
			doctype = _condition_doctype(rule.get("condition_dsl") or "")
			if doctype and not frappe.db.exists("DocType", doctype):
				continue
			if rule.get("module") == "Healthcare" and "omnexa_healthcare" not in installed:
				continue
			if rule.get("module") == "Fixed Assets" and "omnexa_fixed_assets" not in installed:
				continue
			existing = frappe.db.get_value(
				"Setup Intelligence Rule",
				{"governance_code": rule.get("governance_code")},
				"name",
			)
			if existing:
				doc = _safe_get_doc("Setup Intelligence Rule", existing)
				if not doc:
					continue
				doc.update(rule)
				doc.save(ignore_permissions=True)
			else:
				doc = _safe_get_doc({"doctype": "Setup Intelligence Rule", **rule})
				if not doc:
					continue
				doc.insert(ignore_permissions=True)


def _ensure_rule_doctype_ready() -> bool:
	"""Ensure Setup Intelligence Rule DocType is available during fresh installs."""
	if frappe.db.exists("DocType", "Setup Intelligence Rule"):
		return True

	try:
		frappe.reload_doc("omnexa_setup_intelligence", "doctype", "setup_intelligence_rule")
	except Exception:
		frappe.log_error(frappe.get_traceback(), "Setup Intelligence: reload setup_intelligence_rule failed")

	if frappe.db.exists("DocType", "Setup Intelligence Rule"):
		return True

	frappe.log_error(
		"Setup Intelligence Rule DocType is unavailable during seed_default_rules; skipped seeding.",
		"Setup Intelligence: DocType not ready",
	)
	return False


def _safe_get_doc(*args, **kwargs):
	"""Get doc with one recovery attempt if controller import is not ready yet."""
	try:
		return frappe.get_doc(*args, **kwargs)
	except ImportError:
		if not _ensure_rule_doctype_ready():
			return None
		try:
			return frappe.get_doc(*args, **kwargs)
		except Exception:
			frappe.log_error(frappe.get_traceback(), "Setup Intelligence: get_doc failed after reload")
			return None

