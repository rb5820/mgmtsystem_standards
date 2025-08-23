# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MgmtSystemStandardAuditQuestion(models.Model):
    """Management System Standard Audit Question
    
    This model represents audit questions that can be used to verify
    compliance with standard requirements during audits.
    """
    _name = "mgmtsystem.standard.audit.question"
    _description = "Standard Audit Question"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "sequence"
    _check_company_auto = True
    
    name = fields.Char(
        string="Question",
        required=True,
        tracking=True,
        help="Audit question text"
    )

    sequence = fields.Integer(
        default=10,
        help="Sequence for ordering questions"
    )
    
    description = fields.Text(
        string="Description",
        help="Additional context or guidance for the auditor"
    )
    
    requirement_id = fields.Many2one(
        'mgmtsystem.standard.requirement',
        string='Requirement',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="The requirement this question helps audit"
    )
    
    standard_id = fields.Many2one(
        'mgmtsystem.standard',
        related='requirement_id.standard_id',
        string='Standard',
        store=True,
        readonly=True,
        help="The standard this question relates to"
    )
    
    expected_evidence = fields.Text(
        string="Expected Evidence",
        help="Description of what evidence would satisfy this requirement"
    )
    
    objective_evidence = fields.Text(
        string="Objective Evidence",
        help="Records of the evidence found during an audit"
    )
    
    active = fields.Boolean(
        default=True,
        help="If unchecked, it will allow you to hide this question without removing it."
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='requirement_id.company_id',
        store=True,
        readonly=True
    )
