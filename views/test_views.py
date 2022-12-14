# coding=utf8
from __future__ import unicode_literals

import json
import transaction
import uuid
from . import article_form as form
import datetime
from ...base.base_view import BaseView
from ...lib.my_exception import MyException
from ..account.account_service import AccountService
from .article_service import ArticleService
from ..category.category_service import CategoryService


class ArticlePageView(BaseView):
    def __init__(self, request):
        super(ArticlePageView, self).__init__(request)
        self.article_service = ArticleService(self.session)
        self.category_service = CategoryService(self.session)
        self.account_service = AccountService(self.session)



    def article_list(self):
        _ = self.localizer

        category_list = self.category_service.get_list(type='article')

        category_obj_list = [a.__json__() for a in category_list]


        return {'category_list': category_obj_list}

    def article_category_list(self):
        _ = self.localizer

        return {}

    def article_create(self):
        _ = self.localizer

        category_list = self.category_service.get_list(type='article')

        category_obj_list = [a.__json__() for a in category_list]

        today = datetime.date.today()

        return {'category_list': category_obj_list, 'today': today}

    def article_edit(self):
        _ = self.localizer

        article_obj = self.article_service.get_by_id(obj_id=self.request.matchdict['article_id'],
                                                       check=True)

        category_list = self.category_service.get_list(type='article')

        category_obj_list = [a.__json__() for a in category_list]

        today = datetime.date.today()

        article = article_obj.__json__(show_image=True)

        if article.get('create_by') != 'None':
            account = self.account_service.get_by_id(obj_id=uuid.UUID(article.get('create_by')))
            article['create_name'] = account.name
        else:
            article['create_name'] = ''


        return {'category_list': category_obj_list, 'today': today, 'article': article}

class ArticleJsonView(BaseView):
    def __init__(self, request):
        super(ArticleJsonView, self).__init__(request)
        self.article_service = ArticleService(self.session)
        self.account_service = AccountService(self.session)

    def create(self):
        """
        ????????????
        """
        _ = self.localizer

        # ??????????????????
        request_data = form.ArticleCreateForm().to_python(self.request_params)

        # ????????????????????????
        article_obj = self.article_service.get_by(title=request_data.get('title'))
        if article_obj:
            raise MyException(code=1402)

        with transaction.manager:
            article_obj = self.article_service.create(user_id= self.account_id, **request_data)

        return {'response': {'article': article_obj.__json__()},
                'message': _(u'??????????????????')}

    def search(self):
        """
        ????????????
        """

        # ??????????????????
        request_data = form.ArticleSearchForm().to_python(self.request_params)

        # ????????????
        current_page = request_data.get('page', 1)
        limit = request_data.get('limit', 10)
        request_data['offset'] = (current_page - 1) * limit
        request_data['limit'] = limit
        request_data['order_by'] = [('created', -1)]

        # ????????????
        article_list, total_count = self.article_service.get_list(show_count=True, **request_data)

        article_obj_list = [a.__json__(show_image=True) for a in article_list]

        for article in article_obj_list:
            if article.get('create_by')!='None':
                account = self.account_service.get_by_id(obj_id=uuid.UUID(str(article.get('create_by'))))
                article['create_name'] = account.name
            else:
                article['create_name'] = ''

        return {'response': {'article_list': article_obj_list,
                             'total_count': total_count,
                             'total_page': (int(total_count / limit) + 1 if total_count % limit else 0)
                             },
                'message': u'??????????????????'}

    def get(self):
        """
        ????????????
        """

        # ??? category_id ????????????
        article_obj = self.article_service.get_by_id(obj_id=self.request.matchdict['article_id'],
                                                       check=True)

        return {'response': {'article': article_obj.__json__()},
                'message': '??????????????????'}

    def edit(self):
        """
        ????????????
        """

        # ??????????????????
        request_data = form.ArticleEditForm().to_python(self.request_params)

        # ??? category_id ????????????
        article_obj = self.article_service.get_by_id(obj_id=self.request.matchdict['article_id'],
                                                       check=True)

        s_data = {
            'title':request_data.get('title')
        }

        article_list, total_count = self.article_service.get_list(show_count=True, **s_data)

        if total_count > 0 and article_obj.title!=request_data.get('title'):
            raise MyException(code=1402)

        # ????????????
        with transaction.manager:
            article_obj = self.article_service.update(old_obj=article_obj,
                                                        user_id=self.account_id,
                                                        **request_data)

        return {'response': {'article': article_obj.__json__()},
                'message': u'??????????????????'}

    def delete(self):
        """
        ????????????
        """

        # ??? category_id ????????????
        article_obj = self.article_service.get_by_id(obj_id=self.request.matchdict['article_id'],
                                                       check=True)
        # ?????? status ???????????????
        with transaction.manager:
            self.article_service.delete(article_obj=article_obj)

        return {'message': u'??????????????????'}
