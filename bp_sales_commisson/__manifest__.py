{
    'name': 'Sales Commmission',
    'description': """ Sales Commmissio """,
    'author': "",
    'website': '',
    'version': '18.0.1.0.0',
    'support': '',
    'category': 'Sales',
    'depends': ['sale','base', 'hr', 'crm', 'sales_team'],
    'data': [
        'security/ir.model.access.csv',
        'views/achivements.xml',
        'views/team.xml',
        'views/user.xml',
    ],
    'assets': {

    },

    # 'images': [""],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
}

