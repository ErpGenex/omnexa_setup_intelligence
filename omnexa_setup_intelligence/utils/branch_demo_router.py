"""Branch demo action router — vertical demo seeds scoped to one branch."""

from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import cint

from omnexa_core.omnexa_core.company_activity_utils import first_company_activity_value


def _assert_system_manager() -> None:
	if "System Manager" not in (frappe.get_roles() or []) and frappe.session.user != "Administrator":
		frappe.throw(_("Not permitted"), frappe.PermissionError)


def _resolve_branch_demo_activity(branch_doc) -> str:
	activity = (branch_doc.get("branch_demo_activity") or "").strip()
	if activity:
		return activity
	return first_company_activity_value(branch_doc.company)


def run_demo_action_for_branch(branch_doc, action_key: str, **kwargs) -> dict:
	_assert_system_manager()
	company = branch_doc.company
	branch = branch_doc.name
	if not company or not branch:
		frappe.throw(_("Branch and company are required"))

	key = (action_key or "").strip()
	activity = _resolve_branch_demo_activity(branch_doc)

	if key == "seed_masters":
		from omnexa_accounting.utils.production_readiness import seed_activity_demo_data

		return seed_activity_demo_data(company, branch=branch, activity=activity, include_transactions=0)

	if key == "seed_with_tx":
		from omnexa_accounting.utils.production_readiness import seed_activity_demo_data

		return seed_activity_demo_data(company, branch=branch, activity=activity, include_transactions=1)

	if key == "construction_portfolio":
		from omnexa_construction.utils.demo_seed import seed_construction_portfolio_demo

		return seed_construction_portfolio_demo(company, branch=branch, force=kwargs.get("force", 0))

	if key == "hotel_assets":
		from omnexa_fixed_assets.api import seed_hotel_demo_assets_from_company

		return seed_hotel_demo_assets_from_company(
			company=company,
			branch=branch,
			count=kwargs.get("count", cint(branch_doc.get("branch_demo_hotel_assets_count")) or 50),
			guest_floors=kwargs.get("guest_floors", 6),
			guest_rooms_per_floor=kwargs.get("guest_rooms_per_floor", 20),
			with_transfer=kwargs.get("with_transfer", 1),
			with_rfid=kwargs.get("with_rfid", 1),
		)

	if key == "healthcare_hospital":
		if "omnexa_healthcare" not in (frappe.get_installed_apps() or []):
			frappe.throw(
				_("Install and migrate omnexa_healthcare on this site, then reload the Branch form."),
				title=_("Healthcare demo"),
			)
		from omnexa_healthcare.utils.branch_demo_seed import seed_healthcare_hospital_demo

		return seed_healthcare_hospital_demo(
			company=company,
			branch=branch,
			patients=kwargs.get("patients", cint(branch_doc.get("branch_demo_healthcare_patients")) or 20),
			force=kwargs.get("force", cint(branch_doc.get("branch_demo_healthcare_force"))),
			include_financial=kwargs.get(
				"include_financial", cint(branch_doc.get("branch_demo_healthcare_financial") or 1)
			),
		)

	if key == "finance_group":
		from omnexa_core.omnexa_core.finance_demo.finance_branch_demo_seed import seed_finance_group_branch_demo

		return seed_finance_group_branch_demo(
			company=company,
			branch=branch,
			customers=kwargs.get("customers", cint(branch_doc.get("branch_demo_finance_customers")) or 50),
			sync_roles=kwargs.get("sync_roles", cint(branch_doc.get("branch_demo_finance_sync_roles") or 1)),
			force=kwargs.get("force", cint(branch_doc.get("branch_demo_finance_force") or 0)),
		)

	if key == "education":
		if "omnexa_education" not in (frappe.get_installed_apps() or []):
			frappe.throw(
				_("Install and migrate omnexa_education on this site, then reload the Branch form."),
				title=_("Education demo"),
			)
		from omnexa_education.education_demo.branch_demo_seed import seed_education_branch_demo

		return seed_education_branch_demo(
			company=company,
			branch=branch,
			institution_type=kwargs.get(
				"institution_type", branch_doc.get("branch_demo_education_institution_type") or "All 5 Types"
			),
			seed_roles=kwargs.get("seed_roles", cint(branch_doc.get("branch_demo_education_seed_roles") or 1)),
			sync_laravel=kwargs.get("sync_laravel", cint(branch_doc.get("branch_demo_education_sync_laravel") or 0)),
		)

	if key == "reset_dry":
		from omnexa_accounting.utils.production_readiness import reset_transactions

		return reset_transactions(company, branch=branch, dry_run=1)

	if key == "reset_execute":
		from omnexa_accounting.utils.production_readiness import enqueue_reset_transactions

		return enqueue_reset_transactions(company, branch=branch, limit=0, batch_size=200)

	frappe.throw(_("Unknown branch demo action: {0}").format(key))
