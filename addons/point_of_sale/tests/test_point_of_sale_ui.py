# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

import noblecrm.tests


@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestUi(noblecrm.tests.HttpCase):

    def test_01_point_of_sale_tour(self):
        self.phantom_js("/web", "noblecrm.__DEBUG__.services['web_tour.tour'].run('point_of_sale_tour')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.point_of_sale_tour.ready", login="admin")
