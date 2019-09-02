# -*- coding: utf-8 -*-
# Copyright (c) 2019, Systematic-eg and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, cstr, nowdate, comma_and
from frappe import msgprint, _
from frappe.model.document import Document

class PayableCheque(Document):
	def on_cancel(self):
		frappe.throw(_("Not permitted, Cannot Cancel this document"))
		
	def on_update(self):
		notes_acc = frappe.db.get_value("Company", self.company, "payable_notes_account")
		if not notes_acc:
			frappe.throw(_("Payable Notes Account not defined in the company setup page"))
		elif len(notes_acc) < 4:
				frappe.throw(_("Payable Notes Account not defined in the company setup page"))

		rec_acc = frappe.db.get_value("Company", self.company, "default_payable_account")
		if not rec_acc:
			frappe.throw(_("Default Payable Account not defined in the company setup page"))
		elif len(rec_acc) < 4:
			frappe.throw(_("Default Payable Account not defined in the company setup page"))
			
	def check_modified_date(self):
		mod_db = frappe.db.get_value("Receivable Cheque", self.name, "modified")
		date_diff = frappe.db.sql("select TIMEDIFF('%s', '%s')" %
			( mod_db, cstr(self.modified)))
		if date_diff and date_diff[0][0]:
			frappe.throw(_("{0} {1} has been modified. Please refresh.").format(self.doctype, self.name))
	
	def update_status(self, status=None):
		self.check_modified_date()

		if status != self.status:
			self.db_set("status", status,)

		#self.update_required_items()

		return status
	
	def check_to_make_action(self,posting_date=None, action_status=None):
		notes_acc = frappe.db.get_value("Company", self.company, "payable_notes_account")
		if not notes_acc:
			frappe.throw(_("Payable Notes Account not defined in the company setup page"))
		elif len(notes_acc) < 4:
				frappe.throw(_("Payable Notes Account not defined in the company setup page"))

		rec_acc = frappe.db.get_value("Company", self.company, "default_payable_account")
		if not rec_acc:
			frappe.throw(_("Default Payable Account not defined in the company setup page"))
		elif len(rec_acc) < 4:
			frappe.throw(_("Default Payable Account not defined in the company setup page"))
			
		if action_status == "Cheque Deducted":
			if not self.bank_account and not self.collect_account:
				frappe.throw(_("Deposit bank account not defined to proceed collecting cheque"))
			self.make_journal_entry(notes_acc, self.collect_account, self.amount, action_status, posting_date, party_type=None, party=None, cost_center=None, 
					save=True, submit=True)
		if action_status == "Cheque Cancelled":
			self.cancel_payment_entry(action_status)


	def cancel_payment_entry(self,action_status):
		self.update_status(action_status)
		if self.payment_entry: 
			frappe.get_doc("Payment Entry", self.payment_entry).cancel()
				
		self.append("status_history", {
				"status": action_status,
				"transaction_date": nowdate(),
				"bank": self.bank
			})
		self.submit()
		message = """<a href="#Form/Payment Entry/%s" target="_blank">%s</a>""" % (self.payment_entry, self.payment_entry)
		msgprint(_("Payment Entry {0} Cancelled").format(comma_and(message)))
		
		return message
			
	def make_journal_entry(self, account1, account2, amount, action_status, posting_date=None, party_type=None, party=None, cost_center=None, 
							save=True, submit=False):
		cost_center_project = cost_center
		if self.project:
			cost_center_project = frappe.db.get_value("Project", self.project, "cost_center")
		jv = frappe.new_doc("Journal Entry")
		jv.posting_date = posting_date or nowdate()
		jv.company = self.company
		jv.cheque_no = self.cheque_no
		jv.cheque_date = self.cheque_date
		jv.user_remark = self.remarks or "Cheque Transaction"
		jv.multi_currency = 0
		jv.set("accounts", [
			{
				"account": account1,
				"party_type": party_type if (action_status == "Cheque Cancelled") else None,
				"party": party if action_status == "Cheque Cancelled" else None,
				"cost_center": cost_center_project,
				"project": self.project,
				"debit_in_account_currency": amount if amount > 0 else 0,
				"credit_in_account_currency": abs(amount) if amount < 0 else 0
			}, {
				"account": account2,
				"party_type": party_type if action_status == "Cheque Issued" else None,
				"party": party if action_status == "Cheque Issued" else None,
				"cost_center": cost_center_project,
				"project": self.project,
				"credit_in_account_currency": amount if amount > 0 else 0,
				"debit_in_account_currency": abs(amount) if amount < 0 else 0
			}
		])
		if save or submit:
			jv.insert(ignore_permissions=True)

			if submit:
				jv.submit()

		self.append("status_history", {
				"status": action_status,
				"transaction_date": nowdate(),
				"transaction_posting_date": posting_date or nowdate(),
				"debit_account": account1,
				"credit_account": account2,
				"journal_entry": jv.name
			})
		
		self.update_status(action_status)
		self.submit()
		message = """<a href="#Form/Journal Entry/%s" target="_blank">%s</a>""" % (jv.name, jv.name)
		msgprint(_("Journal Entry {0} created").format(comma_and(message)))
		#message = _("Journal Entry {0} created").format(comma_and(message))
		
		return message

@frappe.whitelist()
def make_action(reference_doctype, reference_name, action_status,posting_date=None):
	if not frappe.has_permission(reference_doctype, "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)
	pc = frappe.get_doc(reference_doctype, reference_name)
	return pc.check_to_make_action(posting_date, action_status)