# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.category'

    categ_image = fields.Binary("Image")
    description = fields.Text("Desc")



class Suggestions(models.Model):
    _name = 'product.suggestions'

    name = fields.Char('Name')


class UserSuggestions(models.Model):
    _name = 'user.suggestions'

    user_id = fields.Many2one('res.users', 'User', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    categ_id = fields.Many2one('product.category', 'Category', required=True)
    suggestion_ids = fields.Many2many('product.suggestions', 'user_suggestions_pdt_default_rel', 'product_id', 'suggestion_id', string='Suggestions')


