# -*- coding: utf-8 -*-

{
    'name': 'Management System Standards',
    'version': '18.0.1.0.1',
    'license': 'AGPL-3',
    'category': 'RB5820',
    'summary': 'Standards Management for Management Systems',
    'author': 'EQUANS',
    'website': 'https://www.equans.com',
    'depends': [
        'base',
        'mail',
        'mgmtsystem',
        'document_page',
        'product',
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        # Report
        'reports/report_standard_control.xml',
        'views/report_standard_control.xml',
        # Views
        'views/mgmtsystem_standard_views.xml',
        'views/mgmtsystem_standard_category_views.xml',
        'views/mgmtsystem_standard_domain_views.xml',
        'views/mgmtsystem_standard_requirement_views.xml',
        'views/mgmtsystem_standard_control_views.xml',
        'views/mgmtsystem_standard_certification_views.xml',
        'views/mgmtsystem_standard_assessment_tool_views.xml',
        # Data
        'data/mgmtsystem_standard_data.xml',
        'data/mgmtsystem_iec62443_2023_data.xml',



    ],
    'demo': [
        'data/mgmtsystem_standard_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
Management System Standards
==========================

This module allows you to manage standards, their categories, and requirements for your management system.

Key Features:
------------
* Manage standards with detailed information (e.g., ISO 9001, ISO 14001)
* Organize standards in hierarchical categories
* Track individual requirements within each standard
* Evaluate and monitor compliance with standard requirements
* Create audit questions for each requirement
* Link documents and evidence to standards and requirements
* Track standard versions and superseded standards

This module is particularly useful for organizations implementing or maintaining:
* Quality Management Systems
* Environmental Management Systems
* Health and Safety Management Systems
* Information Security Management Systems
* Energy Management Systems
* And other compliance requirements
    """
}
