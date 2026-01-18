# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StandardCertification(models.Model):
    """Standard Certification Model

    This model represents comprehensive certification data for controls,
    including detailed procedures, impact analysis, and remediation steps
    extracted from benchmark documents like CIS Excel files.
    """
    _name = "mgmtsystem.standard.certification"
    _description = "Standard Certification"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "standard_id, sequence, name"
    _check_company_auto = True

    # Basic Information
    name = fields.Char(
        string="Certification Name",
        required=True,
        tracking=True,
        help="Name of the certification requirement"
    )

    title = fields.Char(
        string="Title",
        required=True,
        tracking=True,
        help="Full title of the certification requirement"
    )

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Sequence order for sorting"
    )

    # References and Relationships
    control_id = fields.Many2one(
        'mgmtsystem.standard.control',
        string="Related Control",
        help="Link to the standard control this certification relates to"
    )

    standard_id = fields.Many2one(
        'mgmtsystem.standard',
        string="Standard",
        required=True,
        tracking=True,
        help="The standard this certification belongs to"
    )

    domain_id = fields.Many2one(
        'mgmtsystem.standard.domain',
        string="Domain",
        help="Domain or section this certification belongs to"
    )

    # Core Certification Fields (from Excel analysis)
    description = fields.Html(
        string="Description",
        help="Detailed description of the certification requirement"
    )

    assessment_status = fields.Selection([
        ('automated', 'Automated'),
        ('manual', 'Manual'),
        ('hybrid', 'Hybrid'),
        ('not_applicable', 'Not Applicable')
    ], string="Assessment Status", 
       tracking=True,
       help="How this requirement can be assessed")

    rationale_statement = fields.Html(
        string="Rationale Statement",
        help="Why this requirement is important for security/compliance"
    )

    impact_statement = fields.Html(
        string="Impact Statement", 
        help="Business and technical impact of implementing this requirement"
    )

    remediation_procedure = fields.Html(
        string="Remediation Procedure",
        help="Step-by-step instructions for implementing this requirement"
    )

    audit_procedure = fields.Html(
        string="Audit Procedure",
        help="How to verify compliance with this requirement during audits"
    )

    additional_information = fields.Html(
        string="Additional Information",
        help="Extra context, notes, or considerations"
    )

    default_value = fields.Text(
        string="Default Value",
        help="Default system configuration value"
    )

    references = fields.Text(
        string="References",
        help="External references, links, and documentation"
    )

    # CIS Framework Integration
    cis_controls = fields.Text(
        string="CIS Controls",
        help="Related CIS Controls mapping"
    )

    cis_safeguards_v8_ig1 = fields.Text(
        string="CIS Safeguards v8 IG1",
        help="CIS Implementation Group 1 safeguards (v8)"
    )

    cis_safeguards_v8_ig2 = fields.Text(
        string="CIS Safeguards v8 IG2", 
        help="CIS Implementation Group 2 safeguards (v8)"
    )

    cis_safeguards_v8_ig3 = fields.Text(
        string="CIS Safeguards v8 IG3",
        help="CIS Implementation Group 3 safeguards (v8)"
    )

    cis_safeguards_v7_ig1 = fields.Text(
        string="CIS Safeguards v7 IG1",
        help="CIS Implementation Group 1 safeguards (v7)"
    )

    cis_safeguards_v7_ig2 = fields.Text(
        string="CIS Safeguards v7 IG2",
        help="CIS Implementation Group 2 safeguards (v7)"
    )

    cis_safeguards_v7_ig3 = fields.Text(
        string="CIS Safeguards v7 IG3", 
        help="CIS Implementation Group 3 safeguards (v7)"
    )

    # Profile and Level Information
    profile = fields.Char(
        string="Profile",
        help="Benchmark profile (e.g., Level 1 - Domain Controller)"
    )

    level = fields.Selection([
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('ng', 'Next Generation')
    ], string="Benchmark Level",
       help="CIS Benchmark level classification")

    # Status and Compliance
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('review', 'Under Review'),
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('not_applicable', 'Not Applicable'),
        ('remediated', 'Remediated')
    ], string="Status",
       default='draft',
       tracking=True,
       help="Current status of this certification requirement")

    compliance_percentage = fields.Float(
        string="Compliance %",
        help="Percentage of compliance achieved for this requirement"
    )

    # Metadata
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    # Remove complex many2many definition
    allowed_company_ids = fields.Many2many(
        'res.company',
        string='Allowed Companies',
        help="Companies that can access this standard"
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="Whether this certification requirement is active"
    )

    # Computed Fields
    recommendation_number = fields.Char(
        string="Recommendation #",
        help="Recommendation number from benchmark"
    )

    section_number = fields.Char(
        string="Section #", 
        help="Section number from benchmark"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set sequence if not provided"""
        for vals in vals_list:
            if 'sequence' not in vals:
                vals['sequence'] = self.env['ir.sequence'].next_by_code('mgmtsystem.standard.certification') or 10
        return super().create(vals_list)

    def name_get(self):
        """Custom name display"""
        result = []
        for record in self:
            name = record.name
            if record.recommendation_number:
                name = f"{record.recommendation_number} - {name}"
            result.append((record.id, name))
        return result