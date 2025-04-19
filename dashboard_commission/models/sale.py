
import pytz
from datetime import datetime, timedelta
from odoo import api, models
import calendar

class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.model
    def get_dashboard_metrics(self, start=False, end=False, sales_team=False):

        domain = [('move_type', 'in', ['out_invoice'])]

        achieve_domain = []


        if sales_team == "all" or not sales_team:
            sales_team_all = self.env['crm.team'].search([])
            domain.append(('team_id', 'in', sales_team_all.ids))
            achieve_domain.append(('sales_team_id', 'in', sales_team_all.ids))
        else:
            domain.append(('team_id', '=', int(sales_team)))
            achieve_domain.append(('sales_team_id', '=', int(sales_team)))

        if start:
            domain.append(('invoice_date', '>=', start))
            achieve_domain.append(('invoice_date', '>=', start))
        if end:
            domain.append(('invoice_date', '<=', end))
            achieve_domain.append(('invoice_date', '<=', end))

        achievements = self.env['sales.achievements'].search(achieve_domain)
        # achievements_list = achievements.read(['job_position', 'sales_team_id', 'sales_person_id', 'amount', 'invoice_id', 'invoice_date', 'type'])
        achievements_list = [
            {
                'job_position': rec_achieve.job_position.name,
                'sales_team_id': rec_achieve.sales_team_id.name,
                'sales_person_id': rec_achieve.sales_person_id.name,
                'amount': rec_achieve.amount,
                'invoice_id': rec_achieve.invoice_id.name,
                'type': rec_achieve.type,
                'date': rec_achieve.invoice_date.strftime('%Y-%m-%d') if rec_achieve.invoice_date else None
            }
            for rec_achieve in achievements]
        orders = self.env['account.move'].search(domain)
        total_sales = sum(orders.mapped('amount_untaxed'))

        # Example: Dummy tiers logic
        commission_by_tier = {'Sales rep': 0.0, 'Team Lead': 0.0, 'Manager': 0.0}
        for achieve in achievements:
            if achieve.job_position.name == 'Sales rep':
                commission_by_tier['Sales rep'] += achieve.amount
            if achieve.job_position.name == 'Team Lead':
                commission_by_tier['Team Lead'] += achieve.amount
            if achieve.job_position.name == 'Manager':
                commission_by_tier['Manager'] += achieve.amount


        # Sales trend over past 6 months
        labels, values = [], []
        today = datetime.today()
        month_start = today.replace(day=1)
        month_end = today.replace(day=calendar.monthrange(today.year, today.month)[1])

        # month_start = (today.replace(day=1) - timedelta(days=30)).replace(day=1)
        # month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        if start or end:
            if start:
                month_start = start
            if end:
                month_end = end

        monthly_orders = self.search([('date_order', '>=', month_start), ('date_order', '<=', month_end)])

        if isinstance(month_start, str):
            month_start = datetime.strptime(month_start, "%Y-%m-%d")
        labels.append(month_start.strftime('%b %Y'))
        values.append(sum(monthly_orders.mapped('amount_total')))

        position_list = [
            {
                'job_position': rec_achieve.job_position.name,
                'sales_team_id': rec_achieve.sales_team_id.name,
                'sales_person_id': rec_achieve.sales_person_id.name,
                'amount': rec_achieve.amount,
                'invoice_id': rec_achieve.invoice_id.name,
                'type': rec_achieve.type,
                'date': rec_achieve.invoice_date.strftime('%Y-%m-%d') if rec_achieve.invoice_date else None
            }
            for rec_achieve in achievements]

        sales_team_liest = [{
            'id': rec.id,
            'name': rec.name,
        } for rec in self.env['crm.team'].search([])]



        vals = {
            'total_sales': total_sales,
            'commission_distribution': list(commission_by_tier.keys()),
            'commission_distribution_vals': list(commission_by_tier.values()),
            'trend_labels': labels,
            'trend_values': values,
            'sales_teams': sales_team_liest,
        }

        return vals


