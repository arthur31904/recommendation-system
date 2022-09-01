# coding=utf8
from __future__ import unicode_literals
from fastapi import APIRouter, Depends, Body, Response, status, BackgroundTasks
from api.v1.config import Responses
## 推薦系統相關function
from pyspark.ml.feature import Word2Vec, Word2VecModel
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
import faiss
sc = SparkContext('local')
spark = SparkSession(sc)

import traceback
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from database import SessionLocal, Engine

import transaction
import os, sys
import uuid

from schemas import recommendation_schema
from lib import http_requests

from fastapi import Depends, FastAPI, HTTPException, Request, Response

from from_set import recommendation_form as form


import json
from fastapi_utils.cbv import cbv

from fastapi_utils.inferring_router import InferringRouter
from core.router import APIRoute
## 引入回傳值定義
from schemas.response import SuccessResponse, ErrorResponse
from schemas.recommendation_schema import recommendation_back, recommendation_back_list

RecommendationBackResponses = {
    200: {"model": recommendation_back},
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}

RecommendationBackListResponses = {
    200: {"model": recommendation_back_list},
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}

# router = APIRouter()
router = InferringRouter(route_class=APIRoute)

def get_db(request: Request):
    return request.state.db

@cbv(router)
class RecommendationJsonView():
    def __init__(self):
        super(RecommendationJsonView, self).__init__()
        RecommendationJsonView.INSTANCE = self
        # db: Session = Depends(get_db)
        # self.article_service = ArticleService(session=db)
    # user_id: UserID = Depends(get_jwt_user)
    # article_service = ArticleService(Depends(get_db))

    @router.get("/v1/update/model", responses=Responses)
    def update_model(self):
        """
        更新模型
        這邊不能使用中文字
        應該使用tag_id
        """

        url = ""
        # headers = {'Content-type': 'application/json'}

        response = http_requests.get_and_log(url=url)

        obj_list = json.loads(response.content)

        obj_list = {
            1: ["1", "2", "3", "4"],
            2: ["3", "2", "1", "9"],
            3: ["10", "2", "1", "3"],
            4: ["11", "23", "1", "3"],
            5: ["23", "3", "33", "11"],
            6: ["11", "23", "2", "3"],
            7: ["1", "2", "4", "5"],
            8: ["2", "33", "44", "55"],
            9: ["33", "2", "11", "12"],
            10: ["11", "33", "2", "3"],
            11: ["3", "4", "5", "2"],
            12: ["7", "5", "2", "6"],
            13: ["3", "2", "6", "4"]
        }

        tuple_list = []

        for a in obj_list:
            v1_list = []
            v1_list.append(obj_list[a])
            tuple_list.append(tuple(v1_list))

        tuple_list = [
                (["紅茶", "統一", "飲料", "麥香"],)
                , (["奶茶", "統一", "飲料", "麥香"],)
                , (["咖啡", "統一", "飲料", "麥香"],)
                , (["牛排", "統一", "食物", "西式料理"],)
                , (["牛奶", "統一", "飲料", "新鮮"],)
                , (["ps5", "sony", "遊戲機", "電子產品"],)
                , (["遊戲機", "sony", "電子產品", "switch"],)
                , (["手機", "sony", "電子產品", "iphone13"],)
                , (["手機", "sunsong", "電子產品", "iphone13"],)
                , (["手機", "apple", "電子產品", "iphone13"],)
                , (["遊戲機", "任天堂", "電子產品", "switch"],)
                , (["手機", "宏碁", "電子產品"],)
                , (["手機", "電子產品", "iphone13"],)
                , (["imac", "電子產品", "apple"],)
                , (["蔥油餅", "統一", "食物"],)
                , (["炸雞", "統一", "食物"],)
                , (["雞腿", "統一", "食物"],)
                , (["啤酒", "台灣啤酒", "酒精飲料"],)
                , (["日式料理", "餐廳", "美食", "啤酒"],)
                , (["中式料理", "餐廳", "美食", "特色料理"],)
                , (["西式料理", "餐廳", "美食", "特色料理"],)
                , (["義式式料理", "餐廳", "美食", "在地料理"],)
                , (["威士忌", "台灣啤酒", "酒精飲料"],)
                , (["啤酒", "金牌啤酒", "酒精飲料"],)
                , (["啤酒", "海尼根", "酒精飲料"],)
                , (["高粱", "金門", "酒精飲料"],)
                , (["永豐餘", "衛生紙", "日用品"],)
                , (["五月花", "衛生紙", "日用品"],)
                , (["高露潔", "牙刷", "日用品"],)
                , (["高露潔", "牙膏", "日用品"],)
                , (["漢堡", "薯條", "麥當勞"],)
            ]
        df = spark.createDataFrame(
            tuple_list, ["text"]
        )

        import math
        vectorsize = math.ceil(len(tuple_list) * 0.96)
        word2Vec = Word2Vec(vectorSize=vectorsize, minCount=0, inputCol="text", outputCol="result")
        model = word2Vec.fit(df)
        import shutil
        pathTest = "./word2vec_model"
        shutil.rmtree(pathTest)
        model.save(pathTest)

        return {'response': {},
                'message': u'模型重建完成'}

    @router.post("/v1/get/embedding", responses=Responses)
    def get_embedding(self, tag_list: recommendation_schema.TagIdList):
        """
        更新模型
        """

        tag_id_list = tag_list.dict().get('tag_id_list')
        v1_list =[]
        v1_list.append(tag_id_list)
        tuple_list = []
        tuple_list.append(tuple(v1_list))
        df2 = spark.createDataFrame(
            tuple_list, ["text"]
        )

        model_2 = Word2VecModel.load("./word2vec_model")

        result = model_2.transform(df2)

        return_str = ",".join([str(_) for _ in list(result.collect()[0][1])])
        return {'response': {'return_str': return_str},
                'message': u'取得embedding'}

    @router.get("/v1/recommendation/item/{item_id}/{limit}", responses=Responses)
    def get_recommendation(self, item_id: str, limit: int):
        """
        創建分類
        """
        url = ""
        # headers = {'Content-type': 'application/json'}

        response = http_requests.get_and_log(url=url)
        import json
        obj_list = json.loads(response.content)

        obj_key_list = list(obj_list.keys())

        obj_list = {
            1: ["1", "2", "3", "4"],
            2: ["3", "2", "1", "9"],
            3: ["10", "2", "1", "3"],
            4: ["11", "23", "1", "3"],
            5: ["23", "3", "33", "11"],
            6: ["11", "23", "2", "3"],
            7: ["1", "2", "4", "5"],
            8: ["2", "33", "44", "55"],
            9: ["33", "2", "11", "12"],
            10: ["11", "33", "2", "3"],
            11: ["3", "4", "5", "2"],
            12: ["7", "5", "2", "6"],
            13: ["3", "2", "6", "4"]
        }

        tuple_list = []

        for a in obj_list:
            v1_list = []
            v1_list.append(obj_list[a])
            tuple_list.append(tuple(v1_list))

        df2 = spark.createDataFrame(
            tuple_list, ["text"]
        )

        model_2 = Word2VecModel.load("./word2vec_model")

        result = model_2.transform(df2)

        test_dict = {}
        name_dict = {}

        # for row in result.collect():
        #     text, vector = row
        #     obj_list[obj_key_list[i]] = str(vector)
            # test_dict[id] = str(vector)
            # name_dict[id] = str(" ".join(text))


        for i in range(len(result.collect())):
            text, vector = result.collect()[i]
            obj_list[obj_key_list[i]] = str(vector)

        import pandas as pd
        import numpy as np
        import json

        df = pd.DataFrame(list(obj_list.items()),
                          columns=['id', 'features'])

        ids = df['id'].values.astype(np.int64)

        datas = []
        for a in df['features']:
            datas.append(json.loads(a))

        datas_v2 = np.array(datas).astype(np.float32)

        dimenion = datas_v2.shape[1]

        index = faiss.IndexFlatL2(dimenion)
        index2 = faiss.IndexIDMap(index)

        index2.add_with_ids(datas_v2, ids)

        tager_id = item_id
        df2 = pd.DataFrame(list(obj_list.items()),
                           columns=['id', 'features'])
        emb = np.array(json.loads(df2[df2['id'] == tager_id]['features'].iloc[0]))
        emb = np.expand_dims(emb, axis=0).astype(np.float32)

        topk = limit+1
        faiss.normalize_L2(emb)
        D, I = index2.search(emb, topk)
        r_list = []
        for a in I[0]:

            if str(a) != tager_id:
                print(a)
                r_list.append(str(a))

        return {'response': {'taget_tag': item_id,
                             're_list': r_list},
                'message': u'回傳推薦列表'}


