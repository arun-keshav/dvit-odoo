# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    product_manager = fields.Many2one('res.users', string='Product Manager')


class ProjectTask(models.Model):
    _inherit = 'project.task'
    reviewer_id = fields.Many2one('res.users', string='Reviewer')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.project_project_id:
                for line in order.order_line:
                    if line.product_id.product_tmpl_id.product_manager:
                        line_tasks = self.env['project.task'].search([('sale_line_id','=',line.id)])
                        for task in line_tasks:
                            task.reviewer_id = line.product_id.product_tmpl_id.product_manager
                            task.user_id = line.product_id.product_tmpl_id.product_manager
        return res