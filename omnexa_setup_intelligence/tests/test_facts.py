# Copyright (c) 2026, Omnexa
import frappe
from frappe.tests.utils import FrappeTestCase

from omnexa_setup_intelligence.api import _governance_workspaces, get_executive_governance_summary
from omnexa_setup_intelligence.engine.facts import build_facts, get_user_company


class TestSetupIntelligenceFacts(FrappeTestCase):
	def test_get_user_company_uses_effective_company(self):
		company = get_user_company()
		if company:
			self.assertTrue(frappe.db.exists("Company", company))

	def test_build_facts_company_scoped_vs_global(self):
		company = get_user_company()
		scoped = build_facts(company, company_scoped=True)
		global_facts = build_facts(company, company_scoped=False)
		self.assertIn("count", scoped)
		self.assertIn("count", global_facts)
		if company and frappe.db.has_column("Customer", "company"):
			self.assertLessEqual(scoped["count"].get("Customer", 0), global_facts["count"].get("Customer", 0))

	def test_governance_workspaces_not_empty(self):
		workspaces = _governance_workspaces()
		self.assertTrue(workspaces)
		self.assertTrue(all(isinstance(w, str) and w.strip() for w in workspaces))

	def test_executive_governance_summary(self):
		out = get_executive_governance_summary()
		self.assertTrue(out.get("ok"))
		self.assertIn("score", out)
		self.assertIn("workspace_breakdown", out)
		self.assertTrue(len(out.get("workspace_breakdown") or []) >= 1)
