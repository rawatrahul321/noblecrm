# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Calendar',
    'version': '1.0',
    'sequence': 130,
    'depends': ['base', 'mail'],
    'summary': 'Personal & Shared Calendar',
    'description': """
This is a full-featured calendar system.
========================================

It supports:
------------
    - Calendar of events
    - Recurring events

If you need to manage your meetings, you should install the CRM module.
    """,
    'category': 'Extra Tools',
    'website': 'https://www.infonoble.com/page/crm',
    'demo': [
        'data/calendar_demo.xml'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/calendar_security.xml',
        'data/calendar_cron.xml',
        'data/calendar_data.xml',
        'views/mail_activity_views.xml',
        'views/calendar_templates.xml',
        'views/calendar_views.xml',
        'data/mail_activity_data.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
