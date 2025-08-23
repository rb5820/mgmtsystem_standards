# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MgmtSystemStandardCategory(models.Model):
    """
    Management System Standard Category
    """
    _name = "mgmtsystem.standard.category"
    _description = "Management System Standard Category"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "name"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(
        string='Category',
        required=True,
        tracking=True,
    )
    description = fields.Text(
        string='Description',
        tracking=True,
    )
    parent_id = fields.Many2one(
        'mgmtsystem.standard.category',
        string='Parent Category',
        index=True,
        tracking=True,
        ondelete='cascade',
    )
    child_ids = fields.One2many(
        'mgmtsystem.standard.category',
        'parent_id',
        string='Child Categories',
    )
    parent_path = fields.Char(
        string="Parent Path",
        index=True,
    )
    standard_ids = fields.One2many(
        'mgmtsystem.standard',
        'category_id',
        string='Standards',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True,
    )
    color = fields.Integer(string='Color Index')
    complete_name = fields.Char(
        string='Complete Name',
        recursive=True,
        compute='_compute_complete_name',
        store=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
