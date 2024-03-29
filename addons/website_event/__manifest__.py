# -*- coding: utf-8 -*-

{
    'name': 'Online Events',
    'category': 'Marketing',
    'sequence': 166,
    'summary': 'Publish Events and Manage Online Registrations on your Website',
    'website': 'https://www.infonoble.com/page/website-builder',
    'description': "",
    'depends': ['website', 'website_partner', 'website_mail', 'event'],
    'data': [
        'data/event_data.xml',
        'views/res_config_settings_views.xml',
        'views/event_templates.xml',
        'views/event_views.xml',
        'security/ir.model.access.csv',
        'security/event_security.xml',
    ],
    'demo': [
        'data/event_demo.xml'
    ],
    'application': True,
}
