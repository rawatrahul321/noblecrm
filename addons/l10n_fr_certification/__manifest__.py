# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'France - VAT Anti-Fraud Certification (CGI 286 I-3 bis)',
    'version': '1.0',
    'category': 'Localization',
    'description': """
This add-on brings the technical requirements of the French regulation CGI art. 286, I. 3° bis that stipulates certain criteria concerning the inalterability, security, storage and archiving of data related to sales to private individuals (B2C).
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The module adds following features:

    Inalterability: deactivation of all the ways to cancel or modify key data, invoices and journal entries

    Security: chaining algorithm to verify the inalterability

    Storage: automatic sales closings with computation of both period and cumulative totals (daily, monthly, annually)

    Access to download the mandatory Certificate of Conformity delivered by NobleCRM SA (only for NobleCRM Enterprise users)
""",
    'depends': ['l10n_fr'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'data': [
        'data/account_move.xml',
        'views/res_config.xml',
    ],
    'post_init_hook': '_setup_inalterability',
}
