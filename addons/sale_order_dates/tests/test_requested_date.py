# -*- coding: utf-8 -*-

from datetime import timedelta
from noblecrm.tests import common
from noblecrm import fields


class TestSaleOrderDates(common.TransactionCase):

    def test_sale_order_requested_date(self):

        # In order to test the Requested Date feature in Sales Orders in NobleCRM,
        # I copy a demo Sales Order with Requested Date on 2010-07-12
        new_order = self.env.ref('sale.sale_order_6').copy({'requested_date': '2010-07-12'})
        # I confirm the Sales Order.
        new_order.action_confirm()
        # I verify that the Procurements and Stock Moves have been generated with the correct date
        security_delay = timedelta(days=new_order.company_id.security_lead)
        requested_date = fields.Datetime.from_string(new_order.requested_date)
        right_date = fields.Datetime.to_string(requested_date - security_delay)
        for line in new_order.order_line:
            self.assertEqual(line.move_ids[0].date_expected, right_date, "The expected date for the Stock Move is wrong")
