# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sale_note = fields.Text(string='Default Terms and Conditions', translate=True)
