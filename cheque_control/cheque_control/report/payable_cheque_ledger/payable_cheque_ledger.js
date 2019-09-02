// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Payable Cheque Ledger"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company"),
			on_change: function() {
				var company = frappe.query_report.get_filter_value('company');

				if(company === "") {
					frappe.query_report.set_filter_value('payable_cheque', "");
					frappe.query_report.set_filter_value('cheque_no', "");
					frappe.query_report.set_filter_value('party_type', "");
					frappe.query_report.set_filter_value('party', "");
					frappe.query_report.set_filter_value('party_name', "");
					return;
				}
			}
		},
		{
			"fieldname":"payable_cheque",
			"label": __("Payable Cheque"),
			"fieldtype": "Link",
			"options": "Payable Cheque",
			"get_query": function() {
				var company = frappe.query_report.get_filter_value('company');
				return {
					"doctype": "Payable Cheque",
					"filters": {
						"company": company,
					}
				}
			},
			on_change: function() {
				var payable_cheque = frappe.query_report.get_filter_value('payable_cheque');

				if(payable_cheque === "") {
					frappe.query_report.set_filter_value('cheque_no', "");
					frappe.query_report.set_filter_value('party_type', "");
					frappe.query_report.set_filter_value('party', "");
					frappe.query_report.set_filter_value('party_name', "");
					return;
				} else {
					var party_type =  "Payable Cheque";
					var fieldname =  "cheque_no";
					frappe.db.get_value(party_type, payable_cheque, fieldname, function(value) {
						frappe.query_report.set_filter_value('cheque_no', value[fieldname]);
					});
					frappe.db.get_value(party_type, payable_cheque, "party_type", function(value) {
						frappe.query_report.set_filter_value('party_type', value["party_type"]);
					});
					frappe.db.get_value(party_type, payable_cheque, "party", function(value) {
						frappe.query_report.set_filter_value('party', value["party"]);
					});
					frappe.db.get_value(party_type, payable_cheque, "party_name", function(value) {
						frappe.query_report.set_filter_value('party_name', value["party_name"]);
					});
				}
			}
		},
		{
			"fieldname":"cheque_no",
			"label": __("Cheque No."),
			"fieldtype": "Read Only",
			"default": "",
			"reqd": 1,
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Read Only",
		},
		{
			"fieldname":"party",
			"label": __("Party"),
			"fieldtype": "Read Only",
		},
		{
			"fieldname":"party_name",
			"label": __("Party Name"),
			"fieldtype": "Read Only",
		},
	]
}
