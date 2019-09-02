# -*- coding: utf-8 -*-
# Copyright (c) 2019, Systematic-eg and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'cheque_no',
		'non_standard_fieldnames': {
			'Journal Entry': 'reference_name',
		},
		'internal_links': {
			'Journal Entry': ['status_history','journal_entry']
		},
		'transactions': [
			{
				'label': _('Reference'),
				'items': ['Journal Entry']
			},
		]
	}