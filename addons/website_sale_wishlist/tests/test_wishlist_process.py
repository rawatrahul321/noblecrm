# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.
import noblecrm.tests


@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestUi(noblecrm.tests.HttpCase):
    def test_01_wishlist_tour(self):
        self.phantom_js("/", "noblecrm.__DEBUG__.services['web_tour.tour'].run('shop_wishlist')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.shop_wishlist.ready")
