# coding=utf-8
from __future__ import unicode_literals

import uuid
from models.test_model import Article
from lib.my_exception import MyException
from base.base_service import EMPTY_DIC, BaseService, now_func
from sqlalchemy.orm import Session
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple

class ArticleService(BaseService):
    TABLE = Article

    # def __init__(self, session: Session):
    #     # super(ArticleService, self).__init__(session, logger=logger)
    #     self.session = session

    def create(self, db:Session, **data)-> Article:
        """
        必填資料
            article: 文章
        其他資料
            **data: 其他資料
        """
        # 物件元素
        class_args = self.TABLE.__getattributes__()
        # 不可用參數
        un_available_args = ['article_id']
        # 可用參數
        available_args = [key for key in class_args if key not in un_available_args]
        # 資料過濾
        create_data = {key: data[key] for key in available_args if key in data}

        # create_data['article_id'] = uuid.uuid4()
        # 當有使用者id時

        # 資料創建
        try:
            return self._create(db=db,**create_data)
        except Exception as e:
            # raise MyException(code=1401, message=e)
            raise e

    def update(self,db:Session, old_obj:, **data)-> Article:
        # 物件元素
        class_args = self.TABLE.__getattributes__()
        # 不可用參數
        un_available_args = ['article_id']
        # 可用參數
        available_args = [key for key in class_args if key not in un_available_args]
        # 資料過濾
        update_data = {key: data[key] for key in available_args if key in data}
        # 當有使用者id時
        # if user_id:
        #     update_data['update_by'] = uuid.UUID(user_id)

        update_data['updated'] = now_func()

        # 資料更新
        try:
            return self._update(db=db,old_obj=old_obj, **update_data)
        except Exception as e:
            # raise MyException(code=1403, message=e)
            pass
    def get_by_id(self,db:Session, obj_id, check=False)-> Article:
        """
        讀取帳號編號
        :param obj_id:
        :param check:
        :return:
        """
        id = obj_id
        article = self._get_by(db=db,article_id=id)
        # if check and not article:
        #     raise MyException(code=1405)

        return article

    def get_by(self,db:Session, **data)-> Article:
        try:
            return self._get_by(db=db,**data)
        except Exception as e:
            raise MyException(code=1404, message=e)

    def get_list(self,db:Session, order_by=EMPTY_DIC, group_by=EMPTY_DIC,
                 offset=0, limit=None, show_count=False, title=None, category_id=None,
                 status=None, check_mechanism='filtering', **search_condition)-> Tuple[list[Article], int]:

        # 物件元素
        class_args = self.TABLE.__getattributes__()
        # 可不用參數
        un_available_args = []
        # 可用參數
        available_args = [key for key in class_args if key not in un_available_args]

        # 查詢條件製成
        session = db
        # query = self.session.query(self.TABLE)
        query = session.query(self.TABLE)

        if title is not None:
            like_str = '%{0}%'.format(title)
            query = query.filter(self.TABLE.title.ilike(like_str))

        if category_id is not None:
            query = query.filter(self.TABLE.category_id == category_id)

        if status is not None:
            status_value = self.TABLE._status.info.get(status, None)
            if status_value is None:
                raise MyException(code=901, message='{0}-{1}'.format(self.TABLE.__name__, 'Status'))
            query = query.filter(self.TABLE._status == status_value)
        else:
            query = query.filter(self.TABLE.status != 400)

        # 資料篩選器
        if check_mechanism == 'filtering':
            # 資料過濾機制
            search_condition = {key: search_condition[key] for key in available_args if key in search_condition}
        elif check_mechanism == 'defence':
            # 資料防護機制
            for key in search_condition:
                if key in un_available_args:
                    raise Exception('input query args is Disable in {0} '.format(self.TABLE.__name__))
                elif key not in available_args:
                    raise Exception('input query args is error in {0} '.format(self.TABLE.__name__))

        try:

            return self._get_list(query, order_by, group_by,
                                  offset, limit, show_count, **search_condition)

        except Exception as e:
            raise MyException(code=1404, message=e)

    def delete(self,db:Session, article_obj):

        self._delete(article_obj)

        return True
