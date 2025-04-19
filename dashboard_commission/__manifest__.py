{
    'name': "Commission Dashboard",
    'version': '18.0.1.0.0',
    'category': 'Sale',
    'summary': """ """,
    'description': """ """,
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['hr', 'sale', 'web', 'bp_sales_commisson'],
    'data': [
        'views/views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'dashboard_commission/static/src/xml/dashboard.xml',
            'dashboard_commission/static/src/js/dashboard.js',
            'dashboard_commission/static/src/css/dashboard.css',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js'
        ],
    },
    'external_dependencies': {
        'python': ['pandas'],
    },
    'images': ['static/description/banner.png'],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}
