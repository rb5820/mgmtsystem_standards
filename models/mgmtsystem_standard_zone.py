from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _

class StandardZone(models.Model):
    _name = 'mgmtsystem.standard.zone'
    _description = 'Standard Security Zone'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'
    _check_company_auto = True

    name = fields.Char(
        'Zone Name', 
        required=True,
        tracking=True,
        help="Name of the security zone (e.g., 'Authentication and Access Control')"
    )
    
    title = fields.Char(
        'Title',
        tracking=True,
        help="Title of the security zone"
    )
    
    code = fields.Char(
        'Zone Code',
        help="Short code for the zone (e.g., 'AUTH', 'NET', 'AUDIT')"
    )
    
    description = fields.Text(
        'Description',
        tracking=True,
        help="Description of the security zone and its purpose"
    )
    
    sequence = fields.Integer(
        'Sequence',
        default=10,
        help="Sequence order for displaying zones"
    )
    
    active = fields.Boolean(
        'Active',
        default=True,
        tracking=True,
        help="If unchecked, it will allow you to hide this zone without removing it."
    )
    
    standard_id = fields.Many2one(
        'mgmtsystem.standard',
        string='Standard',
        help="The standard this zone belongs to"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='standard_id.company_id',
        store=True,
        readonly=True,
        help='Company related to this zone through its standard'
    )
    
    # Related fields
    domain_ids = fields.One2many(
        'mgmtsystem.standard.domain',
        'zone_id',
        string='Domains',
        help="Domains grouped under this zone"
    )
    
    domain_count = fields.Integer(
        'Domain Count',
        compute='_compute_domain_count',
        help="Number of domains in this zone"
    )
    
    control_count = fields.Integer(
        'Control Count', 
        compute='_compute_control_count',
        help="Total number of controls across all domains in this zone"
    )
    
    @api.depends('domain_ids')
    def _compute_domain_count(self):
        for zone in self:
            zone.domain_count = len(zone.domain_ids)
    
    @api.depends('domain_ids.control_ids')
    def _compute_control_count(self):
        for zone in self:
            zone.control_count = sum(len(domain.control_ids) for domain in zone.domain_ids)
    
    @api.constrains('code')
    def _check_unique_code(self):
        for zone in self:
            if zone.code:
                existing = self.search([
                    ('code', '=', zone.code),
                    ('standard_id', '=', zone.standard_id.id),
                    ('id', '!=', zone.id)
                ])
                if existing:
                    raise ValidationError(_("Zone code must be unique within a standard."))
    
    def name_get(self):
        """Custom display name showing code and name."""
        result = []
        for zone in self:
            if zone.code:
                name = f"[{zone.code}] {zone.name}"
            else:
                name = zone.name
            result.append((zone.id, name))
        return result
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        """Search by code or name."""
        args = args or []
        if name:
            zone_ids = self._search([
                '|',
                ('code', operator, name),
                ('name', operator, name)
            ] + args, limit=limit, access_rights_uid=name_get_uid)
        else:
            zone_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return zone_ids