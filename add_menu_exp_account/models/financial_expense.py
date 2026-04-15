# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from datetime import date




class FinancialExpense(models.Model):
    _name = 'financial.expense'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Financial Expense'
    _rec_name = 'seq'

    name = fields.Text(string="Ref", required=False, )
    expense_date = fields.Date(string="Expense Date", required=True, copy=False, tracking=True,
                               default=lambda self: date.today())
    expenses_ids = fields.One2many(comodel_name="financial.expense.line", inverse_name="invoice_id", string="Expenses",
                                   tracking=True)
    total = fields.Float(string="Total", tracking=True)
    tax = fields.Float(string="Taxes", compute="_get_tax", tracking=True, store=True)
    state = fields.Selection(selection=
    [
        ('draft', 'creator'),
        ('account1', 'Accounts 1'),
        ('chief_acc', 'Chief Acc'),
        ('cfo', 'CFO'),
        ('upload_bank', 'Upload Bank'),
        ('approve', 'Approve'),
        ('account2', 'Accounts 2'),

    ], required=False, default='draft', tracking=True)
    amount_taxed = fields.Float(string="Un Taxed Amount", tracking=True)
    seq = fields.Char(readonly=True, copy=False, default=lambda self: 'New')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)
    department_id = fields.Many2one(comodel_name='user.department', compute='_get_department', store=True)
    # ========================== Users =============================
    user_id = fields.Many2one(comodel_name='res.users', string='User', default=lambda self: self.env.user, copy=False)
    account1 = fields.Many2one(comodel_name='res.users', string='Accounts 1')
    chief_acc = fields.Many2one(comodel_name='res.users', string='Chief Acc')
    cfo = fields.Many2one(comodel_name='res.users', string='CFO')
    upload_bank = fields.Many2one(comodel_name='res.users', string='Upload Bank')
    approve = fields.Many2one(comodel_name='res.users', string='Approve')
    account2 = fields.Many2one(comodel_name='res.users', string='Accounts 2')

    def _fix_workflow_users(self):
        for rec in self:
            user = self.env.user
                    # Groups
            group_financial_creator = self.env.user.has_group('add_menu_exp_account.group_financial_creator')
            group_financial_account1 = self.env.user.has_group('add_menu_exp_account.group_financial_account1')
            group_financial_chief_acc = self.env.user.has_group('add_menu_exp_account.group_financial_chief_acc')
            group_financial_cfo = self.env.user.has_group('add_menu_exp_account.group_financial_cfo')
            group_financial_upload_bank = self.env.user.has_group('add_menu_exp_account.group_financial_upload_bank')
            group_financial_approve = self.env.user.has_group('add_menu_exp_account.group_financial_approve')
            group_financial_account2 = self.env.user.has_group('add_menu_exp_account.group_financial_account2')

            if group_financial_creator  and group_financial_account1 and group_financial_chief_acc and  group_financial_cfo and group_financial_upload_bank and group_financial_approve and group_financial_account2:
                rec.user_id = user.id
                rec.account1 = user.id
                rec.chief_acc = user.id
                rec.cfo = user.id
                rec.upload_bank = user.id
                rec.approve = user.id
                rec.account2 = user.id
            elif group_financial_creator and group_financial_account1 and group_financial_chief_acc and group_financial_cfo and group_financial_upload_bank and group_financial_approve and not group_financial_account2:
                rec.user_id = user.id
                rec.account1 = user.id
                rec.chief_acc = user.id
                rec.cfo = user.id
                rec.upload_bank = user.id
                rec.approve = user.id
                rec.account2 = rec.approve.financial_manager_id.id
            elif group_financial_creator and group_financial_account1 and group_financial_chief_acc and group_financial_cfo and group_financial_upload_bank and not group_financial_approve and not group_financial_account2:
                rec.user_id = user.id
                rec.account1 = user.id
                rec.chief_acc = user.id
                rec.cfo = user.id
                rec.upload_bank = user.id
                rec.approve = rec.upload_bank.financial_manager_id.id
                rec.account2 = rec.approve.financial_manager_id.id
            elif group_financial_creator and group_financial_account1 and group_financial_chief_acc and group_financial_cfo and not group_financial_upload_bank and not group_financial_approve and not group_financial_account2:
                rec.user_id = user.id
                rec.account1 = user.id
                rec.chief_acc = user.id
                rec.cfo = user.id
                rec.upload_bank = rec.cfo.financial_manager_id.id
                rec.approve = rec.upload_bank.financial_manager_id.id
                rec.account2 = rec.approve.financial_manager_id.id
            elif group_financial_creator and group_financial_account1 and group_financial_chief_acc and not group_financial_cfo and not group_financial_upload_bank and not group_financial_approve and not group_financial_account2:
                rec.user_id = user.id
                rec.account1 = user.id
                rec.chief_acc = user.id
                rec.cfo = rec.chief_acc.financial_manager_id.id
                rec.upload_bank = rec.cfo.financial_manager_id.id
                rec.approve = rec.upload_bank.financial_manager_id.id
                rec.account2 = rec.approve.financial_manager_id.id
            elif group_financial_creator and group_financial_account1 and not group_financial_chief_acc and not group_financial_cfo and not group_financial_upload_bank and not group_financial_approve and not group_financial_account2:
                rec.user_id = user.id
                rec.account1 = user.id
                rec.chief_acc = rec.account1.financial_manager_id.id
                rec.cfo = rec.chief_acc.financial_manager_id.id
                rec.upload_bank = rec.cfo.financial_manager_id.id
                rec.approve = rec.upload_bank.financial_manager_id.id
                rec.account2 = rec.approve.financial_manager_id.id
            elif group_financial_creator and not group_financial_account1 and not group_financial_chief_acc and not group_financial_cfo and not group_financial_upload_bank and not group_financial_approve and not group_financial_account2:
                rec.user_id = user.id
                rec.account1 = rec.user_id.financial_manager_id.id
                rec.chief_acc = rec.account1.financial_manager_id.id
                rec.cfo = rec.chief_acc.financial_manager_id.id
                rec.upload_bank = rec.cfo.financial_manager_id.id
                rec.approve = rec.upload_bank.financial_manager_id.id
                rec.account2 = rec.approve.financial_manager_id.id
            elif group_financial_creator and group_financial_account1 and not group_financial_chief_acc and not group_financial_cfo and not group_financial_upload_bank and not group_financial_approve and group_financial_account2:
                rec.user_id = user.id
                rec.account1 = user.id
                rec.chief_acc = rec.account1.financial_manager_id.id
                rec.cfo = rec.chief_acc.financial_manager_id.id
                rec.upload_bank = rec.cfo.financial_manager_id.id
                rec.approve = rec.upload_bank.financial_manager_id.id
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
            'account1': self.account1,
            'chief_acc': self.chief_acc,
            'cfo': self.cfo,
            'upload_bank': self.upload_bank,
            'approve': self.approve,
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


            elif rec.state == 'account1':
                if rec.account1 != user:
                    raise AccessError("Only Accounts 1 can edit")

            elif rec.state == 'chief_acc':
                if rec.chief_acc != user:
                    raise AccessError("Only Chief Accountant can edit")


            elif rec.state == 'cfo':
                if rec.cfo != user:
                    raise AccessError("Only CFO can edit")

            elif rec.state == 'upload_bank':
                if rec.upload_bank != user:
                    raise AccessError("Only Upload Bank can edit")

            elif rec.state == 'approve':
                if rec.approve != user:
                    raise AccessError("Only Approve can edit")

            elif rec.state == 'account2':
                if rec.account2 != user:
                    raise AccessError("Only Accounts 2 can edit")

        return super(FinancialExpense, self).write(vals)
    # =========================================
    #  إرسال الإيميل
    # =========================================

    def _send_stage_email(self):
        template = self.env.ref('add_menu_exp_account.email_template_financial_expense_stage')

        for rec in self:
            user = rec._get_user_by_state()

            if user and user.email:
                template.with_context(
                    tracking_disable=True,
                    mail_notrack=True,
                    mail_create_nosubscribe=True,
                    mail_notify_force_send=False,
                ).send_mail(
                    rec.id,
                    email_values={'email_to': user.email},
                    force_send=True,
                )
                # ✅ Optional: إضافة Activity
                # rec.activity_schedule(
                #     'mail.mail_activity_data_todo',
                #     user_id=user.id,
                #     summary="Expense Approval Required",
                # )

    # =========================================
    # Send Refuse mail
    # =========================================

    def _send_refuse_email(self):
        template = self.env.ref('add_menu_exp_account.financial_email_template_refuse')

        for rec in self:
            user = rec._get_user_by_state()

            if user and user.email:
                template.with_context(
                    tracking_disable=True,
                    mail_notrack=True,
                    mail_create_nosubscribe=True,
                    mail_notify_force_send=False,
                ).send_mail(
                    rec.id,
                    email_values={'email_to': user.email},
                    force_send=True,
                )
                # ✅ Optional: إضافة Activity
                # rec.activity_schedule(
                #     'mail.mail_activity_data_todo',
                #     user_id=user.id,
                #     summary="Expense Approval Required",
                # )

    def unlink(self):
        error_message = _('You cannot delete a expense which is in %s state')
        state_description_values = {elem[0]: elem[1] for elem in self._fields['state']._description_selection(self.env)}

        if self.env.user.has_group('base.group_user'):
            if any(hol.state not in ['draft'] for hol in self):
                raise UserError(error_message % state_description_values.get(self[:1].state))
        return super(FinancialExpense, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('seq', 'New') == 'New':
                vals['seq'] = self.env['ir.sequence'].next_by_code('financial.sequence') or 'New'
        record = super(FinancialExpense, self).create(vals_list)
        record._fix_workflow_users()
        return record

    # ========================================================================
    # Confirm
    # =======================================================================


    def to_account1(self):
        for rec in self:
            rec.state = 'account1'
            rec._send_stage_email()


    def to_chief_acc(self):
        for rec in self:
            rec.state = 'chief_acc'
            rec._send_stage_email()

    def to_cfo(self):
        for rec in self:
            rec.state = 'cfo'
            rec._send_stage_email()

    def to_upload_bank(self):
        for rec in self:
            rec.state = 'upload_bank'
            rec._send_stage_email()

    def to_approve(self):
        for rec in self:
            rec.state = 'approve'
            rec._send_stage_email()

    def to_account2(self):
        for rec in self:
            rec.state = 'account2'
            rec._send_stage_email()

    # ========================================================================
    # Refuse
    # =======================================================================
    def refuse_account1(self):
        for rec in self:
            if rec.state == 'account1':
                rec.state = 'draft'
                rec._send_refuse_email()


    def refuse_chief_acc(self):
        for rec in self:
            if rec.state == 'chief_acc':
                rec.state = 'account1'
                rec._send_refuse_email()

    def refuse_cfo(self):
        for rec in self:
            if rec.state == 'cfo':
                rec.state = 'chief_acc'
                rec._send_refuse_email()

    def refuse_upload_bank(self):
        for rec in self:
            if rec.state == 'upload_bank':
                rec.state = 'cfo'
                rec._send_refuse_email()

    def refuse_approve(self):
        for rec in self:
            if rec.state == 'approve':
                rec.state = 'upload_bank'
                rec._send_refuse_email()

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


class FinancialExpenseLine(models.Model):
    _name = 'financial.expense.line'
    _description = 'Financial Expense Line'

    invoice_id = fields.Many2one(comodel_name="financial.expense", )
    company_id = fields.Many2one(related='invoice_id.company_id', store=True)
    product_ids = fields.Many2one(comodel_name="product.product", string="Product",
                                  domain=[('is_expense', '=', True)])
    name = fields.Char(string="Label", )
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
        res = super(FinancialExpenseLine, self).write(vals)
        self._link_attachments()
        return res

    def _link_attachments(self):
        for rec in self:
            for att in rec.attachment_ids:
                if not att.res_id:
                    att.write({
                        'res_model': 'financial.expense.line',
                        'res_id': rec.id,
                    })


