# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Analytic Defaults',
    'version': '1.0',
    'category': 'Accounting',
    'description': """
Set default values for your analytic accounts.
==============================================

Allows to automatically select analytic accounts based on criterions:
---------------------------------------------------------------------
    * Product
    * Partner
    * User
    * Company
    * Date
    """,
    'website': 'https://www.infonoble.com/page/accounting',
    'depends': ['sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/account_analytic_default_security.xml',
        'views/account_analytic_default_view.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
}
