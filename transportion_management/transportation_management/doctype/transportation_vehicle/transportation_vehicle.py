# Copyright (c) 2013, Arun Logistics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
import frappe

from flows.stdlogger import root
import utils as transportation_utils


class TransportationVehicle(Document):
    def __init__(self, *args, **kwargs):
        super(TransportationVehicle, self).__init__(*args, **kwargs)
        self.create_account_under = None


    def save(self, *args, **kwargs):
        warehouse_account = self.get_warehouse_account()
        if not warehouse_account:
            warehouse_account = {}

        warehouse_account.update(self.map_warehouse_account())
        warehouse_account.update({"doctype": "Warehouse"})

        warehouse_account = frappe.get_doc(warehouse_account)

        warehouse_account.save()

        return super(TransportationVehicle, self).save(*args, **kwargs)

    def map_warehouse_account(self):
        return {
            "company": self.stock_owner,
            "warehouse_name": self.vehicle_number
        }

    def get_warehouse_account(self, ):
        warehouse = frappe.db.get_value(
            "Warehouse", transportation_utils.transport_vehicle_to_warehouse_name(self.name,
                                                                                  self.stock_owner),
            "*", as_dict=True
        )
        root.debug(warehouse)
        return warehouse