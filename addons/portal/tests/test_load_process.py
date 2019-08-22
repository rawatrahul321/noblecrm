# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.
import noblecrm.tests


@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestUi(noblecrm.tests.HttpCase):
    def test_01_portal_load_tour(self):
        self.phantom_js(
            "/",
            "noblecrm.__DEBUG__.services['web_tour.tour'].run('portal_load_homepage')",
            "noblecrm.__DEBUG__.services['web_tour.tour'].tours.portal_load_homepage.ready",
            login="portal"
        )
