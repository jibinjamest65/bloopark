from odoo import api, fields, models, _
from datetime import datetime
import calendar
from odoo.exceptions import UserError


class SalesSlab(models.Model):
    _name = "sales.slab"
    _description = "Sales Slab"

    salesperson_id = fields.Many2one('res.users', 'Sales Person')
    job_position = fields.Many2one('hr.job', 'Position')
    sales_team_id = fields.Many2one('crm.team', 'Team')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    percentage = fields.Float('Percentage')
    type = fields.Selection([('on_invoice', 'Invoiced Value'), ('monthly_target', 'At Monthly Target')], string='Commission Type')


class SalesTeam(models.Model):
    _inherit = "crm.team"

    commission_ids = fields.One2many('sales.slab','sales_team_id', 'Commissions')
    expense_journal_id = fields.Many2one('account.journal', 'Expense Journal')
    expense_account_id = fields.Many2one('account.account', 'Expense Account')
    regional_manager_id = fields.Many2one('res.users', 'Regional Manager')

    def action_open_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Entries'),
            'res_model': 'account.move',
            'domain': [('generated_for_sales_team_id', '=', self.id)],
            'view_mode': 'list,form',

        }




    def action_generate_invoice(self):
        date = fields.Datetime.now()
        first_day = date.replace(day=1)
        last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])
        invoices = self.env['account.move'].search([('invoice_date', '>=', first_day), ('team_id', '=', self.id),
                                                    ('invoice_date', '<=', last_day),
                                                    ('achievement_generated', '=', False),
                                                    ('move_type', '=', 'out_invoice')])

        sales_person_added = []

        for inv in invoices:
            if inv.user_id.id not in sales_person_added:
                sales_person_added.append(inv.user_id.id)
                own_invoices = invoices.filtered(lambda x: x.user_id.id == inv.user_id.id and x.team_id.id == self.id)

                inv_amount = sum(own_invoices.mapped('amount_untaxed'))
                if inv_amount >= self.invoiced_target:
                    slab_defined = inv.team_id.commission_ids.filtered(lambda
                                                                           x: inv.invoice_date >= x.date_start and inv.invoice_date <= x.date_end and x.type == 'monthly_target')
                    if slab_defined:
                        if inv.user_id:
                            if inv.user_id.id != inv.team_id.user_id.id and inv.user_id.id != inv.team_id.regional_manager_id.id:
                                user_slab = slab_defined.filtered(lambda x: x.job_position == inv.user_id.job_position)
                                self.env['sales.achievements'].create({
                                    'name': "commission from invoice" + str(inv.name),
                                    'job_position': inv.user_id.job_position.id,
                                    'sales_team_id': inv.team_id.id,
                                    'sales_person_id': inv.user_id.id,
                                    'amount': (inv.amount_untaxed * user_slab.percentage) / 100,
                                    'invoice_id': inv.id,
                                    'invoice_date': inv.invoice_date,
                                    'type': 'monthly_target',
                                })

                                if inv.team_id.user_id:
                                    user_slab = slab_defined.filtered(
                                        lambda x: x.job_position == inv.team_id.user_id.job_position)
                                    self.env['sales.achievements'].create({
                                        'name': "commission from invoice" + str(inv.name),
                                        'job_position': inv.team_id.user_id.job_position.id,
                                        'sales_team_id': inv.team_id.id,
                                        'sales_person_id': inv.team_id.user_id.id,
                                        'amount': (inv.amount_untaxed * user_slab.percentage) / 100,
                                        'invoice_id': inv.id,
                                        'invoice_date': inv.invoice_date,
                                        'type': 'monthly_target',
                                    })

                                if inv.team_id.regional_manager_id:
                                    user_slab = slab_defined.filtered(
                                        lambda x: x.job_position == inv.team_id.regional_manager_id.job_position)
                                    self.env['sales.achievements'].create({
                                        'name': "commission from invoice" + str(inv.name),
                                        'job_position': inv.team_id.regional_manager_id.job_position.id,
                                        'sales_team_id': inv.team_id.id,
                                        'sales_person_id': inv.team_id.regional_manager_id.id,
                                        'amount': (inv.amount_untaxed * user_slab.percentage) / 100,
                                        'invoice_id': inv.id,
                                        'invoice_date': inv.invoice_date,
                                        'type': 'monthly_target',
                                    })
                            elif inv.user_id.id == inv.team_id.regional_manager_id.id:
                                user_slab = slab_defined.filtered(
                                    lambda x: x.job_position == inv.team_id.regional_manager_id.job_position)
                                self.env['sales.achievements'].create({
                                    'name': "commission from invoice" + str(inv.name),
                                    'job_position': inv.team_id.regional_manager_id.job_position.id,
                                    'sales_team_id': inv.team_id.id,
                                    'sales_person_id': inv.team_id.regional_manager_id.id,
                                    'amount': (inv.amount_untaxed * user_slab.percentage) / 100,
                                    'invoice_id': inv.id,
                                    'invoice_date': inv.invoice_date,
                                    'type': 'monthly_target',
                                })
                            elif inv.user_id.id == inv.team_id.user_id.id:
                                user_slab = slab_defined.filtered(
                                    lambda x: x.job_position == inv.team_id.regional_manager_id.job_position)
                                self.env['sales.achievements'].create({
                                    'name': "commission from invoice" + str(inv.name),
                                    'job_position': inv.team_id.regional_manager_id.job_position.id,
                                    'sales_team_id': inv.team_id.id,
                                    'sales_person_id': inv.team_id.regional_manager_id.id,
                                    'amount': (inv.amount_untaxed * user_slab.percentage) / 100,
                                    'invoice_id': inv.id,
                                    'invoice_date': inv.invoice_date,
                                    'type': 'monthly_target',
                                })

        achievements = self.env['sales.achievements'].search([('invoice_date', '>=', first_day),
                                                              ('invoice_date', '<=', last_day),
                                                              ('invoiced', '=', False)])
        if not achievements:
            raise UserError("Nothing to generate")
        else:

            sales_list = []
            move_lines = []

            expense = self.env['account.move'].create({
                'journal_id': self.expense_journal_id.id,
                'name': "commission for sales person for period",
                'move_type': 'entry',
                'ref': 'Commission for Sales',
                'generated_for_sales_team_id': self.id,
            })

            for rec in achievements:
                if rec.sales_person_id.id not in sales_list:
                    sales_list.append(rec.sales_person_id.id)
                    achievement_amount = sum(achievements.filtered(lambda x: x.sales_person_id.id == rec.sales_person_id.id).mapped('amount'))

                    expense_lines_credeit = self.env['account.move.line'].with_context(check_move_validity=False).create({
                        'partner_id': rec.sales_person_id.partner_id.id,
                        'move_id': expense.id,
                        'name': 'Commission for Sales on '+rec.invoice_id.name,
                        'account_id': rec.sales_person_id.property_account_payable_id.id,
                        'credit': achievement_amount,
                        'debit': 0,
                    })
                    expense_lines_debit = self.env['account.move.line'].with_context(check_move_validity=False).create({
                        'partner_id': rec.sales_person_id.partner_id.id,
                        'move_id': expense.id,
                        'account_id': self.expense_account_id.id,
                        'name': 'Commission for Sales on '+rec.invoice_id.name,
                        'debit': achievement_amount,
                        'credit': 0,

                    })
                rec.invoiced = True


