# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _action_launch_procurement_rule(self):
        res = super(SaleOrderLine, self)._action_launch_procurement_rule()
        orders = list(set(x.order_id for x in self))
        for order in orders:
            reassign = order.picking_ids.filtered(lambda x: x.state=='confirmed' or (x.state in ['waiting', 'assigned'] and not x.printed))
            if reassign:
                reassign.do_unreserve()
                reassign.action_assign()
        return res
