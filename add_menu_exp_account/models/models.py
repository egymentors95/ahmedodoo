# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from datetime import date


# @api.depends('restrict_mode_hash_table', 'state')
# def _compute_show_reset_to_draft_button(self):
#     for move in self:
#         move.show_reset_to_draft_button = not move.restrict_mode_hash_table and move.state in ('posted', 'cancel')


class Expense(models.Model):
    _name = 'expense.expense'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'expense_expense'
    _rec_name = 'seq'

    name = fields.Text(string="Ref", required=False, )
    # journal_entry_id = fields.Many2one(comodel_name="account.move", string="Journal Entry", copy=False)
    expense_date = fields.Date(string="Expense Date", required=True, copy=False, tracking=True,
                               default=lambda self: date.today())
    # journal_id = fields.Many2one(comodel_name="account.journal", string="Journal", required=False, tracking=True,
    #                              domain="[('type', 'in', ['bank','cash'])]")
    expenses_ids = fields.One2many(comodel_name="expense.line", inverse_name="invoice_id", string="Expenses",
                                   tracking=True)
    total = fields.Float(string="Total", tracking=True)
    tax = fields.Float(string="Taxes", compute="_get_tax", tracking=True, store=True)
    state = fields.Selection(selection=
    [
        ('draft', 'creator'),
        ('direct_manager', 'Direct Manager'),
        ('account1', 'Accounts 1'),
        ('account_manager', 'Account Manager'),
        ('financial_manager', 'Financial Manager'),
        ('cash_management', 'Cash Management'),
        ('account2', 'Accounts 2'),

    ], required=False, default='draft', tracking=True)
    amount_taxed = fields.Float(string="Un Taxed Amount", tracking=True)
    seq = fields.Char(readonly=True, copy=False, )
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)
    department_id = fields.Many2one(comodel_name='user.department', compute='_get_department', store=True)
    # ========================== Users =============================
    user_id = fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.user, copy=False)
    direct_manager = fields.Many2one(comodel_name='res.users', string='Direct Manager')
    account1 = fields.Many2one(comodel_name='res.users', string='Accounts 1')
    account_manager = fields.Many2one(comodel_name='res.users', string='Account Manager')
    financial_manager = fields.Many2one(comodel_name='res.users', string='Financial Manager')
    cash_management = fields.Many2one(comodel_name='res.users', string='Cash Management')
    account2 = fields.Many2one(comodel_name='res.users', string='Accounts 2')

    def _fix_workflow_users(self):
        for rec in self:
            user = self.env.user
                    # Groups
            group_creator = self.env.user.has_group('add_menu_exp_account.group_creator')
            group_direct_manager = self.env.user.has_group('add_menu_exp_account.group_direct_manager')
            group_account1 = self.env.user.has_group('add_menu_exp_account.group_account1')
            group_account_manager = self.env.user.has_group('add_menu_exp_account.group_account_manager')
            group_financial_manager = self.env.user.has_group('add_menu_exp_account.group_financial_manager')
            group_cash_management = self.env.user.has_group('add_menu_exp_account.group_cash_management')
            group_account2 = self.env.user.has_group('add_menu_exp_account.group_account2')

            if group_creator and group_direct_manager and group_account1 and group_account_manager and group_financial_manager and group_cash_management and group_account2:
                rec.user_id = user.id
                rec.direct_manager = user.id
                rec.account1 = user.id
                rec.account_manager = user.id
                rec.financial_manager = user.id
                rec.cash_management = user.id
                rec.account2 = user.id
            elif group_creator and group_direct_manager and group_account1 and group_account_manager and group_financial_manager and group_cash_management and not group_account2:
                rec.user_id = user.id
                rec.direct_manager = user.id
                rec.account1 = user.id
                rec.account_manager = user.id
                rec.financial_manager = user.id
                rec.cash_management = user.id
                rec.account2 = rec.cash_management.manager_id.id
            elif group_creator and group_direct_manager and group_account1 and group_account_manager and group_financial_manager and not group_cash_management and not group_account2:
                rec.user_id = user.id
                rec.direct_manager = user.id
                rec.account1 = user.id
                rec.account_manager = user.id
                rec.financial_manager = user.id
                rec.cash_management = rec.financial_manager.manager_id.id
                rec.account2 = rec.cash_management.manager_id.id
            elif group_creator and group_direct_manager and group_account1 and group_account_manager and not group_financial_manager and not group_cash_management and not group_account2:
                rec.user_id = user.id
                rec.direct_manager = user.id
                rec.account1 = user.id
                rec.account_manager = user.id
                rec.financial_manager = rec.account_manager.manager_id.id
                rec.cash_management = rec.financial_manager.manager_id.id
                rec.account2 = rec.cash_management.manager_id.id
            elif group_creator and group_direct_manager and group_account1 and not group_account_manager and not group_financial_manager and not group_cash_management and not group_account2:
                rec.user_id = user.id
                rec.direct_manager = user.id
                rec.account1 = user.id
                rec.account_manager = rec.account1.manager_id.id
                rec.financial_manager = rec.account_manager.manager_id.id
                rec.cash_management = rec.financial_manager.manager_id.id
                rec.account2 = rec.cash_management.manager_id.id
            elif group_creator and group_direct_manager and not group_account1 and not group_account_manager and not group_financial_manager and not group_cash_management and not group_account2:
                rec.user_id = user.id
                rec.direct_manager = user.id
                rec.account1 = rec.direct_manager.manager_id.id
                rec.account_manager = rec.account1.manager_id.id
                rec.financial_manager = rec.account_manager.manager_id.id
                rec.cash_management = rec.financial_manager.manager_id.id
                rec.account2 = rec.cash_management.manager_id.id
            elif group_creator and not group_direct_manager and not group_account1 and not group_account_manager and not group_financial_manager and not group_cash_management and not group_account2:
                rec.user_id = user.id
                rec.direct_manager = rec.user_id.manager_id.id
                rec.account1 = rec.direct_manager.manager_id.id
                rec.account_manager = rec.account1.manager_id.id
                rec.financial_manager = rec.account_manager.manager_id.id
                rec.cash_management = rec.financial_manager.manager_id.id
                rec.account2 = rec.cash_management.manager_id.id
            elif group_creator and group_direct_manager and group_account1 and not group_account_manager and not group_financial_manager and not group_cash_management and group_account2:
                rec.user_id = user.id
                rec.direct_manager = user.id
                rec.account1 = user.id
                rec.account_manager = rec.account1.manager_id.id
                rec.financial_manager = rec.account_manager.manager_id.id
                rec.cash_management = rec.financial_manager.manager_id.id
                rec.account2 = user.id


    @api.depends('user_id')
    def _get_department(self):
        for rec in self:
            if rec.user_id and rec.user_id.department_id:
                rec.department_id = rec.user_id.department_id.id

    # =========================================
    # 🔥 تحديد اليوزر حسب المرحلة
    # =========================================

    def _get_user_by_state(self):
        self.ensure_one()
        return {
            'direct_manager': self.direct_manager,
            'account1': self.account1,
            'account_manager': self.account_manager,
            'financial_manager': self.financial_manager,
            'cash_management': self.cash_management,
            'account2': self.account2,
        }.get(self.state)

    def write(self, vals):
        user = self.env.user
        print('user', user)

        for rec in self:
            print('rec._user_id', rec.user_id.name)

            if rec.state == 'draft':
                if rec.user_id != user:
                    print('draft')
                    raise AccessError("Only creator can edit in Draft")

            elif rec.state == 'direct_manager':
                if rec.direct_manager != user:
                    raise AccessError("Only Direct Manager can edit")

            elif rec.state == 'account1':
                if rec.account1 != user:
                    raise AccessError("Only Accounts 1 can edit")

            elif rec.state == 'account_manager':
                if rec.account_manager != user:
                    raise AccessError("Only Account Manager can edit")

            elif rec.state == 'financial_manager':
                if rec.financial_manager != user:
                    raise AccessError("Only Financial Manager can edit")

            elif rec.state == 'cash_management':
                if rec.cash_management != user:
                    raise AccessError("Only Cash Management can edit")

            elif rec.state == 'account2':
                if rec.account2 != user:
                    raise AccessError("Only Accounts 2 can edit")

        return super().write(vals)
    # =========================================
    # 🔥 إرسال الإيميل
    # =========================================

    def _send_stage_email(self):
        template = self.env.ref('add_menu_exp_account.email_template_expense_stage')

        for rec in self:
            user = rec._get_user_by_state()

            if user and user.email:
                template.send_mail(
                    rec.id,
                    email_values={'email_to': user.email},
                    force_send=True
                )
                # ✅ Optional: إضافة Activity
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=user.id,
                    summary="Expense Approval Required",
                )

    # =========================================
    # Send Refuse mail
    # =========================================

    def _send_refuse_email(self):
        template = self.env.ref('add_menu_exp_account.email_template_refuse')

        for rec in self:
            user = rec._get_user_by_state()

            if user and user.email:
                template.send_mail(
                    rec.id,
                    email_values={'email_to': user.email},
                    force_send=True
                )
                # ✅ Optional: إضافة Activity
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=user.id,
                    summary="Expense Approval Required",
                )

    def unlink(self):
        error_message = _('You cannot delete a expense which is in %s state')
        state_description_values = {elem[0]: elem[1] for elem in self._fields['state']._description_selection(self.env)}

        if self.env.user.has_group('base.group_user'):
            if any(hol.state not in ['draft'] for hol in self):
                raise UserError(error_message % state_description_values.get(self[:1].state))
        return super(Expense, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('seq', _('New')) == _('New'):
                vals['seq'] = self.env['ir.sequence'].next_by_code(
                    'expense.sequence'
                ) or _('New')
        record = super(Expense, self).create(vals_list)
        record._fix_workflow_users()
        return record

    def to_direct_manager(self):
        for rec in self:
            rec.state = 'direct_manager'
            rec._send_stage_email()

    def to_account1(self):
        for rec in self:
            rec.state = 'account1'
            rec._send_stage_email()

    def to_account_manager(self):
        for rec in self:
            rec.state = 'account_manager'
            rec._send_stage_email()

    def to_financial_manager(self):
        for rec in self:
            rec.state = 'financial_manager'
            rec._send_stage_email()

    def to_cash_management(self):
        for rec in self:
            rec.state = 'cash_management'
            rec._send_stage_email()

    def to_account2(self):
        for rec in self:
            rec.state = 'account2'
            rec._send_stage_email()

    # Refuse
    def refuse_direct_manager(self):
        for rec in self:
            if rec.state == 'direct_manager':
                rec.state = 'draft'
                rec._send_refuse_email()

    def refuse_account1(self):
        for rec in self:
            if rec.state == 'account1':
                rec.state = 'direct_manager'
                rec._send_refuse_email()

    def refuse_account_manager(self):
        for rec in self:
            if rec.state == 'account_manager':
                rec.state = 'account1'
                rec._send_refuse_email()

    def refuse_financial_manager(self):
        for rec in self:
            if rec.state == 'financial_manager':
                rec.state = 'account_manager'
                rec._send_refuse_email()

    def refuse_cash_management(self):
        for rec in self:
            if rec.state == 'cash_management':
                rec.state = 'financial_manager'
                rec._send_refuse_email()

    # def refuse_account2(self):
    #     for rec in self:
    #         if rec.state == 'account2':
    #             rec.state = 'cash_management'
    #             rec._send_refuse_email()




    # def get_confirm(self):
    #     for rec in self:
    #         if not rec.journal_id:
    #             raise UserError(
    #                 _("You cannot Post Entry. Please fill Journal."))
    #
    #         for line in rec.expenses_ids:
    #             if not line.account_id:
    #                 raise UserError(
    #                     _("You cannot Post Entry because some expense lines have no Account. Please fill all Accounts."))
    #
    #         lines = []
    #         taxx = 0
    #         for line in rec.expenses_ids:
    #             for tax in line.tax_ids.invoice_repartition_line_ids:
    #                 if tax.account_id:
    #                     taxx = tax.account_id.id
    #             lines.append([0, 0, {
    #                 'account_id': line.account_id.id,
    #                 'name': f"{line.product_ids.name} - {line.name}",
    #                 'debit': line.price_subtotal,
    #
    #             }])
    #         if taxx:
    #             lines.append([0, 0, {
    #                 'account_id': taxx,
    #                 'name': f'Tax',
    #                 'debit': rec.tax,
    #
    #             }])
    #         lines.append([0, 0, {
    #             'account_id': rec.journal_id.default_account_id.id,
    #             'name': f"{line.product_ids.name} - {line.name}",
    #             'credit': rec.total,
    #
    #         }])
    #
    #         if rec.journal_entry_id.is_created == False:
    #             invoice = self.env['account.move'].sudo().create({
    #                 'is_created': True,
    #                 'move_type': 'entry',
    #                 'ref': rec.seq,
    #                 'date': rec.expense_date,
    #                 'journal_id': rec.journal_id.id,
    #                 'line_ids': lines,
    #             })
    #             rec.journal_entry_id = invoice.id
    #             invoice.action_post()
    #
    #         else:
    #             rec.journal_entry_id.date = rec.expense_date
    #             rec.journal_entry_id.journal_id = rec.journal_id
    #             rec.journal_entry_id.ref = rec.name
    #             rec.journal_entry_id.line_ids = False
    #             rec.journal_entry_id.line_ids = lines
    #             rec.journal_entry_id.action_post()
    #         rec.state = 'confirm'

    @api.depends(
        'expenses_ids.quantity',
        'expenses_ids.price_unit',
        'expenses_ids.tax_ids'
    )
    def _get_tax(self):
        for rec in self:
            amount_untaxed = 0.0
            amount_tax = 0.0

            for line in rec.expenses_ids:
                taxes_res = line.tax_ids.compute_all(
                    line.price_unit,
                    quantity=line.quantity,
                    currency=rec.company_id.currency_id,
                    product=line.product_ids,
                )

                # subtotal بدون ضريبة (حتى لو السعر شامل)
                line.price_subtotal = taxes_res['total_excluded']

                amount_untaxed += taxes_res['total_excluded']
                amount_tax += taxes_res['total_included'] - taxes_res['total_excluded']

            rec.amount_taxed = amount_untaxed
            rec.tax = amount_tax
            rec.total = amount_untaxed + amount_tax


class ExpenseLine(models.Model):
    _name = 'expense.line'
    _description = 'expense_line'

    invoice_id = fields.Many2one(comodel_name="expense.expense", )
    company_id = fields.Many2one(related='invoice_id.company_id', store=True)
    product_ids = fields.Many2one(comodel_name="product.product", string="Product",
                                  domain=[('is_expense', '=', True)])
    name = fields.Char(string="Label", )
    # account_id = fields.Many2one(comodel_name="account.account", string="Account", required=False,
    #                              readonly=False, )
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendors', domain=[('supplier_rank', '>', 0)])
    quantity = fields.Float(string="Quantity", required=False, default="1")
    price_unit = fields.Float(string="Price", required=True, )
    tax_ids = fields.Many2many(comodel_name="account.tax", string="Taxes", )
    price_subtotal = fields.Float(string="Subtotal", required=False, )
    vat_value = fields.Float(string='Vat Value', compute='_get_total_vat', store=True)
    attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments', )

    @api.depends('price_subtotal', 'tax_ids')
    def _get_total_vat(self):
        for rec in self:
            t = 0
            for any_line in rec.tax_ids:
                t = t + any_line.amount
            taxes = (t / 100) * rec.price_subtotal
            rec.vat_value = taxes

    @api.onchange('product_ids')
    def _onchange_product_ids(self):
        for rec in self:
            if rec.product_ids:
                # نسخ الضريبة من supplier_taxes_id الخاصة بالمنتج
                rec.tax_ids = rec.product_ids.supplier_taxes_id.filtered(
                    lambda t: t.company_id == rec.invoice_id.company_id
                )
            else:
                rec.tax_ids = False

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for rec in records:
            rec._link_attachments()

        return records

    def write(self, vals):
        res = super().write(vals)
        self._link_attachments()
        return res

    def _link_attachments(self):
        for rec in self:
            for att in rec.attachment_ids:
                if not att.res_id:
                    att.write({
                        'res_model': 'expense.line',
                        'res_id': rec.id,
                    })


class AccountMoveExpenses(models.Model):
    _inherit = 'account.move'

    is_expenses = fields.Boolean()
    is_created = fields.Boolean(string="", default=False)
