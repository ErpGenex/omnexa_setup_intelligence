from frappe.tests.utils import FrappeTestCase

from omnexa_setup_intelligence import hooks


class TestSetupIntelligenceSmoke(FrappeTestCase):
	def test_hooks_are_present(self):
		self.assertEqual(hooks.app_name, "omnexa_setup_intelligence")
		self.assertTrue(any("workspace_setup_assistant" in x for x in (hooks.app_include_js or [])))

