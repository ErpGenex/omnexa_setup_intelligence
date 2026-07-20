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
	user = frappe.session.user
	if not user or user == "Guest":
		return None
	try:
		co = frappe.defaults.get_user_default("Company", user=user)
	except Exception:
		co = None
	if co:
		return co
	return _safe_default_company()


def build_facts(company: str | None = None) -> dict:
	"""Build a safe facts dict for DSL evaluation.

	No SQL, no dynamic execution. Only counts/existence and selected settings.
	"""
	company = company or get_user_company()

	count = {}
	def _count(doctype: str) -> int:
		try:
			return int(frappe.db.count(doctype))
		except Exception:
			return 0

	for dt in (
		"Company",
		"Customer",
		"Supplier",
		"Item",
		"Warehouse",
		"Sales Invoice",
		"Purchase Invoice",
	):
		count[dt] = _count(dt)

	settings = {}
	settings["Global Defaults.default_company"] = _safe_default_company()

	out = {
		"company": company,
		"count": count,
		"settings": settings
	}
	return out

