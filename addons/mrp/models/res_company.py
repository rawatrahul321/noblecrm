# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    manufacturing_lead = fields.Float(
        'Manufacturing Lead Time', default=0.0, required=True,
        help="Security days for each manufacturing operation.")
