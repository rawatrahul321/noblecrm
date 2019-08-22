# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm.api import Environment
import noblecrm.tests


@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestWebsiteCrm(noblecrm.tests.HttpCase):

    def test_tour(self):
        self.phantom_js("/", "noblecrm.__DEBUG__.services['web_tour.tour'].run('website_crm_tour')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.website_crm_tour.ready")

        # need environment using the test cursor as it's not committed
        cr = self.registry.cursor()
        assert cr is self.registry.test_cr
        env = Environment(cr, self.uid, {})
        record = env['crm.lead'].search([('description', '=', '### TOUR DATA ###')])
        assert len(record) == 1
        assert record.contact_name == 'John Smith'
        assert record.email_from == 'john@smith.com'
        assert record.partner_name == 'NobleCRM S.A.'
