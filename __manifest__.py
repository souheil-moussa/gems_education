{
    'name': 'Gems Education',
    'version': '1.0',
    'depends': ['mail','base','website'],
    'author': 'Souheil,Kevin,Charbel',
    'category': 'Inventory',
    'description': 'Manage Gems education system',
    'data': [
        'security/ir.model.access.csv',
        'security/gems_group.xml',
        'security/session_rule.xml',
        'views/gems_session_views.xml',
        'views/gems_school_views.xml',
        'views/res_users_views.xml',
        'views/gems_grade_views.xml',
        'views/gems_classroom_subject_views.xml',
        'views/gems_portal_templates_views.xml',
        'data/gems_sequence.xml'


    ],

    'sequence': '1',
    'installable': True,
    'application': True,
}
