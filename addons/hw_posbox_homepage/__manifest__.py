# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'PosBox Homepage',
    'category': 'Point of Sale',
    'sequence': 6,
    'website': 'https://www.infonoble.com/page/point-of-sale',
    'summary': 'A homepage for the PosBox',
    'description': """
PosBox Homepage
===============

This module overrides NobleCRM web interface to display a simple
Homepage that explains what's the posbox and show the status,
and where to find documentation.

If you activate this module, you won't be able to access the 
regular NobleCRM interface anymore.

""",
    'depends': ['hw_proxy'],
    'installable': False,
}
