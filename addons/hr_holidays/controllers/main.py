# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm.addons.mail.controllers.main import MailController
from noblecrm import http


class HrHolidaysController(http.Controller):

    @http.route('/hr_holidays/validate', type='http', auth='user', methods=['GET'])
    def hr_holidays_validate(self, res_id, token):
        comparison, record, redirect = MailController._check_token_and_record_or_redirect('hr.holidays', int(res_id), token)
        if comparison and record:
            try:
                record.action_approve()
            except Exception:
                return MailController._redirect_to_messaging()
        return redirect

    @http.route('/hr_holidays/refuse', type='http', auth='user', methods=['GET'])
    def hr_holidays_refuse(self, res_id, token):
        comparison, record, redirect = MailController._check_token_and_record_or_redirect('hr.holidays', int(res_id), token)
        if comparison and record:
            try:
                record.action_refuse()
            except Exception:
                return MailController._redirect_to_messaging()
        return redirect
