# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class ServiceTaxRate(models.Model):
    _name = "l10n_eu_service.service_tax_rate"

    country_id = fields.Many2one('res.country', string='Country')
    rate = fields.Float(string="VAT Rate")
