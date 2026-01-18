from odoo import models, fields

class StandardAssessmentTool(models.Model):
    _name = 'mgmtsystem.standard.control.assessment.tool'
    _description = 'Standard Assessment Tool'
    _check_company_auto = True
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tool Name', required=True, help='Name of the assessment tool or integration.')
    title = fields.Char(
        string='Title',
        tracking=True,
        help='Title of the assessment tool'
    )
    description = fields.Text(string='Description', help='Description of the assessment tool.')
    tool_type = fields.Selection([
        ('manual', 'Manual'),
        ('automated', 'Automated'),
        ('integration', 'Integration'),
    ], string='Tool Type', default='manual', help='Type of assessment tool.')

    tool_url = fields.Char(string='Tool URL', help='URL for the assessment tool or integration.')
    tool_instructions = fields.Text(string='Tool Instructions', help='Instructions for using the assessment tool.')

    vendor = fields.Char(string='Vendor', help='Vendor or provider of the assessment tool.')
    version = fields.Char(string='Version', help='Version of the assessment tool.')
    documentation_url = fields.Char(string='Documentation Link', help='Link to the tool documentation or user guide.')

    # Relationships
    # This field links the assessment tool to a specific control in the management system standards.
    # It is not required to ensure flexibility in tool usage.
    # If a tool is not linked to a specific control, it can still be used independently.
    # If a tool is linked to a control, it can be used for assessments related to that control.
    # This allows for both standalone tools and those integrated into specific controls.
    # If the tool is linked to a control, it will be used for assessments related to that control.
    # If not linked, it can be used independently.
    # This field is optional to allow for tools that may not be directly linked to a control.
    # If a tool is not linked to a control, it can still be used independently.
    # If a tool is linked to a control, it can be used for assessments related to that control.
    # linked_standard_ids = fields.Many2many(
    #     'mgmtsystem.standard.control',
    #     'assessment_tool_standard_control_rel',  # short relation table name
    #     'assessment_tools_id',                    # column for this model
    #     'standard_control_id',                   # column for the related model
    #     string='Linked Standards',
    #     help='Standards this assessment tool is linked to.'
    # )

    # List of all controls that link to this assessment tool via the Many2many field
    linked_control_ids = fields.One2many(
        'mgmtsystem.standard.control',
        'assessment_tools',
        string='Linked Controls'
    )

    # List of all standards 



    control_id = fields.Many2one(
        'mgmtsystem.standard.control',
        string='Standard Control',
        ondelete='cascade',
        help='The control this assessment tool is linked to.'
    )
    active = fields.Boolean(string='Active', default=True, help='Set to True to keep the tool active, False to archive it.')
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this standard belongs to'
    )

    # Remove complex many2many definition
    allowed_company_ids = fields.Many2many(
        'res.company',
        string='Allowed Companies',
        help="Companies that can access this standard"
    )
