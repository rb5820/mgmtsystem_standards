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
    _order = "sequence, id"
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
        tracking=True
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
        compute='_compute_parent_path', 
        store=True, 
        index=True,
        help="Full path from root to current record based on letter codes"
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
         'domain_id',
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


    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this domain belongs to'
    )

    # Remove complex many2many definition
    allowed_company_ids = fields.Many2many(
        'res.company',
        string='Allowed Companies',
        default=lambda self: self.env.user.company_id,
        help="Companies that can access this domain"
    )

    owner_id = fields.Many2one(
        'res.users',
        string="Owner",
        help="User responsible for this domain"
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
    
    
    @api.depends('parent_id', 'parent_id.path_level')
    def _compute_path_level(self):
        """Compute the level in the hierarchy"""
        for record in self:
            if not record.parent_id:
                record.path_level = 1
            else:
                record.path_level = record.parent_id.path_level + 1
    
    @api.depends('control_ids', 'control_ids.implemented')
    def _compute_statistics(self):
        """Compute control statistics for this domain"""
        for record in self:
            record.control_count = len(record.control_ids)
            
            implemented = record.control_ids.filtered(lambda c: c.implemented)
            record.implemented_control_count = len(implemented)
    
    
    @api.depends('control_ids.implemented', 'control_count')
    def _compute_compliance_score(self):
        """Compute compliance score based on implemented controls"""
        for record in self:
            if record.control_count:
                record.compliance_score = (record.implemented_control_count / record.control_count) * 100
            else:
                record.compliance_score = 0
    
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