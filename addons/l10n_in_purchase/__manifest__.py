# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Indian - Purchase Report(GST)',
    'version': '1.0',
    'description': """GST Purchase Report""",
    'category': 'Localization',
    'depends': [
        'l10n_in',
        'purchase',
    ],
    'data': [
        'views/report_purchase_order.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
