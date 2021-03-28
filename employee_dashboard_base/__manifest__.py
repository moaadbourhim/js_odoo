# -*- coding: utf-8 -*-
{
    'name': "test de Java script",

    'summary': """
        This Module is for Eric Clean""",

    'description': """
        This Module module add new features to the standard 
        module project management in Odoo 
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'project', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'view/web_assest_emp.xml',
        'view/menu_dashboard_test.xml'

    ],
    'qweb': [
            'static/src/xml/dashboard.xml'
    ]
}