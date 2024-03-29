# -*- coding: utf-8 -*-

import os

from noblecrm import tools
from noblecrm.tests import common
from noblecrm.modules.module import get_module_resource


class RepoortIntrastatTest(common.TransactionCase):

    def _load(self, module, *args):
        tools.convert_file(self.cr, 'report_intrastat',
                           get_module_resource(module, *args),
                           {}, 'init', False, 'test', self.registry._assertion_report)

    def setUp(self):
        super(RepoortIntrastatTest, self).setUp()

        self._load('account', 'test', 'account_minimal_test.xml')
        self.invoice = self.env['account.invoice'].create({
            'currency_id': self.ref('base.EUR'),
            'company_id': self.ref('base.main_company'),
            'partner_id': self.ref('base.res_partner_1'),
            'state': 'draft',
            'type': 'out_invoice',
            'account_id': self.ref('report_intrastat.a_recv'),
            'name': 'Test invoice 1'
        })

    def test_00_create_pdf(self):
        data, data_format = self.env.ref('report_intrastat.account_intrastatinvoices').render(self.invoice.ids)
        if tools.config['test_report_directory']:
            open(os.path.join(tools.config['test_report_directory'], 'report_intrastat-intrastat_report.' + data_format), 'wb+').write(data)
