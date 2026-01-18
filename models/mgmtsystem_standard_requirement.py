# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MgmtSystemStandardRequirement(models.Model):
    """Management System Standard Requirement
    
    This model represents individual requirements defined within standards,
    allowing for detailed tracking of compliance with specific clauses.
    """
    _name = "mgmtsystem.standard.requirement"
    _description = "Management System Standard Requirement"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "sequence, standard_id, code, name"
    _parent_name = "parent_id"
    _parent_store = True
    _check_company_auto = True
    
    name = fields.Char(
        string="Requirement Name",
        required=True,
        tracking=True,
        help="Name or title of the requirement"
    )
    
    title = fields.Char(
        string="Title",
        tracking=True,
        help="Title of the requirement"
    )

    code = fields.Char(
        string="Code/Clause",
        tracking=True,
        help="Code or clause number (e.g., 4.1, 6.2.1)"
    )
    
    description = fields.Text(
        string="Description",
        help="Full description of the requirement"
    )

    sequence = fields.Integer(
        default=10,
        help="Sequence for ordering requirements"
    )

    standard_id = fields.Many2one(
        'mgmtsystem.standard',
        string='Standard',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Standard to which this requirement belongs"
    )
    
    parent_id = fields.Many2one(
        'mgmtsystem.standard.requirement',
        string='Parent Requirement',
        index=True,
        ondelete='cascade',
        tracking=True,
        help="Parent requirement (for hierarchical structuring of clauses)"
    )
    
    child_ids = fields.One2many(
        'mgmtsystem.standard.requirement',
        'parent_id',
        string='Child Requirements',
        help="Sub-requirements or sub-clauses"
    )
    
    parent_path = fields.Char(
        string="Parent Path",
        index=True,
    )
    
    implementation_evidence = fields.Text(
        string="Implementation Evidence",
        help="Description of evidence needed to demonstrate compliance"
    )
    
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('partial', 'Partially Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('not_applicable', 'Not Applicable'),
        ('not_evaluated', 'Not Evaluated')
    ], string='Compliance Status', default='not_evaluated', tracking=True)
    
    compliance_notes = fields.Text(
        string="Compliance Notes",
        help="Notes regarding compliance status"
    )
    
    document_ids = fields.Many2many(
        'ir.attachment',
        string='Documents',
        help="Related documents and evidence"
    )
    
    audit_question_ids = fields.One2many(
        'mgmtsystem.standard.audit.question',
        'requirement_id',
        string='Audit Questions',
        help="Questions to ask during audits to verify compliance"
    )
    
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        help="Person responsible for ensuring compliance with this requirement"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='standard_id.company_id',
        store=True,
        readonly=True
    )

    # Remove complex many2many definition
    allowed_company_ids = fields.Many2many(
        'res.company',
        string='Allowed Companies',
        help="Companies that can access this standard"
    )
    
    active = fields.Boolean(
        default=True,
        help="If unchecked, it will allow you to hide this requirement without removing it."
    )
    
    color = fields.Integer(string='Color Index')
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical')
    ], default='1', string="Priority", help="Priority of this requirement")
    
    complete_code = fields.Char(
        string='Complete Code',
        recursive=True,
        compute='_compute_complete_code',
        store=True,
    )

    @api.depends('code', 'parent_id.complete_code')
    def _compute_complete_code(self):
        for requirement in self:
            if requirement.parent_id and requirement.parent_id.complete_code and requirement.code:
                requirement.complete_code = '%s.%s' % (requirement.parent_id.complete_code, requirement.code)
            else:
                requirement.complete_code = requirement.code

    @api.model_create_multi
    def create(self, vals_list):
        """Ensure company_id is always included in allowed_company_ids"""
        records = super().create(vals_list)
        for record in records:
            if record.company_id and record.company_id not in record.allowed_company_ids:
                record.allowed_company_ids = [(4, record.company_id.id)]
        return records
    
    def write(self, vals):
        """Ensure company_id is always included in allowed_company_ids when updated"""
        result = super().write(vals)
        # Check if either company_id or allowed_company_ids was modified
        if 'company_id' in vals or 'allowed_company_ids' in vals:
            for record in self:
                if record.company_id and record.company_id not in record.allowed_company_ids:
                    record.allowed_company_ids = [(4, record.company_id.id)]
        return result
