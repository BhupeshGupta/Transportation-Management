# Copyright (c) 2013, Arun Logistics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TransportationRoute(Document):
    def autoname(self):
        self.name = '{} - {}'.format(self.route_name, self.vehicle_make)
