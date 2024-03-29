# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm.addons.hr.tests.common import TestHrCommon


class TestHrFlow(TestHrCommon):

    def test_open2recruit2close_job(self):

        """ Opening the job position for "Developer" and checking the job status and recruitment count. """
        self.job_developer.set_open()
        self.assertEqual(self.job_developer.state, 'open', "Job position of 'Job Developer' is in 'open' state.")
        self.assertEqual(self.job_developer.no_of_recruitment, 0,
             "Wrong number of recruitment for the job 'Job Developer'(%s found instead of 0)."
             % self.job_developer.no_of_recruitment)

        """ Recruiting employee "NIV" for the job position "Developer" and checking the job status and recruitment count. """
        self.job_developer.set_recruit()
        self.assertEqual(self.job_developer.state, 'recruit', "Job position of 'Job Developer' is in 'recruit' state.")
        self.assertEqual(self.job_developer.no_of_recruitment, 1,
             "Wrong number of recruitment for the job 'Job Developer'(%s found instead of 1.0)."
             % self.job_developer.no_of_recruitment)

        self.employee_niv.write({'job_id': self.job_developer.id})

        """ Closing the recruitment for the job position "Developer" by marking it as open. """
        self.job_developer.set_open()
        self.assertEqual(self.job_developer.state, 'open', "Job position of 'Job Developer' is in 'open' state.")
        self.assertEqual(self.job_developer.no_of_recruitment, 0,
             "Wrong number of recruitment for the job 'Job Developer'(%s found instead of 0)."
             % self.job_developer.no_of_recruitment)
