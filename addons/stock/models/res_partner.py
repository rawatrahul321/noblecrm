# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models
from noblecrm.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP


class Partner(models.Model):
    _inherit = 'res.partner'

    property_stock_customer = fields.Many2one(
        'stock.location', string="Customer Location", company_dependent=True,
        help="This stock location will be used, instead of the default one, as the destination location for goods you send to this partner")
    property_stock_supplier = fields.Many2one(
        'stock.location', string="Vendor Location", company_dependent=True,
        help="This stock location will be used, instead of the default one, as the source location for goods you receive from the current partner")
    picking_warn = fields.Selection(WARNING_MESSAGE, 'Stock Picking', help=WARNING_HELP, default='no-message', required=True)
    # TDE FIXME: expand this message / help
    picking_warn_msg = fields.Text('Message for Stock Picking')
