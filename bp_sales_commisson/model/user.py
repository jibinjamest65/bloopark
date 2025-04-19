from odoo import api, fields, models, _
from odoo.exceptions import UserError


class User(models.Model):
    _inherit = "res.users"

    job_position = fields.Many2one('hr.job', 'Job Position')
