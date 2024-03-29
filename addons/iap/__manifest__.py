# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.


{
    'name': 'In-App Purchases',
    'category': 'Tools',
    'summary': 'Basic models and helpers to support In-App purchases.',
    'description': """
This module provides standard tools (account model, context manager and helpers) to support In-App purchases inside NobleCRM.
""",
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/assets.xml',
        'views/iap_views.xml',
    ],
    'qweb': [
        'static/src/xml/iap_templates.xml',
    ],
    'auto_install': True,
    # needed because dependencies can't be changed in a stable version
    # TODO in master: add web_settings_dashboard to depends and remove this
    'post_init_hook': '_install_web_settings_dashboard',
}
