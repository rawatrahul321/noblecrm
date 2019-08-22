# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

import noblecrm.tests


@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestUi(noblecrm.tests.HttpCase):
    def test_admin(self):
        self.phantom_js("/", "noblecrm.__DEBUG__.services['web_tour.tour'].run('blog')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.blog.ready", login='admin')
