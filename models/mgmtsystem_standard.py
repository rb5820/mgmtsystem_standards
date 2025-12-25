# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MgmtSystemStandard(models.Model):

    """Management System Standard
    
    This model represents management system standards such as ISO standards,
    IEC standards, and other regulatory frameworks for organizational compliance.
    """
    _name = "mgmtsystem.standard"
    _description = "Management System Standard"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True
    _parent_name = 'parent_id'                  # by default its name is parent_id you can change it
    _parent_store = True                        # tell odoo that this model support parent & child relation ship
    _order = "parent_left, issuing_body, name"                      # Default ordering by parent_left for hierarchical display

    name = fields.Char(
        string="Standard Name",
        required=True,
        tracking=True,
        help="Name of the management system standard (e.g., ISO 9001, ISO 14001)"
    )

    # Standard Code and Version
    # This is a unique identifier for the standard, often used in references
    title = fields.Char(
        string="Standard Title",
        required=True,
        tracking=True,
        help="Title of the management system standard (e.g., Quality Management System)"
    )

    #model should be extended from rds.base
    # This field links the standard to a specific RDS base, allowing for better integration with RDS models
    # This model entry should be made in the rds module itself
    # rds_base_id = fields.Char(
    #     string="RDS Base ID",
    #     help="Reference to the RDS base record identifier - will be converted to a relation field when RDS module is installed"
    # )
    
    # RDS integration note - keep this comment for future reference
    # When RDS module is installed, this field should be changed back to:
    # rds_base_id = fields.Many2one(
    #     'rds.base',
    #     string="RDS Base",
    #     help="Reference to the RDS base record"
    # )


    code = fields.Char(
        string="Standard Code",
        compute="_compute_code",
        store=True,
        tracking=True,
        help="Code or reference number of the standard (e.g., ISO 9001:2015)"
    )
    
    version = fields.Char(
        string="Version",
        tracking=True,
        help="Version or edition of the standard (e.g., 2015, 2018)"
    )
     
    description = fields.Text(
        string="Description",
        help="Description of the standard and its purpose"
    )

    scope = fields.Text(
        string="Scope",
        help="Scope of application for this standard"
    )

    publication_date = fields.Date(
        string="Publication Date",
        help="Date when the standard was published"
    )
    
    effective_date = fields.Date(
        string="Effective Date",
        help="Date when the standard became effective"
    )
    
    expiry_date = fields.Date(
        string="Expiry Date", 
        help="Date when the standard will expire or be superseded"
    )
    
    standard_type = fields.Selection([
        ('quality', 'Quality Management'),
        ('environmental', 'Environmental Management'),
        ('safety', 'Health & Safety'),
        ('security', 'Information Security'),
        ('energy', 'Energy Management'),
        ('risk', 'Risk Management'),
        ('compliance', 'Regulatory Compliance'),
        ('technical', 'Technical Standard'),
        ('industry', 'Industry Specific'),
        ('project', 'Project Specific'),
        ('other', 'Other')
    ], string='Standard Type', required=True, default='other')

    documentation_url = fields.Char(
        string="Documentation URL",
        help="URL for external documentation of the standard"  
    )

    internal_documentation_url = fields.Char(
        string="Internal Documentation URL",
    )

    documentation_filename = fields.Char(
        string="Documentation Filename",
        help="Filename for the internal documentation file"
    )
        
    internal_documentation_file = fields.Binary(
        string="Internal Documentation File",
        help="Upload internal documentation for this standard"
    )

    issuing_body = fields.Char(
        string="Issuing Body",
        help="Organization that issued the standard (e.g., ISO, IEC)"
    )

    parent_id = fields.Many2one(
        'mgmtsystem.standard',
        string='Parent Standard',
        help="If this standard is a sub-standard, specify the parent standard"
    )

    parent_path = fields.Char(
        string='Parent Path',
        index=True,
        help="Path to the parent standard in the hierarchy"
    )


    child_ids = fields.One2many(
        'mgmtsystem.standard',
        'parent_id',
        string='Child Standards',
        help="Sub-standards under this standard"
    )

    parent_left = fields.Integer(
        string='Parent Left',
        index=True,
        help="Left value for hierarchical structure"
    )
    
    parent_right = fields.Integer(
        string='Parent Right',
        index=True,
        help="Right value for hierarchical structure"
    )

    product_ids = fields.Many2many(
        'product.template',
        string='Products',
        help="Products related to this standard"
    )


    all_product_ids = fields.Many2many(
        'product.template',
        compute='_compute_all_product_ids',
        string='All Products Using This Standard',
        store=False,
        help='All products that use this standard (directly or via related models)'
    )

    @api.depends('product_ids')
    def _compute_all_product_ids(self):
        for record in self:
            # Direct Many2many relation
            direct_products = record.product_ids
            indirect_products = self.env['product.template']
            
            # Indirect: via mgmtsystem.standard.product (if the model exists)
            try:
                ProductStandard = self.env['mgmtsystem.standard.product']
                indirect_products = ProductStandard.search([
                    ('standard_id', '=', record.id)
                ]).mapped('product_id')
            except KeyError:
                # Model doesn't exist, skip indirect products
                indirect_products = self.env['product.template']
            
            # Union of both sets
            all_products = (direct_products | indirect_products)
            record.all_product_ids = all_products


    category_id = fields.Many2one(
        'mgmtsystem.standard.category',
        string='Category',
        index=True,
        help="Category of the standard"
    )

    domain_ids = fields.One2many(
        'mgmtsystem.standard.domain',
        'standard_id',
        string='Domains',
        help="Domains defined in this standard"
    )

    requirement_ids = fields.One2many(
        'mgmtsystem.standard.requirement',
        'standard_id',
        string='Requirements',
        help="Requirements defined in this standard"
    )
    
    document_ids = fields.Many2many(
        'ir.attachment',
        string='Documents',
        help="Related documents and attachments"
    )
    
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
        default=lambda self: self.env.user.company_id,
        help="Companies that can access this standard"
    )

    # Standard Cost Information
    standard_total_maintenance_cost_manual = fields.Float(
        string='Total Maintenance Cost (Manual Only)',
        compute='_compute_standard_costs',
        help='Total annual maintenance cost for all controls in this standard (manual only)'
    )
    
    standard_total_maintenance_cost_combined = fields.Float(
        string='Total Maintenance Cost (Manual + Automated)',
        compute='_compute_standard_costs',
        help='Total annual maintenance cost for all controls in this standard (manual + automated)'
    )
    
    standard_total_implementation_cost = fields.Float(
        string='Total Implementation Cost',
        compute='_compute_standard_costs',
        help='Total implementation cost for all controls in this standard'
    )
    
    standard_control_count = fields.Integer(
        string='Total Control Count',
        compute='_compute_standard_costs',
        help='Total number of controls in this standard'
    )

    # Compliance tracking

    # Statistics for dashboard
    control_count = fields.Integer(
        compute="_compute_statistics",
        string="Total Controls",
        store=True
    )
    
    implemented_control_count = fields.Integer(
        compute="_compute_statistics",
        string="Implemented Controls",
        store=True
    )

    compliance_score = fields.Float(
        string="Compliance Score (%)",
        compute="_compute_compliance_score",
        store=True,
        help="Overall compliance score for this standard"
    )

    last_assessment_date = fields.Date(
        string="Last Assessment",
        tracking=True
    )
    
    next_assessment_date = fields.Date(
        string="Next Assessment",
        tracking=True
    )
    
    
    @api.depends('requirement_ids', 'requirement_ids.compliance_status')
    def _compute_compliance_score(self):
        for standard in self:
            compliant_reqs = standard.requirement_ids.filtered(lambda r: r.compliance_status == 'compliant')
            total_reqs = len(standard.requirement_ids)
            standard.compliance_score = (len(compliant_reqs) / total_reqs * 100) if total_reqs else 0.0
    
    active = fields.Boolean(
        default=True, 
        help="If unchecked, it will allow you to hide this standard without removing it."
    )
    
    color = fields.Integer(string='Color Index')
    
    external_id = fields.Char(
        string="External ID",
        compute="_compute_external_id",
        help="External identifier from data import (XML ID)"
    )
    
    # Control Implementation Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('implementing', 'Implementing'),
        ('implemented', 'Implemented'),
        ('testing', 'Testing'),
        ('verified', 'Verified'),
        ('active', 'Active'),
        ('superseded', 'Superseded'),
        ('retired', 'Retired'),
        ('ineffective', 'Ineffective')
    ], string='Status', default='draft', tracking=True)
    
    superseded_by_id = fields.Many2one(
        'mgmtsystem.standard',
        string='Superseded By',
        help="If this standard has been superseded, specify the new standard"
    )
    
    supersedes_ids = fields.One2many(
        'mgmtsystem.standard',
        'superseded_by_id',
        string='Supersedes',
        help="Standards that this standard replaces"
    )
    
    @api.constrains('expiry_date', 'publication_date', 'effective_date')
    def _check_dates(self):
        for record in self:
            if record.publication_date and record.effective_date and record.publication_date > record.effective_date:
                raise ValidationError(_("Effective date cannot be earlier than publication date."))
            if record.effective_date and record.expiry_date and record.effective_date > record.expiry_date:
                raise ValidationError(_("Expiry date cannot be earlier than effective date."))

    @api.depends('domain_ids', 'domain_ids.control_ids', 'domain_ids.control_ids.implemented')
    def _compute_statistics(self):
        """Compute control statistics for this standard."""
        for record in self:
            # Get all controls linked to this standard through domains
            all_controls = self.env['mgmtsystem.standard.control'].search([
                ('standard_id', '=', record.id)
            ])
            
            record.control_count = len(all_controls)
            record.implemented_control_count = len(all_controls.filtered(
                lambda c: c.implemented
            ))
    
    @api.depends('domain_ids', 'domain_ids.control_ids', 'domain_ids.control_ids.maintenance_cost', 
                 'domain_ids.control_ids.maintenance_cost_combined', 'domain_ids.control_ids.implementation_cost')
    def _compute_standard_costs(self):
        """Compute cost statistics for all controls in this standard"""
        for record in self:
            # Get all controls linked to this standard through domains
            all_controls = self.env['mgmtsystem.standard.control'].search([
                ('standard_id', '=', record.id)
            ])
            
            record.standard_control_count = len(all_controls)
            record.standard_total_maintenance_cost_manual = sum(all_controls.mapped('maintenance_cost'))
            record.standard_total_maintenance_cost_combined = sum(all_controls.mapped('maintenance_cost_combined'))
            record.standard_total_implementation_cost = sum(all_controls.mapped('implementation_cost'))
    
    @api.depends('name', 'version')
    def _compute_code(self):
        for record in self:
            if record.name and record.version:
                record.code = f"{record.name}:{record.version}"
            else:
                record.code = record.name or ''
    
    def action_rebuild_parent_store(self):
        """Rebuild the nested set hierarchy for all domains."""
        domain_model = self.env['mgmtsystem.standard.domain']
        
        # Get all domains across all standards (needed for proper nested set rebuild)
        all_domains = domain_model.search([])
        
        if all_domains:
            try:
                # Clear existing parent_left and parent_right values
                self.env.cr.execute("""
                    UPDATE mgmtsystem_standard_domain 
                    SET parent_left = 0, parent_right = 0
                """)
                
                # Rebuild parent store using Odoo's internal method
                domain_model._parent_store_compute()
                
                # Commit the changes
                self.env.cr.commit()
                
                # Invalidate cache to ensure fresh data
                domain_model.invalidate_recordset(['parent_left', 'parent_right'])
                
                message = f'Successfully rebuilt hierarchy for {len(all_domains)} domain records.'
                notification_type = 'success'
                
            except Exception as e:
                # If rebuild fails, show error
                message = f'Error rebuilding hierarchy: {str(e)}'
                notification_type = 'danger'
            
            # Return action to reload the current form and show notification
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': message,
                    'type': notification_type,
                    'next': {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                    }
                }
            }
        else:
            # If no domains, just show a message
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'No domains found in the system.',
                    'type': 'warning',
                }
            }
    
    def _compute_external_id(self):
        """Compute the external ID (XML ID) for this record"""
        for record in self:
            data = self.env['ir.model.data'].search([
                ('model', '=', record._name),
                ('res_id', '=', record.id)
            ], limit=1)
            if data:
                record.external_id = f"{data.module}.{data.name}"
            else:
                record.external_id = False
    
    # Add a SQL constraint to ensure uniqueness per company
    _sql_constraints = [
        ('code_company_uniq', 'unique (code, company_id)', 
        'The computed code of the standard must be unique per company!')
    ]