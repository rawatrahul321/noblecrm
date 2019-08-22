# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_template_id = fields.Many2one('sale.quote.template', default_model='sale.order', string='Default Template')
