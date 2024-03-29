# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.


{
    "name": "Vietnam - Accounting",
    "version": "2.0",
    "author": "General Solutions",
    'website': 'http://gscom.vn',
    'category': 'Localization',
    "description": """
This is the module to manage the accounting chart for Vietnam in NobleCRM.
=========================================================================

This module applies to companies based in Vietnamese Accounting Standard (VAS)
with Chart of account under Circular No. 200/2014/TT-BTC

**Credits:**
    - General Solutions.
    - Trobz
""",
    "depends": [
        "account",
        "base_iban"
    ],
    "data": [
         'data/l10n_vn_chart_data.xml',
         'data/account_data.xml',
         'data/account_tax_data.xml',
         'data/account_chart_template_data.yml',
    ],
    'post_init_hook': '_preserve_tag_on_taxes',
}
