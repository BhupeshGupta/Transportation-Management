# Copyright (c) 2013, Arun Logistics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
from erpnext.accounts.general_ledger import make_gl_entries
import frappe
from erpnext.accounts.utils import get_fiscal_year


class RepairVoucher(Document):
	def validate(self):
		self.set_missing_values()

	def cancel(self):
		super(RepairVoucher, self).cancel()
		self.set_missing_values()
		self.make_gl_entries()

	def before_submit(self):
		self.make_gl_entries()

	def make_gl_entries(self):
		gl_entries = []
		self.make_customer_gl_entry(gl_entries)

		if gl_entries:
			make_gl_entries(
				gl_entries, cancel=(self.docstatus == 2),
				update_outstanding='Yes', merge_entries=False
			)

	def make_customer_gl_entry(self, gl_entries):
		# Entry in logistics partner account to get money form customer
		gl_entries.append(
			self.get_gl_dict({
			"account": self.debit_account,
			"against": self.credit_account,
			"debit": self.amount,
			"remarks": "Vehicle Repair {}".format(self.vehicle),
			"company": self.company
			})
		)

		gl_entries.append(
			self.get_gl_dict({
			"account": self.credit_account,
			"against": self.debit_account,
			"credit": self.amount,
			"remarks": "Vehicle Repair {}".format(self.vehicle),
			"company": self.company
			})
		)

	def get_gl_dict(self, args):
		"""this method populates the common properties of a gl entry record"""
		gl_dict = frappe._dict({
		'company': self.company,
		'posting_date': self.date,
		'voucher_type': self.doctype,
		'voucher_no': self.name,
		'aging_date': self.get("aging_date") or self.date,
		'remarks': self.get("notes"),
		'fiscal_year': self.fiscal_year,
		'cost_center': self.cost_center,
		'debit': 0,
		'credit': 0,
		'is_opening': "No"
		})
		gl_dict.update(args)
		return gl_dict

	def set_missing_values(self):
		self.fiscal_year = get_fiscal_year(self.date)[0]