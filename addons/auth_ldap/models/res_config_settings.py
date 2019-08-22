# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ldaps = fields.One2many(related='company_id.ldaps', string="LDAP Parameters")
