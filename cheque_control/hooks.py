# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "cheque_control"
app_title = "Cheque Control"
app_publisher = "MostafaFekry"
app_description = "For controlling receivable and payable cheques"
app_icon = "octicon octicon-repo"
app_color = "grey"
app_email = "mostafa.fekry@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cheque_control/css/cheque_control.css"
# app_include_js = "/assets/cheque_control/js/cheque_control.js"

# include js, css files in header of web template
# web_include_css = "/assets/cheque_control/css/cheque_control.css"
# web_include_js = "/assets/cheque_control/js/cheque_control.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "cheque_control.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cheque_control.install.before_install"
# after_install = "cheque_control.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cheque_control.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
    "Payment Entry": {
        "on_submit": "cheque_control.api.pe_on_submit",
        "before_submit": "cheque_control.api.pe_before_submit",
        "on_cancel": "cheque_control.api.pe_on_cancel"
    }
}

fixtures = [{"dt": "Custom Field", "filters": [["name", "in", [
		"Company-cheques_default_accounts",
		"Company-receivable_notes_account",
		"Company-cheques_under_collection_account",
		"Company-cb_00",
		"Company-payable_notes_account"
	]]]}
]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cheque_control.tasks.all"
# 	],
# 	"daily": [
# 		"cheque_control.tasks.daily"
# 	],
# 	"hourly": [
# 		"cheque_control.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cheque_control.tasks.weekly"
# 	]
# 	"monthly": [
# 		"cheque_control.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "cheque_control.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cheque_control.event.get_events"
# }

