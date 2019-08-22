# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hs_code = fields.Char(string="HS Code", help="Standardized code for international shipping and goods declaration")
