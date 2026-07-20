app_name = "omnexa_setup_intelligence"
app_title = "ErpGenEx Setup Intelligence"
app_publisher = "ErpGenEx"
app_description = "Live setup state analyzer and dynamic checklists"
app_email = "dev@erpgenex.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "omnexa_setup_intelligence",
# 		"logo": "/assets/omnexa_setup_intelligence/logo.png",
# 		"title": "Omnexa Setup Intelligence",
# 		"route": "/omnexa_setup_intelligence",
# 		"has_permission": "omnexa_setup_intelligence.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
	"/assets/omnexa_setup_intelligence/css/workspace_setup_assistant.css",
]
app_include_js = [
	"/assets/omnexa_setup_intelligence/js/workspace_setup_assistant.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/omnexa_setup_intelligence/css/omnexa_setup_intelligence.css"
# web_include_js = "/assets/omnexa_setup_intelligence/js/omnexa_setup_intelligence.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "omnexa_setup_intelligence/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "omnexa_setup_intelligence/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "omnexa_setup_intelligence.utils.jinja_methods",
# 	"filters": "omnexa_setup_intelligence.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "omnexa_setup_intelligence.install.enforce_supported_frappe_version"
before_migrate = "omnexa_setup_intelligence.install.enforce_supported_frappe_version"
after_install = "omnexa_setup_intelligence.install.after_install"

after_migrate = "omnexa_setup_intelligence.install.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "omnexa_setup_intelligence.uninstall.before_uninstall"
# after_uninstall = "omnexa_setup_intelligence.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "omnexa_setup_intelligence.utils.before_app_install"
# after_app_install = "omnexa_setup_intelligence.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "omnexa_setup_intelligence.utils.before_app_uninstall"
# after_app_uninstall = "omnexa_setup_intelligence.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "omnexa_setup_intelligence.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"omnexa_setup_intelligence.tasks.all"
# 	],
# 	"daily": [
# 		"omnexa_setup_intelligence.tasks.daily"
# 	],
# 	"hourly": [
# 		"omnexa_setup_intelligence.tasks.hourly"
# 	],
# 	"weekly": [
# 		"omnexa_setup_intelligence.tasks.weekly"
# 	],
# 	"monthly": [
# 		"omnexa_setup_intelligence.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "omnexa_setup_intelligence.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "omnexa_setup_intelligence.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "omnexa_setup_intelligence.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["omnexa_setup_intelligence.utils.before_request"]
# after_request = ["omnexa_setup_intelligence.utils.after_request"]

# Job Events
# ----------
# before_job = ["omnexa_setup_intelligence.utils.before_job"]
# after_job = ["omnexa_setup_intelligence.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{}",
# 		"filter_by": "{}",
# 		"redact_fields": ["{}", "{}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{}",
# 		"filter_by": "{}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"omnexa_setup_intelligence.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

