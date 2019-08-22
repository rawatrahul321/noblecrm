# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    last_website_so_id = fields.Many2one('sale.order', string='Last Online Sales Order', copy=False)
