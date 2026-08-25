frappe.pages["si-executive-dashboard"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({ parent: wrapper, title: __("Setup Intelligence Executive"), single_column: true });
	frappe.call({
		method: "omnexa_setup_intelligence.api.get_executive_governance_summary",
		callback(r) {
			const s = r.message || {};
			const rows = (s.workspace_breakdown || [])
				.map((w) => `<tr><td>${frappe.utils.escape_html(w.workspace)}</td><td>${w.missing_items}</td></tr>`)
				.join("");
			$(page.body).html(`
				<div class="p-4">
					<h4>${__("Governance Score")}: <b>${s.score || 0}</b>/100</h4>
					<p>${__("Risk")}: ${s.risk_level || "-"} | ${__("Missing")}: ${s.total_missing_items || 0}</p>
					<table class="table table-bordered table-sm"><thead><tr><th>${__("Workspace")}</th><th>${__("Missing")}</th></tr></thead><tbody>${rows}</tbody></table>
				</div>`);
		},
	});
};
