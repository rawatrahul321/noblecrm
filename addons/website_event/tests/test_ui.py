import noblecrm.tests


@noblecrm.tests.common.at_install(False)
@noblecrm.tests.common.post_install(True)
class TestUi(noblecrm.tests.HttpCase):
    def test_admin(self):
        self.phantom_js("/", "noblecrm.__DEBUG__.services['web_tour.tour'].run('event')", "noblecrm.__DEBUG__.services['web_tour.tour'].tours.event.ready", login='admin')
