# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request



class LovebelliesSurvey(http.Controller):


    @http.route('/categories', type="json", methods=['GET', 'POST'], auth='none')
    def get_categories(self, **post):
        category_dict = {}
        res = []
        categories = request.env['product.category'].sudo().search([])
        answered_categs = self.get_answered_category_count()
        for category in categories:
            image = category.categ_image
            res.append({
                'id' : category.id,
                'subCategoriesCount' : self.get_count(category),
                'name': category.name,
                'answered': True if category.id in answered_categs else False
            })
        category_dict.update({
            'categories' : res,
            'totalCategories': request.env['product.category'].sudo().search_count([]),
            'answeredCategories': len(self.get_answered_category_count())
        })
        return category_dict

    def get_answered_category_count(self):
        category_lst = []
        categories = request.env['product.category'].sudo().search([])
        for category in categories:
            total_pdt = request.env['product.template'].sudo().search_count([('categ_id', '=', category.id)])
            answered = request.env['user.suggestions'].sudo().search_count([('categ_id', '=', category.id)])
            if total_pdt == answered and total_pdt != 0:
                category_lst.append(category.id)
        return category_lst

    def get_count(self, category):
        read_group_res = request.env['product.template'].sudo().read_group([('categ_id', 'child_of', category.ids)], ['categ_id'],
                                                                 ['categ_id'])
        group_data = dict((data['categ_id'][0], data['categ_id_count']) for data in read_group_res)
        product_count = 0
        for sub_categ_id in request.env['product.category'].sudo().search([('id', 'child_of', category.id)]).ids:
            product_count += group_data.get(sub_categ_id, 0)
            return product_count


    @http.route('/products', type="json", methods=['GET', 'POST'], auth='none')
    def get_products(self, **post):
        categoryDetail = {}
        res = []
        data = request.jsonrequest
        categ_id = int(request.httprequest.referrer.split("/")[4])
        category = request.env['product.category'].sudo().search([('id', '=', categ_id)])
        products = request.env['product.product'].sudo().search([('categ_id', '=', categ_id)])
        for product in products:
            test = 'data:image/jpeg;base64,' + str(product.image).split("b'")[1][:-1] if product.image else " "
            suggestion_obj = request.env['user.suggestions'].sudo().search([('product_id', '=', product.id),('user_id', '=', 1)])
            res.append(dict(id=product.id,
                            img='data:image/jpeg;base64,' + str(product.image).split("b'")[1][:-1] if product.image else " ",
                            name=product.name,
                            suggestions= suggestion_obj.suggestion_ids.ids
            ))
        categoryDetail.update({
            'img': 'data:image/jpeg;base64,' + str(category.categ_image).split("b'")[1][:-1] if category.categ_image else " ",
            'description': category.description,
            'totalSubItems': request.env['product.product'].sudo().search_count([('categ_id', '=', categ_id)]),
            'categoryName': category.name,
            'subCategories': res
        })
        return categoryDetail


    @http.route('/suggestions', type="json", methods=['GET', 'POST'], auth='none')
    def suggestions(self, **post):
        print("sjbkldjsb")
        data = request.jsonrequest
        suggestions = request.env['user.suggestions'].sudo().search([('user_id', '=', 1),('product_id', '=', data.get('subcategoryId'))])
        product_obj= request.env['product.product'].sudo().search([('id', '=', data.get('subcategoryId'))])
        if not suggestions:
            suggestion_obj = request.env['user.suggestions'].sudo().create({
                'user_id': 1,
                'product_id': data.get('subcategoryId'),
                'suggestion_ids' : [(6, 0, [data.get('id')])],
                'categ_id':  product_obj.categ_id.id
            })
        else:
            suggestion_ids = suggestions.suggestion_ids.ids
            if data.get('isSelected'):
                suggestion_ids.append(data.get('id'))
            else:
                suggestion_ids.remove(data.get('id'))
            suggestions.suggestion_ids = [(6, 0, suggestion_ids)]
        self.unlink_other()
        return True


    def unlink_other(self):
        suggestions = request.env['user.suggestions'].sudo().search([])
        for suggestion in suggestions:
            if len(suggestion.suggestion_ids.ids) == 0:
                suggestion.unlink()
        return True










        


