# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Indian - Stock Report(GST)',
    'version': '1.0',
    'description': """GST Stock Report""",
    'category': 'Localization',
    'depends': [
        'l10n_in',
        'stock',
    ],
    'data': [
        'views/report_stockpicking_operations.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
