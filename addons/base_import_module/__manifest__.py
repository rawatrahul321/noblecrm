# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.
{
    'name': 'Base import module',
    'description': """
Import a custom data module
===========================

This module allows authorized users to import a custom data module (.xml files and static assests)
for customization purpose.
""",
    'category': 'Extra Tools',
    'depends': ['web'],
    'installable': True,
    'auto_install': False,
    'data': ['views/base_import_module_view.xml'],
}
