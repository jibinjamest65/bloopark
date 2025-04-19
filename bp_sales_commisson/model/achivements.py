from odoo import api, fields, models, _

class SalesAchievements(models.Model):
    _name = "sales.achievements"
    _description = "Sales Achievements"

    name = fields.Char('Name')
    job_position = fields.Many2one('hr.job', 'Position')
    sales_team_id = fields.Many2one('crm.team', 'Team')
    sales_person_id = fields.Many2one('res.users', 'Sales Person')
    amount = fields.Float('Amount')
    invoice_id = fields.Many2one('account.move', 'Invoice')
    invoice_date = fields.Date('Invoice Date')
    invoiced = fields.Boolean(default=False, string='Invoiced')
    type = fields.Selection([('on_invoice', 'Invoiced Value'), ('monthly_target', 'At Monthly Target')], string='Commission Type')



