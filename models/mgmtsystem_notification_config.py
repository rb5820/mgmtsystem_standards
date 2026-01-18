# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import logging

_logger = logging.getLogger(__name__)


class MgmtSystemNotificationConfig(models.Model):
    _name = 'mgmtsystem.notification.config'
    _description = 'Management System Notification Configuration'
    
    name = fields.Char('Name', required=True, default='Default Notification Config')
    active = fields.Boolean('Active', default=True)
    
    # Login notification settings
    enable_login_notifications = fields.Boolean('Enable Login Notifications', default=True)
    notification_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], string='Notification Frequency', default='daily')
    
    # What to include in notifications
    include_overdue_standards = fields.Boolean('Include Overdue Standards', default=True)
    include_due_today_standards = fields.Boolean('Include Due Today Standards', default=True)
    include_overdue_domains = fields.Boolean('Include Overdue Domains', default=True)
    include_due_today_domains = fields.Boolean('Include Due Today Domains', default=True)
    
    # Limits
    max_overdue_items = fields.Integer('Max Overdue Items to Show', default=5)
    max_due_today_items = fields.Integer('Max Due Today Items to Show', default=5)
    
    def _get_overdue_items(self):
        """Get overdue standards and domains"""
        today = date.today()
        
        overdue_data = {
            'standards': self.env['mgmtsystem.standard'],
            'domains': self.env['mgmtsystem.standard.domain'],
            'count': 0
        }
        
        if self.include_overdue_standards:
            # Find overdue standards
            overdue_standards = self.env['mgmtsystem.standard'].search([
                '|', '|',
                ('deadline', '<', today),
                ('target_date', '<', today),
                ('review_date', '<', today),
                ('active', '=', True)
            ])
            overdue_data['standards'] = overdue_standards[:self.max_overdue_items]
            overdue_data['count'] += len(overdue_standards)
        
        if self.include_overdue_domains:
            # Find overdue domains
            overdue_domains = self.env['mgmtsystem.standard.domain'].search([
                '|', '|',
                ('deadline', '<', today),
                ('target_date', '<', today),
                ('review_date', '<', today),
                ('active', '=', True)
            ])
            overdue_data['domains'] = overdue_domains[:self.max_overdue_items]
            overdue_data['count'] += len(overdue_domains)
        
        return overdue_data
    
    def _get_due_today_items(self):
        """Get standards and domains due today"""
        today = date.today()
        
        due_today_data = {
            'standards': self.env['mgmtsystem.standard'],
            'domains': self.env['mgmtsystem.standard.domain'],
            'count': 0
        }
        
        if self.include_due_today_standards:
            # Find standards due today
            due_today_standards = self.env['mgmtsystem.standard'].search([
                '|', '|',
                ('deadline', '=', today),
                ('target_date', '=', today),
                ('review_date', '=', today),
                ('active', '=', True)
            ])
            due_today_data['standards'] = due_today_standards[:self.max_due_today_items]
            due_today_data['count'] += len(due_today_standards)
        
        if self.include_due_today_domains:
            # Find domains due today
            due_today_domains = self.env['mgmtsystem.standard.domain'].search([
                '|', '|',
                ('deadline', '=', today),
                ('target_date', '=', today),
                ('review_date', '=', today),
                ('active', '=', True)
            ])
            due_today_data['domains'] = due_today_domains[:self.max_due_today_items]
            due_today_data['count'] += len(due_today_domains)
        
        return due_today_data
    
    @api.model
    def get_default_config(self):
        """Get or create default notification configuration"""
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            config = self.create({
                'name': 'Default Notification Configuration',
                'active': True,
            })
        return config