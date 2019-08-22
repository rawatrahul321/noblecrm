# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import fields, models


class Attachment(models.Model):

    _inherit = ['ir.attachment']

    product_downloadable = fields.Boolean("Downloadable from product portal", default=False)
