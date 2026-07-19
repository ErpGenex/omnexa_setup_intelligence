// Omnexa Setup Intelligence — Workspace Setup Assistant widget

(function () {
	"use strict";

	function currentWorkspaceName() {
		// Workspace page route is typically /app/<workspace-route>
		// Fallback: use page title.
		try {
			const route = (frappe.get_route && frappe.get_route()) || [];
			if (route[0] === "Workspace" && route[1]) return route[1];
			if (route[0] && typeof route[0] === "string" && route[0] !== "app") return route[0];
		} catch (e) {
			// ignore
		}
		const title = document.querySelector(".page-title .title-text");
		return (title && title.textContent && title.textContent.trim()) || "Global";
	}

	function ensureContainer() {
		// Place at top of page body content
		const page = document.querySelector(".page-container .page-body, .page-body");
		if (!page) return null;
		let el = document.getElementById("omnexa-setup-assistant");
		if (!el) {
			el = document.createElement("div");
			el.id = "omnexa-setup-assistant";
			el.className = "omnexa-setup-assistant";
			page.prepend(el);
		}
		return el;
	}

	function pill(sev) {
		const m = {
			critical: "red",
			high: "orange",
			medium: "blue",
			low: "gray",
		};
		return m[sev] || "gray";
	}

	function render(container, data) {
		const items = (data && data.items) || [];
		if (!items.length) {
			container.innerHTML = "";
			container.style.display = "none";
			return;
		}
		container.style.display = "";
		const rows = items
			.map((x) => {
				const sev = frappe.utils.escape_html((x.severity || "medium").toUpperCase());
				const title = frappe.utils.escape_html(x.title || "");
				const msg = frappe.utils.escape_html(x.message || "");
				const tone = pill((x.severity || "medium").toLowerCase());
				const href = (x.action && x.action.value) || "/app";
				const label = (x.action && x.action.label) || __("Fix now");
				return `
					<div class="omnexa-setup-item">
						<div class="omnexa-setup-item-main">
							<div class="omnexa-setup-item-title">
								<span class="indicator-pill ${tone}">${sev}</span>
								<span>${title}</span>
							</div>
							<div class="omnexa-setup-item-msg text-muted">${msg}</div>
						</div>
						<div class="omnexa-setup-item-actions">
							<button class="btn btn-sm btn-primary" data-route="${encodeURIComponent(href)}">${frappe.utils.escape_html(
					label
				)}</button>
						</div>
					</div>
				`;
			})
			.join("");

		container.innerHTML = `
			<div class="omnexa-setup-card">
				<div class="omnexa-setup-head">
					<div class="omnexa-setup-title">${__("Setup Assistant")}</div>
					<div class="omnexa-setup-sub text-muted">${__("Missing setup items for this workspace (auto-updates).")}</div>
				</div>
				<div class="omnexa-setup-body">${rows}</div>
			</div>
		`;

		container.querySelectorAll("button[data-route]").forEach((btn) => {
			btn.addEventListener("click", () => {
				const route = decodeURIComponent(btn.getAttribute("data-route") || "/app");
				frappe.set_route(route);
			});
		});
	}

	let lastFetch = 0;
	async function refresh() {
		const container = ensureContainer();
		if (!container) return;
		const ws = currentWorkspaceName();
		const now = Date.now();
		if (now - lastFetch < 1000) return;
		lastFetch = now;
		try {
			const r = await frappe.call({
				method: "omnexa_setup_intelligence.api.get_workspace_checklist",
				args: { workspace: ws },
				freeze: false,
			});
			render(container, r.message || {});
		} catch (e) {
			// keep quiet
		}
	}

	function hookRouting() {
		// Refresh on app ready and on route changes
		$(document).on("app_ready", () => refresh());
		$(document).on("workspace-rendered", () => refresh());
		const orig = frappe.router && frappe.router.set_route;
		if (orig && !window._omnexa_setup_intelligence_route_patch) {
			window._omnexa_setup_intelligence_route_patch = true;
			frappe.router.set_route = function (...args) {
				const p = orig.apply(frappe.router, args);
				setTimeout(refresh, 300);
				return p;
			};
		}
		// light polling
		setInterval(refresh, 60000);
	}

	function mount_workspace_setup_assistant() {
		if (!window.frappe || !frappe.boot || frappe.session.user === "Guest") return;
		// Skip setup wizard routes to avoid noise before core defaults are initialized.
		if ((window.location.pathname || "").indexOf("/app/setup-wizard") === 0) return;
		if (window.__workspace_setup_assistant_mounted) return;
		window.__workspace_setup_assistant_mounted = true;
		hookRouting();
		refresh();
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", mount_workspace_setup_assistant);
	} else {
		mount_workspace_setup_assistant();
	}
	$(window).on("load", mount_workspace_setup_assistant);
})();

