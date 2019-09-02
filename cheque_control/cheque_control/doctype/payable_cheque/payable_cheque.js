// Copyright (c) 2019, Systematic-eg and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payable Cheque', {
	setup: function(frm) {
		frm.set_query("contact_person", function() {
			if (frm.doc.party) {
				return {
					query: 'frappe.contacts.doctype.contact.contact.contact_query',
					filters: {
						link_doctype: frm.doc.party_type,
						link_name: frm.doc.party
					}
				};
			}
		});
	},
	refresh: function(frm) {
		
		if(frm.doc.docstatus==1) {		
			if(frm.doc.status == 'Cheque Issued' ) {
					frm.add_custom_button(__('Cheque Deducted'), () => frm.events.check_collect_account(frm,'Cheque Deducted'), __('Actions'));
					frm.add_custom_button(__('Cheque Cancelled'), () => frm.events.make_cheque_cancelled_action(frm,'Cheque Cancelled'), __('Actions'));
			}
			frm.page.set_inner_btn_group_as_primary(__('Actions'));
		
		}
		if(frm.doc.status == 'Cheque Issued' ) {
			if(! frm.doc.bank_account) {
				frm.set_df_property("bank_account", 'reqd', 1);
			}
		}
		else{
			frm.set_df_property("bank_account", 'reqd', 0);
		}
		
	},
	check_collect_account: function(frm,action_status) {
		
		if(action_status == 'Cheque Deducted' ) {
			if( frm.doc.collect_account && frm.doc.bank_account) {
				frm.events.make_cheque_action(frm,action_status);
			}
			else{
				frm.set_df_property("bank_account", 'reqd', 1);
				msgprint(__('Collect Bank Account required to Deducting'));
			}
		}
	},
	make_cheque_cancelled_action: function(frm,action_status) {
		
		if(action_status == 'Cheque Cancelled' ) {
			frappe.confirm(
				'Permanently Cancel '+frm.docname+'?',
				function(){
					frm.events.make_cheque_action(frm,action_status);
				},
				function(){
					// do nothing
				}
			)
		}
	},
	make_cheque_action: function(frm,action_status){
		if (action_status=="Cheque Cancelled") {
			frappe.call({
				method: 'cheque_control.cheque_control.doctype.payable_cheque.payable_cheque.make_action',
				args: {
					reference_doctype: frm.doctype,
					reference_name: frm.docname,
					action_status: action_status
				},
				// disable the button until the request is completed
				btn: $('.primary-action'),
				// freeze the screen until the request is completed
				freeze: true,
				callback: (r) => {
					frm.set_value("status", action_status);
					refresh_field("status_history");
					frm.reload_doc();
				}
			})
		}
		else{
			var d = new frappe.ui.Dialog({
				title: __('Transaction Posting Date'),
				fields: [
					{
						'fieldname': 'posting_date',
						'fieldtype': 'Date',
						'label': 'Posting Date',
						'reqd': 1
					}
				],
				primary_action: function() {
					var data = d.get_values();
					frappe.ui.form.is_saving = true;
					frappe.call({
						method: "cheque_control.cheque_control.doctype.payable_cheque.payable_cheque.make_action",
						args: {
							reference_doctype: frm.doctype,
							reference_name: frm.docname,
							posting_date: data.posting_date,
							action_status: action_status
						},
						callback: function(r) {
							if(!r.exc) {
								frm.set_value("status", action_status);
								refresh_field("status_history");
								d.hide();
								frm.reload_doc();
							}
						},
						always: function() {
							frappe.ui.form.is_saving = false;
						}
					});
				}
			});
			d.show();
		}
	},
	contact_person: function(frm) {
		frm.set_value("contact_email", "");
		erpnext.utils.get_contact_details(frm);
	}
});