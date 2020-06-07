# -*- coding: utf-8 -*-
{
    'name': 'openacademy',

    'summary': 'openacademy Short description',

    'description': 'openacademy Long description',

    'author': 'kevinLeBlond',
    'website': 'http://www.lbrouard.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'lbrouard',
    'version': '10.25',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/openacademy.xml',
        'views/partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]
}
