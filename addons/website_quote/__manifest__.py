# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.
{
    'name': 'Online Proposals',
    'category': 'Website',
    'summary': 'Sales',
    'website': 'https://www.infonoble.com/page/quote-builder',
    'version': '1.0',
    'description': "",
    'depends': ['website', 'sale_management', 'mail', 'payment', 'website_mail'],
    'data': [
        'data/website_quote_data.xml',
        'report/sale_order_reports.xml',
        'report/sale_order_templates.xml',
        'report/website_quote_templates.xml',
        'views/sale_order_views.xml',
        'views/sale_quote_views.xml',
        'views/website_quote_templates.xml',
        'views/res_config_settings_views.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/website_quote_demo.xml'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,

    # needed because dependencies can't be changed in a stable version
    # TODO in master: add sale_payment to depends and remove this
    'post_init_hook': '_install_sale_payment',
}
