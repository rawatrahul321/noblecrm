# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from . import models


def post_init(cr, registry):
    """ Set the timesheet project and task on existing leave type. Do it in post_init to
        be sure the internal project/task of res.company are set. (Since timesheet_generate field
        is true by default, those 2 fields are required on the leave type).
    """
    from noblecrm import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    for leave_type in env['hr.holidays.status'].search([('timesheet_generate', '=', True), ('timesheet_project_id', '=', False)]):
        company = leave_type.company_id or env.user.company_id
        leave_type.write({
            'timesheet_project_id': company.leave_timesheet_project_id.id,
            'timesheet_task_id': company.leave_timesheet_task_id.id,
        })
