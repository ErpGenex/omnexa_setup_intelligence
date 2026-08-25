# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

from __future__ import annotations

import frappe

from omnexa_setup_intelligence.engine.dsl import DSLError, eval_condition
from omnexa_setup_intelligence.engine.facts import build_facts, get_user_company


def _governance_workspaces() -> list[str]:
	"""Public workspace titles for executive governance rollup."""
	try:
		rows = frappe.get_all(
			"Workspace",
			filters={"public": 1, "is_hidden": 0},
			pluck="title",
			order_by="sequence_id asc, title asc",
			limit_page_length=50,
		)
		seen: list[str] = []
		for title in rows or []:
			normalized = (title or "").strip()
			if normalized and normalized not in seen:
				seen.append(normalized)
		if seen:
			return seen
	except Exception:
		pass
	return ["Sales", "Inventory", "Accounts", "Projects", "HR"]


def _action_payload(rule) -> dict:
	t = rule.action_type or "route"
	v = rule.action_value or ""
	if t == "doctype_list":
		return {"label": "Fix now", "type": "route", "value": f"/app/{frappe.scrub(v)}"
	}
	if t == "doctype_new":
		return {"label": "Create", "type": "route", "value": f"/app/{frappe.scrub(v)}/new"
	}
	if t == "report":
		return {"label": "Open report", "type": "route", "value": f"/app/query-report/{frappe.scrub(v)}"
	}
	if t == "settings":
		return {"label": "Open settings", "type": "route", "value": f"/app/{frappe.scrub(v)}"
	}
	# route
	return {"label": "Fix now", "type": "route", "value": v or "/app"
	}


@frappe.whitelist(methods=["POST"])
def get_workspace_checklist(workspace: str | None = None):
	"""Return only missing setup items for the given workspace."""
	if frappe.session.user == "Guest":
		frappe.throw("Login required.", frappe.PermissionError)

	ws = (workspace or "").strip() or "Global"
	company = get_user_company()

	rules = frappe.get_all(
		"Setup Intelligence Rule",
		filters={"enabled": 1, "workspace": ws
	},
		fields=[
			"name",
			"workspace",
			"module",
			"title",
			"message",
			"severity",
			"blocking",
			"company_scoped",
			"condition_dsl",
			"action_type",
			"action_value",
			"order",
		],
		order_by="blocking desc, `order` asc, modified desc",
	)

	items = []
	for r in rules:
		company_scoped = int(r.get("company_scoped") or 0)
		facts = build_facts(company, company_scoped=bool(company_scoped))
		try:
			missing = bool(eval_condition(r.get("condition_dsl"), facts))
		except DSLError:
			# Invalid rule; keep it visible for admins only
			if "System Manager" in (frappe.get_roles() or []):
				missing = True
				r["message"] = (r.get("message") or "") + " (Invalid condition DSL)"
			else:
				missing = False
		if not missing:
			continue
		items.append(
			{
				"id": f"rule:{r.get('name')
	}",
				"title": r.get("title"),
				"message": r.get("message") or "",
				"severity": (r.get("severity") or "medium"),
				"blocking": int(r.get("blocking") or 0),
				"action": _action_payload(frappe._dict(r))
	}
		)

	summary_facts = build_facts(company, company_scoped=True)
	return {
		"ok": True,
		"workspace": ws,
		"company": company,
		"facts": {"count": summary_facts.get("count"), "settings": summary_facts.get("settings")},
		"items": items,
	}


@frappe.whitelist(methods=["GET", "POST"])
def get_executive_governance_summary():
	"""High-level governance score for executive dashboard."""
	if frappe.session.user == "Guest":
		frappe.throw("Login required.", frappe.PermissionError)

	workspaces = _governance_workspaces()
	details = []
	total_missing = 0
	critical = 0
	high = 0

	for ws in workspaces:
		out = get_workspace_checklist(ws)
		items = out.get("items") or []
		total_missing += len(items)
		for x in items:
			sev = (x.get("severity") or "").lower()
			if sev == "critical":
				critical += 1
			elif sev == "high":
				high += 1
		details.append(
			{
				"workspace": ws,
				"missing_items": len(items),
				"top_items": [i.get("title") for i in items[:3]]
	}
		)

	base_score = 100
	score = max(0, base_score - (critical * 20) - (high * 10) - ((total_missing - critical - high) * 3))
	if critical > 0:
		risk = "high"
	elif high > 0 or total_missing > 8:
		risk = "medium"
	else:
		risk = "low"

	return {
		"ok": True,
		"score": score,
		"risk_level": risk,
		"total_missing_items": total_missing,
		"critical_items": critical,
		"high_items": high,
		"workspace_breakdown": details
	}
@frappe.whitelist()
def preview_infra_kpi(scenario: str | None = None, params: str | None = None) -> dict:
	from omnexa_core.omnexa_core.parity_api import preview_infra_kpi as _p
	return _p("setup_intelligence", scenario=scenario, params=params)
