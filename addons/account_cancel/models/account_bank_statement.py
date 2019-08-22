# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm import models, api, _
from noblecrm.exceptions import UserError


class BankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.multi
    def button_draft(self):
        self.state = 'open'


