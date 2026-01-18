# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StandardDomain(models.Model):
    """Standard Domain Model

    This model represents domains or categories within standard standards,
    such as sections in ISO 27001 or domains in NIST CSF.
    """
    _name = "mgmtsystem.standard.domain"
    _description = "Standard Domain"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _parent_name = 'parent_id'  # 🛡️ SECURITY: Define parent field for hierarchy
    _parent_store = True  # 🛡️ SECURITY: Store parent-child relationships for hierarchy integrity
    _order = "parent_left,sequence, id"
    _check_company_auto = True
       
    
    name = fields.Char(
        string="Domain Name",
        required=True,
        tracking=True,
        help="Name of the standard domain or category"
    )

    title = fields.Char(
        string="Domain Title",
        required=True,
        tracking=True,
        help="Title of the standard domain (e.g., Information Security)"
    )

    version = fields.Char(
        string="Version",
        tracking=True,
        help="Version or edition of the standard (e.g., 2022)"
    )
    
    reference = fields.Char(
        string="Reference",
        tracking=True,
        help="Reference code for this domain (e.g., A.5, ID.AM)"
    )
    
    description = fields.Text(
        string="Description",
        help="Description of this domain's purpose and scope"
    )

    domain_requirements = fields.Text(
        string="Domain Requirements",
        help="Requirements or controls associated with this domain"
    )

    domain_rationale = fields.Text(
        string="Domain Rationale",
        help="Rationale for the existence of this domain"
    )

    additional_information = fields.Text(
        string="Additional Information",
        help="Any additional information related to this domain"
    )   

    standard_id = fields.Many2one(
        'mgmtsystem.standard',
        string="Standard",
        required=True,
        ondelete='cascade',
        readonly=True,
        tracking=True,
        help="Standard this domain belongs to (cannot be changed after creation)"
    )
    
    zone_id = fields.Many2one(
        'mgmtsystem.standard.zone',
        string="Security Zone",
        help="Security zone this domain belongs to"
    ) 

    # ========================================================================= 
    # HIERARCHY FIELDS - 🛡️ STRUCTURAL INTEGRITY
    # ============================================================================

    parent_id = fields.Many2one(
        'mgmtsystem.standard.domain',
        string="Parent Domain",
        domain="[('standard_id', '=', standard_id)]",
        ondelete='cascade',
        tracking=True,
        help="Parent domain if this is a subdomain"
    )

    parent_path = fields.Char(
        string="Parent Path", 
        index=True,
        help="Full path from root to current record (automatically maintained by parent store)"
    )

    parent_left = fields.Integer(
        string='Left Parent', 
        index=True
    )

    parent_right = fields.Integer(
        string='Right Parent', 
        index=True
    )

    path_level = fields.Integer(
        string='Path Level',
        compute='_compute_path_level',
        recursive=True,  # 🛡️ SECURITY: Recursive hierarchy computation
        store=True,
        help='Level in the Reference Designation System hierarchy (1=top level, 2=second level, etc.)'
    )
    
    child_ids = fields.One2many(
        'mgmtsystem.standard.domain',
        'parent_id',
        string="Subdomains",
        help="Child domains or subcategories"
    )

    #  allow reuse of existing controls
    control_ids = fields.Many2many(
        'mgmtsystem.standard.control',
        'mgmtsystem_standard_domain_control_rel',
        'domain_id',
        'control_id',
        string="Controls",
        help="Standard controls within this domain"
    )

    product_ids = fields.Many2many(
        'product.product',
        string="Related Products",
        help="Products or services related to this domain"
    )
    
    # Domain Implementation Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('implementing', 'Implementing'),
        ('implemented', 'Implemented'),
        ('testing', 'Testing'),
        ('verified', 'Verified'),
        ('ineffective', 'Ineffective'),
        ('retired', 'Retired')
    ], string='Status', default='draft', tracking=True)
    
    sequence = fields.Integer(
        default=10,
        help="Sequence order for displaying domains"
    )


    
    color = fields.Integer(
        string="Color Index"
    )
    
    # Compliance tracking
    compliance_score = fields.Float(
        string="Compliance Score (%)",
        compute="_compute_compliance_score",
        store=True,
        help="Compliance score for this domain based on control implementation"
    )
    
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], 
        string="Priority",
        default='medium',
        tracking=True,
        help="Priority of this domain for implementation"
    )

    # Domain Cost Information
    domain_total_maintenance_cost_manual = fields.Float(
        string='Total Maintenance Cost (Manual Only)',
        compute='_compute_domain_costs',
        help='Total annual maintenance cost for all controls in this domain (manual only)'
    )
    
    domain_total_maintenance_cost_combined = fields.Float(
        string='Total Maintenance Cost (Manual + Automated)',
        compute='_compute_domain_costs',
        help='Total annual maintenance cost for all controls in this domain (manual + automated)'
    )
    
    domain_total_implementation_cost = fields.Float(
        string='Total Implementation Cost',
        compute='_compute_domain_costs',
        help='Total implementation cost for all controls in this domain'
    )
    
    domain_control_count = fields.Integer(
        string='Control Count',
        compute='_compute_domain_costs',
        help='Number of controls in this domain'
    )
    
    # Domain Time Information
    domain_total_maintenance_time_manual = fields.Float(
        string='Total Maintenance Time (Manual Only - minutes)',
        compute='_compute_domain_costs',
        help='Total annual maintenance time for all controls in this domain (manual only)'
    )
    
    domain_total_maintenance_time_combined = fields.Float(
        string='Total Maintenance Time (Combined - minutes)',
        compute='_compute_domain_costs',
        help='Total annual maintenance time for all controls in this domain (automated when available)'
    )
    
    domain_total_maintenance_hours_manual = fields.Float(
        string='Total Maintenance Hours (Manual Only)',
        compute='_compute_domain_costs',
        help='Total annual maintenance hours for all controls in this domain (manual only)'
    )
    
    domain_total_maintenance_hours_combined = fields.Float(
        string='Total Maintenance Hours (Combined)',
        compute='_compute_domain_costs',
        help='Total annual maintenance hours for all controls in this domain (automated when available)'
    )


    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='standard_id.company_id',
        store=True,
        readonly=True,
        help='Company this domain belongs to (inherited from parent standard)'
    )

    # Remove complex many2many definition
    allowed_company_ids = fields.Many2many(
        'res.company',
        string='Allowed Companies',
        related='standard_id.allowed_company_ids',
        readonly=True,
        help="Companies that can access this domain (inherited from parent standard)"
    )

    owner_id = fields.Many2one(
        'res.users',
        string="Owner",
        help="User responsible for this domain"
    )
    
    external_id = fields.Char(
        string="External ID",
        compute="_compute_external_id",
        help="External identifier from data import (XML ID)"
    )
        
    active = fields.Boolean(
        default=True, 
        help="If unchecked, it will allow you to hide this standard without removing it."
    )

    # Statistics
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
    
    child_domain_count = fields.Integer(
        compute="_compute_statistics",
        string="Child Domains",
        store=True,
        help="Number of child domains under this domain"
    )
    
    
    @api.depends('parent_id', 'parent_id.path_level')
    def _compute_path_level(self):
        """Compute the level in the hierarchy"""
        for record in self:
            if not record.parent_id:
                record.path_level = 1
            else:
                record.path_level = record.parent_id.path_level + 1
    
    @api.depends('control_ids', 'control_ids.implemented', 'child_ids', 'child_ids.control_ids', 'child_ids.control_ids.implemented')
    def _compute_statistics(self):
        """Compute control statistics for this domain and all descendants"""
        for record in self:
            # Get all descendant domains using parent_path for efficiency
            descendant_domains = record._get_all_descendant_domains()
            
            # Count all controls from this domain and all descendants
            all_controls = record.env['mgmtsystem.standard.control'].search([
                ('domain_id', 'in', descendant_domains.ids + [record.id])
            ])
            
            record.control_count = len(all_controls)
            
            implemented = all_controls.filtered(lambda c: c.implemented)
            record.implemented_control_count = len(implemented)
            
            # Count direct child domains only (immediate children)
            record.child_domain_count = len(record.child_ids)
    
    @api.depends('control_ids', 'control_ids.maintenance_cost', 'control_ids.maintenance_cost_combined', 
                 'control_ids.implementation_cost', 'control_ids.total_annual_maintenance_time',
                 'control_ids.total_annual_maintenance_time_combined')
    def _compute_domain_costs(self):
        """Compute cost and time statistics for all controls in this domain"""
        for record in self:
            # Get all descendant domains using parent_path for efficiency
            descendant_domains = record._get_all_descendant_domains()
            
            # Get all controls from this domain and all descendants
            all_controls = record.env['mgmtsystem.standard.control'].search([
                ('domain_id', 'in', descendant_domains.ids + [record.id])
            ])
            
            record.domain_control_count = len(all_controls)
            record.domain_total_maintenance_cost_manual = sum(all_controls.mapped('maintenance_cost'))
            record.domain_total_maintenance_cost_combined = sum(all_controls.mapped('maintenance_cost_combined'))
            record.domain_total_implementation_cost = sum(all_controls.mapped('implementation_cost'))
            
            # Time calculations
            record.domain_total_maintenance_time_manual = sum(all_controls.mapped('total_annual_maintenance_time'))
            record.domain_total_maintenance_time_combined = sum(all_controls.mapped('total_annual_maintenance_time_combined'))
            record.domain_total_maintenance_hours_manual = record.domain_total_maintenance_time_manual / 60.0
            record.domain_total_maintenance_hours_combined = record.domain_total_maintenance_time_combined / 60.0
    
    def _get_all_descendant_domains(self):
        """Get all descendant domains efficiently using parent_path"""
        if not self.parent_path:
            return self.env['mgmtsystem.standard.domain'].browse()
        
        # Use parent_path to find all descendants efficiently
        return self.env['mgmtsystem.standard.domain'].search([
            ('parent_path', 'like', self.parent_path + '%'),
            ('id', '!=', self.id),
            ('standard_id', '=', self.standard_id.id)
        ])
    
    
    @api.depends('control_ids.implemented', 'control_count')
    def _compute_compliance_score(self):
        """Compute compliance score based on implemented controls"""
        for record in self:
            if record.control_count:
                record.compliance_score = (record.implemented_control_count / record.control_count) * 100
            else:
                record.compliance_score = 0    
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
    def name_get(self):
        """Custom name display to include the reference code"""
        result = []
        for record in self:
            name = record.name
            if record.reference:
                name = f"[{record.reference}] {name}"
            result.append((record.id, name))
        return result
    
    def action_view_controls(self):
        """View controls for this domain"""
        self.ensure_one()
        return {
            'name': _('Domain Controls'),
            'type': 'ir.actions.act_window',
            'res_model': 'mgmtsystem.standard.control',
            'view_mode': 'list,form',
            'domain': [('domain_id', '=', self.id)],
            'context': {
                'default_domain_id': self.id,
                'default_standard_id': self.standard_id.id,
            }
        }
    
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
    
    def action_rebuild_parent_store(self):
        """Rebuild the nested set model (parent_left/right) for all domains"""
        self.env['mgmtsystem.standard.domain']._parent_store_compute()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    @api.model
    def recompute_parent_store(self):
        """Manually recompute parent store for all records"""
        self._parent_store_compute()
        return True