# class PosOrder(models.Model):
#     """ Inherited class of pos dashboard to add features of dashboard"""
#     _inherit = 'pos.order'
#
#     @api.model
#     def get_department(self, option):
#         """ Function to get the order details of company wise"""
#
#         company_id = self.env.company.id
#         if option == 'pos_hourly_sales':
#
#             user_tz = self.env.user.tz if self.env.user.tz else pytz.UTC
#             query = '''select  EXTRACT(hour FROM date_order at time zone 'utc' at time zone '{}')
#                        as date_month,sum(amount_total) from pos_order where
#                        EXTRACT(month FROM date_order::date) = EXTRACT(month FROM CURRENT_DATE)
#                        AND pos_order.company_id = ''' + str(
#                 company_id) + ''' group by date_month '''
#             query = query.format(user_tz)
#             label = 'HOURS'
#         elif option == 'pos_monthly_sales':
#             query = '''select  date_order::date as date_month,sum(amount_total) from pos_order where
#              EXTRACT(month FROM date_order::date) = EXTRACT(month FROM CURRENT_DATE) AND pos_order.company_id = ''' + str(
#                 company_id) + '''  group by date_month '''
#             label = 'DAYS'
#         else:
#             query = '''select TO_CHAR(date_order,'MON')date_month,sum(amount_total) from pos_order where
#              EXTRACT(year FROM date_order::date) = EXTRACT(year FROM CURRENT_DATE) AND pos_order.company_id = ''' + str(
#                 company_id) + ''' group by date_month'''
#             label = 'MONTHS'
#         self._cr.execute(query)
#         docs = self._cr.dictfetchall()
#         order = []
#         for record in docs:
#             order.append(record.get('sum'))
#         today = []
#         for record in docs:
#             today.append(record.get('date_month'))
#         final = [order, today, label]
#         return final
#
#     @api.model
#     def get_details(self):
#         """ Function to get the payment details"""
#         company_id = self.env.company.id
#         cr = self._cr
#         cr.execute(
#             """select pos_payment_method.name ->>'en_US',sum(amount) from pos_payment inner join pos_payment_method on
#             pos_payment_method.id=pos_payment.payment_method_id group by pos_payment_method.name ORDER
#             BY sum(amount) DESC; """)
#         payment_details = cr.fetchall()
#         cr.execute(
#             '''select hr_employee.name,sum(pos_order.amount_paid) as total,count(pos_order.amount_paid) as orders
#             from pos_order inner join hr_employee on pos_order.user_id = hr_employee.user_id
#             where pos_order.company_id =''' + str(
#                 company_id) + " " + '''GROUP BY hr_employee.name order by total DESC;''')
#         salesperson = cr.fetchall()
#         total_sales = []
#         for rec in salesperson:
#             rec = list(rec)
#             sym_id = rec[1]
#             company = self.env.company
#             if company.currency_id.position == 'after':
#                 rec[1] = "%s %s" % (sym_id, company.currency_id.symbol)
#             else:
#                 rec[1] = "%s %s" % (company.currency_id.symbol, sym_id)
#             rec = tuple(rec)
#             total_sales.append(rec)
#         cr.execute(
#             '''select DISTINCT(product_template.name) as product_name,sum(qty) as total_quantity from
#        pos_order_line inner join product_product on product_product.id=pos_order_line.product_id inner join
#        product_template on product_product.product_tmpl_id = product_template.id  where pos_order_line.company_id =''' + str(
#                 company_id) + ''' group by product_template.id ORDER
#        BY total_quantity DESC Limit 10 ''')
#         selling_product = cr.fetchall()
#         sessions = self.env['pos.config'].search([])
#         sessions_list = []
#         dict = {
#             'opened': 'Opened',
#             'opening_control': "Opening Control"
#         }
#         for session in sessions:
#             st = dict.get(session.pos_session_state)
#             if st == None:
#                 sessions_list.append({
#                     'session': session.name,
#                     'status': 'Closed'
#                 })
#             else:
#                 sessions_list.append({
#                     'session': session.name,
#                     'status': dict.get(session.pos_session_state)
#                 })
#         payments = []
#         for rec in payment_details:
#             rec = list(rec)
#             sym_id = rec[1]
#             company = self.env.company
#             if company.currency_id.position == 'after':
#                 rec[1] = "%s %s" % (sym_id, company.currency_id.symbol)
#             else:
#                 rec[1] = "%s %s" % (company.currency_id.symbol, sym_id)
#             rec = tuple(rec)
#             payments.append(rec)
#         return {
#             'payment_details': payments,
#             'salesperson': total_sales,
#             'selling_product': sessions_list,
#         }
#
#     @api.model
#     def get_refund_details(self):
#         """ Function to get the Refund details"""
#         default_date = datetime.today().date()
#         pos_order = self.env['pos.order'].search([])
#         total = 0
#         today_refund_total = 0
#         total_order_count = 0
#         total_refund_count = 0
#         today_sale = 0
#         a = 0
#         for rec in pos_order:
#             if rec.amount_total < 0.0 and rec.date_order.date() == default_date:
#                 today_refund_total = today_refund_total + 1
#             total_sales = rec.amount_total
#             total = total + total_sales
#             total_order_count = total_order_count + 1
#             if rec.date_order.date() == default_date:
#                 today_sale = today_sale + 1
#             if rec.amount_total < 0.0:
#                 total_refund_count = total_refund_count + 1
#         magnitude = 0
#         while abs(total) >= 1000:
#             magnitude += 1
#             total /= 1000.0
#         # add more suffixes if you need them
#         val = '%.2f%s' % (total, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
#         pos_session = self.env['pos.session'].search([])
#         total_session = 0
#         for record in pos_session:
#             total_session = total_session + 1
#         return {
#             'total_sale': val,
#             'total_order_count': total_order_count,
#             'total_refund_count': total_refund_count,
#             'total_session': total_session,
#             'today_refund_total': today_refund_total,
#             'today_sale': today_sale,
#         }
#
#     @api.model
#     def get_the_top_customer(self, ):
#         """ To get the top Customer details"""
#         company_id = self.env.company.id
#         query = '''select res_partner.name as customer,pos_order.partner_id,sum(pos_order.amount_paid) as amount_total from pos_order
#         inner join res_partner on res_partner.id = pos_order.partner_id where pos_order.company_id = ''' + str(
#             company_id) + ''' GROUP BY pos_order.partner_id,
#         res_partner.name  ORDER BY amount_total  DESC LIMIT 10;'''
#         self._cr.execute(query)
#         docs = self._cr.dictfetchall()
#
#         order = []
#         for record in docs:
#             order.append(record.get('amount_total'))
#         day = []
#         for record in docs:
#             day.append(record.get('customer'))
#         final = [order, day]
#         return final
#
#     @api.model
#     def get_the_top_products(self):
#         """ Function to get the top products"""
#         company_id = self.env.company.id
#         query = '''select DISTINCT(product_template.name)->>'en_US' as product_name,sum(qty) as total_quantity from
#        pos_order_line inner join product_product on product_product.id=pos_order_line.product_id inner join
#        product_template on product_product.product_tmpl_id = product_template.id where pos_order_line.company_id = ''' + str(
#             company_id) + ''' group by product_template.id ORDER
#        BY total_quantity DESC Limit 10 '''
#         self._cr.execute(query)
#         top_product = self._cr.dictfetchall()
#         total_quantity = []
#         for record in top_product:
#             total_quantity.append(record.get('total_quantity'))
#         product_name = []
#         for record in top_product:
#             product_name.append(record.get('product_name'))
#         final = [total_quantity, product_name]
#         return final
#
#     @api.model
#     def get_the_top_categories(self):
#         """ Function to get the top Product categories"""
#         company_id = self.env.company.id
#         query = '''select DISTINCT(product_category.complete_name) as product_category,sum(qty) as total_quantity
#         from pos_order_line inner join product_product on product_product.id=pos_order_line.product_id  inner join
#         product_template on product_product.product_tmpl_id = product_template.id inner join product_category on
#         product_category.id =product_template.categ_id where pos_order_line.company_id = ''' + str(
#             company_id) + ''' group by product_category ORDER BY total_quantity DESC '''
#         self._cr.execute(query)
#         top_product = self._cr.dictfetchall()
#         total_quantity = []
#         for record in top_product:
#             total_quantity.append(record.get('total_quantity'))
#         product_categ = []
#         for record in top_product:
#             product_categ.append(record.get('product_category'))
#         final = [total_quantity, product_categ]
#         return final
