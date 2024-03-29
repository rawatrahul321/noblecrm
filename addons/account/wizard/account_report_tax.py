# -*- coding: utf-8 -*-

from noblecrm import models


class AccountTaxReport(models.TransientModel):
    _inherit = "account.common.report"
    _name = 'account.tax.report'
    _description = 'Tax Report'

    def _print_report(self, data):
        return self.env.ref('account.action_report_account_tax').report_action(self, data=data)
