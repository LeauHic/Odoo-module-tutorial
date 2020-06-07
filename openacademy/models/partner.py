# -*- coding: utf-8 -*-

from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    teacher = fields.Selection([('teacher / Level 1', 'Teacher / Level 1'), ('teacher / Level 2', 'Teacher / Level 2')])
    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)

