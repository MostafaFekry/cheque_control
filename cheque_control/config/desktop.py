# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Cheque Control",
			"category": "Modules",
			"label": _("Cheque Control"),
			"color": "#bdc3c7",
			"reverse": 1,
			"icon": "octicon octicon-repo",
			"type": "module",
			"description": "For controlling receivable and payable cheques."
		}
	]
