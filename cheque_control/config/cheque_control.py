from __future__ import unicode_literals
import frappe
from frappe import _

def get_data():
	return [
		{
			"label": _("Accounts Receivable"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Receivable Cheque",
					"description": _("Receivable Cheque."),
					"onboard": 1,
				},
				{
					"type": "report",
					"name": "Receivable Cheque Ledger",
					"doctype": "Receivable Cheque",
					"is_query_report": True,
				},
			]
		},
		{
			"label": _("Accounts Payable"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Payable Cheque",
					"description": _("Payable Cheque."),
					"onboard": 1,
				},
				{
					"type": "report",
					"name": "Payable Cheque Ledger",
					"doctype": "Payable Cheque",
					"is_query_report": True,
				},
			]
		},
	]

