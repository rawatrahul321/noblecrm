# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

import noblecrm.tests

@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestUi(noblecrm.tests.HttpCase):

    post_install = True
    at_install = False

    def test_01_admin_rte(self):
        self.phantom_js("/web", "noblecrm.__DEBUG__.services['web_tour.tour'].run('rte')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.rte.ready", login='admin')

    def test_02_admin_rte_inline(self):
        self.phantom_js("/web", "noblecrm.__DEBUG__.services['web_tour.tour'].run('rte_inline')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.rte_inline.ready", login='admin')
