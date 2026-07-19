# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document


class SetupIntelligenceRule(Document):
	"""Rule document (data only). Evaluation is done by the engine service."""

	def validate(self):
		self.workspace = (self.workspace or "").strip()
		self.module = (self.module or "").strip() or None
		self.title = (self.title or "").strip()
		self.message = (self.message or "").strip() or None
		self.condition_dsl = (self.condition_dsl or "").strip()
		self.action_value = (self.action_value or "").strip() or None
		self._validate_lifecycle_controls()

	def _validate_lifecycle_controls(self):
		if not self.enabled:
			return
		if not self.governance_code:
			frappe.throw(_("Governance Code is mandatory for enabled rules."), title=_("Governance"))
		if self.severity in {"high", "critical"} and not self.blocking:
			frappe.throw(_("High/Critical rules must be marked as Blocking."), title=_("Policy"))
		if self.action_type in {"route", "doctype_list", "doctype_new", "report", "settings"} and not self.action_value:
			frappe.throw(_("Action Value is mandatory for the selected Action Type."), title=_("Action"))

