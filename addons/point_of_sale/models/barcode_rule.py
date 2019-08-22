# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import models, fields
from noblecrm.tools.translate import _


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
            ('weight', 'Weighted Product'),
            ('price', 'Priced Product'),
            ('discount', 'Discounted Product'),
            ('client', 'Client'),
            ('cashier', 'Cashier')
        ])
