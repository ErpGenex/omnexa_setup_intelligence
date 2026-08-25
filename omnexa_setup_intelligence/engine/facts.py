# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

from __future__ import annotations

import frappe


def _safe_default_company() -> str | None:
	"""Return default company only when Global Defaults doctype exists."""
	try:
		if not frappe.db.exists("DocType", "Global Defaults"):
			return None
		return frappe.db.get_single_value("Global Defaults", "default_company")
	except Exception:
		return None


def get_user_company() -> str | None:
	"""Effective company for setup intelligence (navbar context or user default)."""
	user = frappe.session.user
	if not user or user == "Guest":
		return None
	try:
		from omnexa_core.omnexa_core.session_context import get_effective_company

		co = get_effective_company(user)
		if co:
			return co
	except Exception:
		pass
	try:
		co = frappe.defaults.get_user_default("Company", user=user)
	except Exception:
		co = None
	if co:
		return co
	return _safe_default_company()


def _count_doctype(doctype: str, company: str | None) -> int:
	"""Count rows, scoped by company when the doctype has a company column."""
	try:
		filters = {}
		if company and frappe.db.has_column(doctype, "company"):
			filters["company"] = company
		return int(frappe.db.count(doctype, filters))
	except Exception:
		return 0


def build_facts(company: str | None = None, *, company_scoped: bool = True) -> dict:
	"""Build a safe facts dict for DSL evaluation.

	No SQL, no dynamic execution. Only counts/existence and selected settings.
	When ``company_scoped`` is True and a company is resolved, counts filter by company.
	"""
	company = company or get_user_company()
	use_company_filter = bool(company_scoped and company)

	count = {}
	for dt in (
		"Company",
		"Customer",
		"Supplier",
		"Item",
		"Warehouse",
		"Sales Invoice",
		"Purchase Invoice",
		"Healthcare Patient",
		"Asset",
		"Project",
	):
		if not frappe.db.exists("DocType", dt):
			continue
		count[dt] = _count_doctype(dt, company if use_company_filter else None)

	settings = {}
	settings["Global Defaults.default_company"] = _safe_default_company()

	return {
		"company": company,
		"count": count,
		"settings": settings,
	}
