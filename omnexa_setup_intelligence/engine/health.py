# Copyright (c) 2026, Omnexa and contributors
# License: MIT

"""Daily setup health snapshot for Setup Intelligence."""

from __future__ import annotations

import frappe

from omnexa_setup_intelligence.api import get_executive_governance_summary


def publish_setup_health_snapshot() -> dict:
	"""Evaluate setup health across public workspaces and log to Error Log."""
	summary = get_executive_governance_summary()
	payload = {
		"score": summary.get("score", 0),
		"risk_level": summary.get("risk_level"),
		"total_missing_items": summary.get("total_missing_items", 0),
		"critical_items": summary.get("critical_items", 0),
		"high_items": summary.get("high_items", 0),
		"workspaces": len(summary.get("workspace_breakdown") or []),
	}
	frappe.log_error(
		title="Setup Intelligence Daily Health",
		message=frappe.as_json(payload, indent=0),
	)
	return payload
