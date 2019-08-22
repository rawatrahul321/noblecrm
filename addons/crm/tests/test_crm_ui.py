# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

import noblecrm.tests


@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestUi(noblecrm.tests.HttpCase):

    def test_01_crm_tour(self):
        self.phantom_js("/web", "noblecrm.__DEBUG__.services['web_tour.tour'].run('crm_tour')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.crm_tour.ready", login="admin")
