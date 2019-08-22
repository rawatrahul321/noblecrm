# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = ['account.invoice', 'utm.mixin']
