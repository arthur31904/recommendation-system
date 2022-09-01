# coding=utf8
from __future__ import unicode_literals

import formencode
import uuid
from formencode import validators, ForEach

class SourceForm(formencode.Schema):
    """
    """
    allow_extra_fields = True
    filter_extra_fields = True
    ignore_key_missing = True




class RecommendationForm(SourceForm):
    """使用者建立格式"""
    tag_id_list = validators.Wrapper(convert_to_python=lambda a: uuid.UUID(a) if a else '')



class ArticleEditForm(formencode.Schema):
    """AccountEdit 檢查"""
    allow_extra_fields = True
    ignore_key_missing = True

    article_id = validators.String(not_empty=True, strip=True)


class ArticleSearchForm(formencode.Schema):
    """AccountSearch 檢查"""
    allow_extra_fields = True
    filter_extra_fields = True
    ignore_key_missing = True


    page = validators.Int(not_empty=True, min=1)  # 第幾頁
    limit = validators.Int(not_empty=True, min=1)  # 一頁幾筆

