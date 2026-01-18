# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    # Track login notifications to avoid spam
    last_login_notification = fields.Datetime('Last Login Notification')
    enable_login_notifications = fields.Boolean('Enable Login Notifications', default=True)
    
    @api.model
    def check_login_notifications(self, force=False):
        """Check and send login notifications for current user - called from frontend"""
        user = self.env.user
        now = datetime.now()
        
        # Check if user has notifications enabled
        if not user.enable_login_notifications:
            return {
                'status': 'disabled',
                'show_popup': False,
                'message': 'Login notifications disabled for this user'
            }
        
        # Check if we should send notification (avoid spam - max once per day)
        # Unless force=True for testing purposes
        if (not force and user.last_login_notification and 
            user.last_login_notification.date() == now.date()):
            return {
                'status': 'already_sent',
                'show_popup': False,
                'message': 'Notification already sent today'
            }
            
        try:
            # Get overdue and due today items using existing notification system
            notification_configs = self.env['mgmtsystem.notification.config'].search([
                ('trigger_type', '=', 'login'),
                ('active', '=', True)
            ])
            
            if not notification_configs:
                # If no login notification config exists, use direct queries
                overdue_items = self._get_overdue_standards_and_domains()
                due_today_items = self._get_due_today_standards_and_domains()
            else:
                # Use existing notification system
                config = notification_configs[0]  # Use first active config
                overdue_data = config._get_overdue_items()
                due_today_data = config._get_due_today_items()
                
                # Convert to format expected by frontend
                overdue_items = self._format_items_for_popup(overdue_data)
                due_today_items = self._format_items_for_popup(due_today_data, is_due_today=True)
            
            if len(overdue_items) == 0 and len(due_today_items) == 0:
                if not force:  # Don't update timestamp when testing
                    user.sudo().write({'last_login_notification': now})
                return {
                    'status': 'no_items',
                    'show_popup': False,
                    'message': 'No overdue or due today items'
                }
            
            # Build notification data
            notification_data = {
                'overdue_items': overdue_items,
                'due_today_items': due_today_items
            }
            
            # Update last notification time (only if not testing)
            if not force:
                user.sudo().write({'last_login_notification': now})
            
            return {
                'status': 'has_notifications',
                'show_popup': True,
                'overdue_items': overdue_items,
                'due_today_items': due_today_items,
                'overdue_count': len(overdue_items),
                'due_today_count': len(due_today_items)
            }
            
        except Exception as e:
            _logger.error(f"Error checking login notifications: {e}")
            return {'status': 'error', 'show_popup': False, 'error': str(e)}

    def _format_items_for_popup(self, items_data, is_due_today=False):
        """Format items from notification config format for popup display"""
        formatted_items = []
        
        # Format standards
        for standard in items_data.get('standards', []):
            item = {
                'name': standard.name,
                'type': 'Standard',
                'url': f'/web#id={standard.id}&model=mgmtsystem.standard'
            }
            if not is_due_today:
                deadline = standard.deadline or standard.target_date or standard.review_date
                days_overdue = (date.today() - deadline).days if deadline else 0
                item['days_overdue'] = days_overdue
                item['deadline'] = deadline.strftime('%Y-%m-%d') if deadline else 'No deadline'
            formatted_items.append(item)
            
        # Format domains  
        for domain in items_data.get('domains', []):
            item = {
                'name': domain.name,
                'type': 'Domain',
                'url': f'/web#id={domain.id}&model=mgmtsystem.standard.domain'
            }
            if not is_due_today:
                deadline = domain.deadline or domain.target_date or domain.review_date
                days_overdue = (date.today() - deadline).days if deadline else 0
                item['days_overdue'] = days_overdue
                item['deadline'] = deadline.strftime('%Y-%m-%d') if deadline else 'No deadline'
            formatted_items.append(item)
            
        return formatted_items[:8]  # Limit to 8 items for popup

    def _get_overdue_standards_and_domains(self):
        """Get overdue standards and domains for current user"""
        today = date.today()
        
        overdue_items = []
        
        # Find overdue standards
        overdue_standards = self.env['mgmtsystem.standard'].search([
            '|', '|',
            ('deadline', '<', today),
            ('target_date', '<', today), 
            ('review_date', '<', today),
            ('active', '=', True)
        ], limit=5)
        
        for standard in overdue_standards:
            deadline = standard.deadline or standard.target_date or standard.review_date
            days_overdue = (date.today() - deadline).days if deadline else 0
            overdue_items.append({
                'name': standard.name,
                'type': 'Standard',
                'days_overdue': days_overdue,
                'deadline': deadline.strftime('%Y-%m-%d') if deadline else 'No deadline',
                'url': f'/web#id={standard.id}&model=mgmtsystem.standard'
            })
            
        # Find overdue domains  
        overdue_domains = self.env['mgmtsystem.standard.domain'].search([
            '|', '|',
            ('deadline', '<', today),
            ('target_date', '<', today),
            ('review_date', '<', today), 
            ('active', '=', True)
        ], limit=3)
        
        for domain in overdue_domains:
            deadline = domain.deadline or domain.target_date or domain.review_date
            days_overdue = (date.today() - deadline).days if deadline else 0
            overdue_items.append({
                'name': domain.name,
                'type': 'Domain',
                'days_overdue': days_overdue,
                'deadline': deadline.strftime('%Y-%m-%d') if deadline else 'No deadline',
                'url': f'/web#id={domain.id}&model=mgmtsystem.standard.domain'
            })
            
        return overdue_items
        
    def _get_due_today_standards_and_domains(self):
        """Get standards and domains due today for current user"""
        today = date.today()
        
        due_today_items = []
        
        # Find standards due today
        due_today_standards = self.env['mgmtsystem.standard'].search([
            '|', '|',
            ('deadline', '=', today),
            ('target_date', '=', today),
            ('review_date', '=', today),
            ('active', '=', True)
        ], limit=5)
        
        for standard in due_today_standards:
            due_today_items.append({
                'name': standard.name,
                'type': 'Standard',
                'url': f'/web#id={standard.id}&model=mgmtsystem.standard'
            })
            
        # Find domains due today
        due_today_domains = self.env['mgmtsystem.standard.domain'].search([
            '|', '|',
            ('deadline', '=', today),
            ('target_date', '=', today), 
            ('review_date', '=', today),
            ('active', '=', True)
        ], limit=3)
        
        for domain in due_today_domains:
            due_today_items.append({
                'name': domain.name,
                'type': 'Domain',
                'url': f'/web#id={domain.id}&model=mgmtsystem.standard.domain'
            })
            
        return due_today_items

    @api.model
    def reset_login_notification(self):
        """Reset the last login notification timestamp for testing purposes"""
        user = self.env.user
        user.sudo().write({'last_login_notification': False})
        return {'status': 'reset', 'message': 'Login notification flag reset'}

    @api.model  
    def test_login_notifications(self):
        """Test method to force show login notifications with dummy data"""
        return {
            'status': 'test_data',
            'show_popup': True,
            'overdue_items': [
                {
                    'name': 'ISO 9001:2015 Quality Management',
                    'type': 'Standard',
                    'days_overdue': 5,
                    'deadline': '2025-12-30',
                    'url': '/web#model=mgmtsystem.standard'
                },
                {
                    'name': 'Document Control Process',
                    'type': 'Domain',
                    'days_overdue': 3,
                    'deadline': '2026-01-01',
                    'url': '/web#model=mgmtsystem.standard.domain'
                }
            ],
            'due_today_items': [
                {
                    'name': 'ISO 14001:2015 Environmental Management',
                    'type': 'Standard',
                    'url': '/web#model=mgmtsystem.standard'
                },
                {
                    'name': 'Energy Management Review',
                    'type': 'Domain',
                    'url': '/web#model=mgmtsystem.standard.domain'
                }
            ],
            'overdue_count': 2,
            'due_today_count': 2
        }