# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pad_server = fields.Char(related='company_id.pad_server', string="Pad Server *")
    pad_key = fields.Char(related='company_id.pad_key', string="Pad Api Key *")
