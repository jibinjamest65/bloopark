from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    generated_for_sales_team_id = fields.Many2one('crm.team')
    achievement_generated = fields.Boolean(default=False)

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            if rec.team_id and rec.team_id.commission_ids:
                slab_defined = rec.team_id.commission_ids.filtered(lambda x: rec.invoice_date >= x.date_start and rec.invoice_date <= x.date_end and x.type == 'on_invoice')
                if not slab_defined:
                    raise UserError(" No slab is defined for this period")
                else:
                    if rec.user_id:
                        if rec.user_id.id != rec.team_id.user_id.id and rec.user_id.id != rec.team_id.regional_manager_id.id:
                            user_slab = slab_defined.filtered(lambda x:x.job_position == rec.user_id.job_position)
                            self.env['sales.achievements'].create({
                                'name': "commission from invoice"+ str(rec.name),
                                'job_position': rec.user_id.job_position.id,
                                'sales_team_id': rec.team_id.id,
                                'sales_person_id' : rec.user_id.id,
                                'amount' : (rec.amount_untaxed * user_slab.percentage)/100,
                                'invoice_id' : rec.id,
                                'invoice_date': rec.invoice_date,
                                'type': 'on_invoice',
                            })

                            if rec.team_id.user_id:
                                user_slab = slab_defined.filtered(lambda x: x.job_position == rec.team_id.user_id.job_position)
                                self.env['sales.achievements'].create({
                                    'name': "commission from invoice" + str(rec.name),
                                    'job_position': rec.team_id.user_id.job_position.id,
                                    'sales_team_id': rec.team_id.id,
                                    'sales_person_id': rec.team_id.user_id.id,
                                    'amount': (rec.amount_untaxed * user_slab.percentage) / 100,
                                    'invoice_id': rec.id,
                                    'invoice_date': rec.invoice_date,
                                    'type': 'on_invoice',
                                })

                            if rec.team_id.regional_manager_id:
                                user_slab = slab_defined.filtered(lambda x: x.job_position == rec.team_id.regional_manager_id.job_position)
                                self.env['sales.achievements'].create({
                                    'name': "commission from invoice" + str(rec.name),
                                    'job_position': rec.team_id.regional_manager_id.job_position.id,
                                    'sales_team_id': rec.team_id.id,
                                    'sales_person_id': rec.team_id.regional_manager_id.id,
                                    'amount': (rec.amount_untaxed * user_slab.percentage) / 100,
                                    'invoice_id': rec.id,
                                    'invoice_date': rec.invoice_date,
                                    'type': 'on_invoice',
                                })
                        elif rec.user_id.id == rec.team_id.regional_manager_id.id:
                            user_slab = slab_defined.filtered(
                                lambda x: x.job_position == rec.team_id.regional_manager_id.job_position)
                            self.env['sales.achievements'].create({
                                'name': "commission from invoice" + str(rec.name),
                                'job_position': rec.team_id.regional_manager_id.job_position.id,
                                'sales_team_id': rec.team_id.id,
                                'sales_person_id': rec.team_id.regional_manager_id.id,
                                'amount': (rec.amount_untaxed * user_slab.percentage) / 100,
                                'invoice_id': rec.id,
                                'invoice_date': rec.invoice_date,
                                'type': 'on_invoice',
                            })
                        elif rec.user_id.id == rec.team_id.user_id.id:
                            user_slab = slab_defined.filtered(
                                lambda x: x.job_position == rec.team_id.regional_manager_id.job_position)
                            self.env['sales.achievements'].create({
                                'name': "commission from invoice" + str(rec.name),
                                'job_position': rec.team_id.regional_manager_id.job_position.id,
                                'sales_team_id': rec.team_id.id,
                                'sales_person_id': rec.team_id.regional_manager_id.id,
                                'amount': (rec.amount_untaxed * user_slab.percentage) / 100,
                                'invoice_id': rec.id,
                                'invoice_date': rec.invoice_date,
                                'type': 'on_invoice',
                            })
                        rec.achievement_generated = True
        return res

