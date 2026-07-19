# Copyright (c) 2026, Omnexa
from frappe.tests.utils import FrappeTestCase
from omnexa_setup_intelligence.si_gap_register import GLOBAL_LEADER_TARGET, get_gap_status
from omnexa_setup_intelligence.si_global_benchmark import get_global_si_score

class TestSiGlobalBenchmark(FrappeTestCase):
	def test_global_score(self):
		s = get_global_si_score()
		self.assertGreaterEqual(s["weighted_score"], GLOBAL_LEADER_TARGET)
		self.assertTrue(s.get("global_leader_gate"))

	def test_gaps_closed(self):
		self.assertTrue(get_gap_status()["global_leader_gate"])
