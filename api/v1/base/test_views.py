# coding=utf8
from __future__ import unicode_literals
from fastapi import APIRouter, Depends, Body, Response, status, BackgroundTasks
from api.v1.config import Responses

import traceback
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from database import SessionLocal, Engine
import json
import transaction
import uuid
# from . import article_form as form
from schemas import recommendation_schema
import datetime
from base.base_view import BaseView
from lib.my_exception import MyException
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from services.test_services import ArticleService
from from_set import recommendation_form as form

# from classy_fastapi import Routable, get, delete

from fastapi_utils.cbv import cbv

from fastapi_utils.inferring_router import InferringRouter
from core.router import APIRoute
## 引入回傳值定義
from schemas.response import SuccessResponse, ErrorResponse
from schemas.recommendation_schema import article_back,article_back_list

ArticleBackResponses = {
    200: {"model": article_back},
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}

ArticleBackListResponses = {
    200: {"model": article_back_list},
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}

# router = APIRouter()
router = InferringRouter(route_class=APIRoute)

def get_db(request: Request):
    return request.state.db

@cbv(router)
class ArticleJsonView():
    def __init__(self):
        super(ArticleJsonView, self).__init__()
        ArticleJsonView.INSTANCE = self
        db: Session = Depends(get_db)
        self.article_service = ArticleService(session=db)
    # user_id: UserID = Depends(get_jwt_user)
    # article_service = ArticleService(Depends(get_db))

    @router.post("/v1/aaaaa", responses=Responses)
    def create(self, article: article_schema.article_create, db: Session = Depends(get_db)):
        """
        創建分類
        """
        request_data = form.ArticleCreateForm().to_python(article.dict())

        with transaction.manager:
            article_obj = self.article_service.create(db=db,**request_data)

        return {'response': {'article': article_obj.__json__()},
                'message': u'分類創建成功'}

    @router.post("/v1/aaaaa/edit", responses=Responses)
    def edit(self, article: article_schema.article_edit, db: Session = Depends(get_db)):
        """
        創建分類
        """
        request_data = form.ArticleEditForm().to_python(article.dict())

        article_obj = self.article_service.get_by_id(db=db, obj_id=request_data.get('article_id'), check=True)

        with transaction.manager:
            article_obj = self.article_service.update(db=db, old_obj=article_obj,
                                                        **request_data)
            # article_obj = self.article_service.create(db=db,**request_data)

        return {'response': {'article': article_obj.__json__()},
                'message': u'分類創建成功'}

    @router.post("/v1/aaaaa/get", responses=Responses)
    def get(self, article: article_schema.article_edit, db: Session = Depends(get_db)):
        """
        創建分類
        """
        request_data = form.ArticleEditForm().to_python(article.dict())

        article_obj = self.article_service.get_by_id(db=db, obj_id=request_data.get('article_id'), check=True)

        # with transaction.manager:
        #     article_obj = self.article_service.update(db=db, old_obj=article_obj,
        #                                                 **request_data)
        #     # article_obj = self.article_service.create(db=db,**request_data)

        return {'response': {'article': article_obj.__json__()},
                'message': u'分類創建成功'}

    @router.post("/v1/aaaaa/get_list", responses=Responses)
    def get_list(self, article: article_schema.article_search, db: Session = Depends(get_db)):
        """
        創建分類
        """
        request_data = form.ArticleSearchForm().to_python(article.dict())

        limit = request_data.get('limit', 10)

        article_list, total_count = self.article_service.get_list(db=db, show_count=True, **request_data)

        article_obj_list = [a.__json__() for a in article_list]

        return {'response': {'order_obj_list': article_obj_list,
                      'total_count': total_count,
                      'total_page': (int(total_count / limit) + 1 if total_count % limit else 0)
                      },
                'message': u'搜尋成功'}