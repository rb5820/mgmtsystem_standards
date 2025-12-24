from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, ValidationError
from odoo import _

class StandardControl(models.Model):
    _name = 'mgmtsystem.standard.control'
    _description = 'Standard Control'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    name = fields.Char('Name', required=False)
    
    reference = fields.Char('Control ID', required=False)
    
    description = fields.Text('Description')
    
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide this control without removing it.")

    external_id = fields.Char(
        string="External ID",
        compute="_compute_external_id",
        help="External identifier from data import (XML ID)"
    )

    implemented = fields.Boolean('Implemented', compute='_compute_implemented', store=True, 
                               help="Indicates if the control is currently implemented.")
    
    title = fields.Char(
        string='Title',
        required=False,
        tracking=True,
        help="The official title of the control as defined in the standard framework"
    )

    standard_id = fields.Many2one(
        'mgmtsystem.standard',
        string='Standard',
        required=False,
        help="The framework standard this control is associated with"
    )

    # Control Code
    code = fields.Char(
        string='Control Code',
        required=False,
        help="Unique code identifying the control"
    )

 

        # Link to framework domain
    domain_id = fields.Many2one(
        'mgmtsystem.standard.domain',
        string='Standard Domain',
        tracking=True,
        help="The domain or category this control belongs to within the standard framework"
    )

    # Rationale Statement
    rationale = fields.Text(
        string="Rationale Statement",
        help="The rationale behind implementing this control"
    )

    # Impact Statement
    impact = fields.Text(
        string="Impact Statement",
        help="The potential impact of not implementing this control"
    )

    # Remediation Procedure
    remediation = fields.Text(
        string="Remediation Procedure",
        help="Steps to remediate issues identified by this control"
    )

    # Audit Procedure
    audit = fields.Text(
        string="Audit Procedure",
        help="Steps to audit the effectiveness of this control"
    )

    expected_value = fields.Char(
        string="Expected Value",
        help="The expected value or outcome of this control"
    )

    default_value = fields.Char(
        string="Default Value",
        help="The default value of this control"
    )  

    external_references = fields.Text( 
        string="External References",
        help="References to external documents or sources related to this control"
    )


    # CIS Controls

    # odoo list sequence

    sequence = fields.Integer(
        'Sequence',
        default=10,
        help="Sequence order for displaying controls"
    )



    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env.company,
        help="Company to which the control belongs."
    )

    allowed_company_ids = fields.Many2many(
        'res.company',
        string='Allowed Companies',
        default=lambda self: self.env.user.company_id,
        help="List of allowed companies for this control"
    )

    additional_information = fields.Text(
        string="Additional Information",
        help="Any additional information related to this domain"
    )   

    implementation_details = fields.Text(
        string="Implementation Details",
        help="Details on how the control is implemented"
    )
    test_procedure = fields.Text(
        string="Test Procedure",
        help="Details on how the control is tested"
    )

    owner_id = fields.Many2one(
        'res.users',
        string="Owner",
        help="User responsible for this domain"
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
        ('ineffective', 'Ineffective'),
        ('retired', 'Retired')
    ], string='Status', default='draft', tracking=True)

    asset_class = fields.Selection([
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('applications', 'Applications'),
        ('network', 'Network'),
        ('devices', 'Devices'),
        ('mobile', 'Mobile'),
        ('data', 'Data'),
        ('users', 'Users'),
        ('people', 'People'),
        ('process', 'Process'),
        ('physical', 'Physical'),
        ('endpoints', 'Endpoints'),
        ('cloud', 'Cloud'),
        ('iot', 'IoT'),
        ('other', 'Other')
    ], string='Asset Class', default='other')

    # Control Details
    control_type = fields.Selection([
        ('identify', 'Identify'),
        ('protect', 'Protect'),
        ('detect', 'Detect'),
        ('respond', 'Respond'),
        ('recover', 'Recover'),
        ('preventive', 'Preventive'),
        ('detective', 'Detective'),
        ('corrective', 'Corrective'),
        ('administrative', 'Administrative'),
        ('physical', 'Physical'),
        ('governance', 'Governance'),
        ('management', 'Management'),
        ('technical', 'Technical'),
        ('policy', 'Policy'),
        ('compensating', 'Compensating')
    ], string='Control Type', required=False)
    
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority', default='medium')


    #FIXME RB5820: added is_required field to indicate if the control is mandatory abd to avoid error
    is_required = fields.Boolean(
        string='Not Required',
        default=False,
        help="Indicates if this control is not required for this company"
    )
    
    # Effectiveness Metrics
    effectiveness_score = fields.Float('Effectiveness Score', compute='_compute_effectiveness_score')
    last_assessment_date = fields.Date('Last Assessment Date')
    implementation_time = fields.Float('Implementation Time (hours)', help="Estimated time to implement this control")
    implementation_cost = fields.Float('Implementation Cost')
    maintenance_time = fields.Float('Maintenance Time (minutes) per test frequency', help="Estimated time to maintain this control per test frequency")
    maintenance_cost = fields.Float('Annual Maintenance Cost')
    
    # Testing and Verification
    test_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi_annual', 'Semi-Annual'),
        ('annual', 'Annual')
    ], string='Test Frequency')
    last_test_date = fields.Date('Last Test Date')
    next_test_date = fields.Date('Next Test Date', compute='_compute_next_test_date')
    # Commenting out references to non-existent model to avoid errors
    # test_results = fields.One2many('mgmtsystem.standard.control.test', 'control_id', 
    #                               string='Test Results')
    test_count = fields.Integer('Test Count', default=0) # compute='_compute_test_count'
    action_count = fields.Integer('Action Count', default=0) # compute='_compute_action_count'

    # Workflow Dates
    approval_date = fields.Date('Approval Date', tracking=True, readonly=True)
    implementation_date = fields.Date('Implementation Date', tracking=True, readonly=True)
    verification_date = fields.Date('Verification Date', tracking=True, readonly=True)
    retirement_date = fields.Date('Retirement Date', tracking=True, readonly=True)

    # Approvers
    approver_id = fields.Many2one('res.users', string='Approved By', tracking=True, readonly=True)
    verifier_id = fields.Many2one('res.users', string='Verified By', tracking=True, readonly=True)

    # Commenting out compute methods that reference non-existent model
    # @api.depends('test_results')
    # def _compute_test_count(self):
    #     for control in self:
    #         control.test_count = len(control.test_results)

    # @api.depends('test_results.requires_remediation')
    # def _compute_action_count(self):
    #     for control in self:
    #         domain = [
    #             ('type_action', '=', 'standard'),
    #             ('reference', '=', 'mgmtsystem.standard.control,%s' % control.id)
    #         ]
    #         control.action_count = self.env['mgmtsystem.action'].search_count(domain)

    # Commenting out due to potential dependency issues
    # def action_view_actions(self):
    #     self.ensure_one()
    #     action = self.env['ir.actions.act_window']._for_xml_id('mgmtsystem_action.action_mgmtsystem_actions')
    #     action['domain'] = [
    #         ('type_action', '=', 'standard'),
    #         ('reference', '=', 'mgmtsystem.standard.control,%s' % self.id)
    #     ]
    #     action['context'] = {
    #         'default_type_action': 'standard',
    #         'default_reference': 'mgmtsystem.standard.control,%s' % self.id
    #     }
    #     return action

    # Related Records
    # asset_ids = fields.Many2many(
    #     'mgmtsystem.standard.asset.primary', 
    #     'mgmtsystem_standard_control_asset_rel',
    #     'control_id', 
    #     'asset_id',
    #     string='Protected Assets'
    # )
    # threat_ids = fields.Many2many(
    #     'mgmtsystem.standard.threat.source', 
    #     'mgmtsystem_standard_control_threat_rel',
    #     'control_id', 
    #     'threat_id',
    #     string='Mitigated Threats'
    # )
    control_owner_id = fields.Many2one('res.users', string='Control Owner')
    document_ids = fields.Many2many('ir.attachment', string='Documentation')
    
    # Automated Assessment
    automated_assessment = fields.Boolean('Automated Assessment')
    # assessment_tool = fields.Char('Assessment Tool/Integration')
    assessment_tools = fields.Many2many(
        'mgmtsystem.standard.control.assessment.tool',
        'control_assessment_tool_rel',  # short relation table name
        'control_id',                   # column for this model
        'assessment_tool_id',           # column for the related model
        string='Assessment Tools',
        help='Tools or integrations used for automated assessment of this control'
    )

    # Automated Check

    last_automated_check = fields.Datetime('Last Automated Check')
    automated_check_result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('warning', 'Warning')
    ], string='Automated Check Result')

    @api.depends('state', 'automated_check_result')
    def _compute_effectiveness_score(self):
        for control in self:
            if control.state not in ['implemented', 'verified']:
                control.effectiveness_score = 0
                continue
                
            # Base score (simplified for now)
            base_score = 50
            
            # Adjust based on automated checks if available
            if control.automated_assessment:
                if control.automated_check_result == 'pass':
                    base_score *= 1.2
                elif control.automated_check_result == 'fail':
                    base_score *= 0.6
                elif control.automated_check_result == 'warning':
                    base_score *= 0.8
            
            control.effectiveness_score = min(100, base_score)

    @api.depends('last_test_date', 'test_frequency')
    def _compute_next_test_date(self):
        for control in self:
            if not control.last_test_date or not control.test_frequency:
                control.next_test_date = False
                continue
                
            freq_months = {
                'monthly': 1,
                'quarterly': 3,
                'semi_annual': 6,
                'annual': 12
            }
            months = freq_months.get(control.test_frequency, 12)
            control.next_test_date = fields.Date.from_string(control.last_test_date) + timedelta(days=30*months)

    @api.model
    def _cron_check_control_testing(self):
        """Scheduled action to check controls requiring testing"""
        due_controls = self.search([
            ('next_test_date', '<=', fields.Date.today()),
            ('state', 'in', ['implemented', 'verified'])
        ])
        
        for control in due_controls:
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'note': f'Control {control.code} is due for testing',
                'user_id': control.control_owner_id.id or self.env.user.id,
                'res_id': control.id,
                'res_model_id': self.env['ir.model']._get(self._name).id,
            })

    @api.model
    def is_allowed_state_transition(self, current_state, new_state):
        """Check if the current user is allowed to perform the state transition"""
        user = self.env.user
        #FIXME RB5820: check standard groups
        return True
        #is_manager = user.has_group('mgmtsystem_standard_event.group_standard_manager')
        is_reviewer = user.has_group('mgmtsystem_standard_event.group_standard_reviewer')
        is_manager = True
        
        # Managers can perform any transition
        if is_manager:
            return True
            
        # Reviewers can verify implemented controls
        if is_reviewer and current_state == 'implemented' and new_state == 'verified':
            return True
            
        # Reviewers can mark controls as ineffective
        if is_reviewer and new_state == 'ineffective':
            return True
            
        # Other transitions are not allowed for non-managers
        return False

    def write(self, vals):
        """Override write to check state transitions"""
        if 'state' in vals:
            for record in self:
                if not self.is_allowed_state_transition(record.state, vals['state']):
                    raise AccessError(_('You are not allowed to change the state of this control.'))
        return super().write(vals)

    def action_submit_review(self):
        """Submit control for review"""
        self.ensure_one()
        if not self.control_owner_id:
            raise ValidationError(_('Please assign a control owner before submitting for review.'))
        self.write({'state': 'review'})

    def action_approve(self):
        """Approve control for implementation"""
        self.ensure_one()
        if not self.env.user.has_group('mgmtsystem_standard_event.group_standard_manager'):
            raise AccessError(_('Only managers can approve controls.'))
        self.write({
            'state': 'approved',
            'approval_date': fields.Date.today(),
            'approver_id': self.env.user.id
        })

    def action_start_implementation(self):
        """Start control implementation"""
        self.ensure_one()
        if self.state != 'approved':
            raise ValidationError(_('Control must be approved before implementation.'))
        self.write({'state': 'implementing'})

    def action_mark_implemented(self):
        """Mark control as implemented"""
        self.ensure_one()
        self.write({
            'state': 'implemented',
            'implementation_date': fields.Date.today()
        })

    def action_start_testing(self):
        """Start control testing"""
        self.ensure_one()
        if self.state not in ['implemented', 'ineffective']:
            raise ValidationError(_('Control must be implemented before testing.'))
        self.write({'state': 'testing'})

    def action_mark_verified(self):
        """Mark control as verified after successful testing"""
        self.ensure_one()
        if not self.env.user.has_group('mgmtsystem_standard_event.group_standard_reviewer'):
            raise AccessError(_('Only reviewers can verify controls.'))
        if not self.last_test_date or self.last_test_date < fields.Date.today() - timedelta(days=30):
            raise ValidationError(_('A recent test (within 30 days) is required before verification.'))
        self.write({
            'state': 'verified',
            'verification_date': fields.Date.today(),
            'verifier_id': self.env.user.id
        })

    def action_mark_ineffective(self):
        """Mark control as ineffective and create improvement action"""
        self.ensure_one()
        if not self.env.user.has_group('mgmtsystem_standard_event.group_standard_reviewer'):
            raise AccessError(_('Only reviewers can mark controls as ineffective.'))
        self.write({'state': 'ineffective'})
        
        # Commented out action creation to avoid potential dependency errors
        # Create improvement action
        # self.env['mgmtsystem.action'].create({
        #     'name': f'Improve Ineffective Control: {self.name}',
        #     'type_action': 'standard',
        #     'priority': 'high',
        #     'user_id': self.control_owner_id.id,
        #     'description': f"""
        # Control marked as ineffective:
        # - Control: {self.name} ({self.reference})
        # - Standard: {self.standard_id.name}
        # - Current Effectiveness Score: {self.effectiveness_score}%
        # 
        # Action Required:
        # 1. Review control design and implementation
        # 2. Identify improvement opportunities
        # 3. Implement necessary changes
        # 4. Schedule re-testing
        # 
        # Please update the control and schedule a new test once improvements are made.
        #     """.strip()
        # })

    def action_retire(self):
        """Retire a control"""
        self.ensure_one()
        if not self.env.user.has_group('mgmtsystem_standard_event.group_standard_manager'):
            raise AccessError(_('Only managers can retire controls.'))
        self.write({
            'state': 'retired',
            'retirement_date': fields.Date.today(),
            'active': False
        })

    @api.constrains('state', 'control_owner_id', 'test_frequency')
    def _check_required_fields(self):
        """Ensure required fields are set based on state"""
        for record in self:
            if record.state in ['review', 'approved']:
                if not record.control_owner_id:
                    raise ValidationError(_('Control owner is required.'))
                if not record.test_frequency:
                    raise ValidationError(_('Test frequency must be defined.'))

    def _read_group_state_ids(self, states, domain, order):
        """Read group customization to present all states in kanban view"""
        return [key for key, val in type(self).state.selection]

    @api.depends('state')
    def _compute_implemented(self):
        """Determine if control is implemented based on its state"""
        for control in self:
            control.implemented = control.state in ['implemented', 'verified']

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
