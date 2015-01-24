import frappe


def transport_vehicle_to_warehouse_name(vehicle_name, stock_owner_company):
    stock_owner_company = frappe.db.get_value(
        "Company", stock_owner_company, ["abbr"], as_dict=True
    )

    return '{} - {}'.format(vehicle_name, stock_owner_company.abbr.strip())


def warehouse_name_to_transport_vehicle(warehouse_name):
    return warehouse_name.split('-')[0]
