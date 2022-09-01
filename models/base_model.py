# coding=utf8
from __future__ import unicode_literals

from sqlalchemy import (
    Column,
    Integer,
    String,
    ARRAY,
    ForeignKey,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from ..base.meta_module import (Base, TimestampTable, GUID, uuid4)

class Article(Base, TimestampTable):
    """
    文章資料表
    """
    __tablename__ = 't_article'
    article_id = Column('f_article_id', Integer, primary_key=True, autoincrement=True
                        , doc=u"文章流水編號")

    title = Column('f_title', String(100), nullable=False, unique=True, doc=u"文章名稱")

    author = Column('f_author', String(100), nullable=False, doc=u"作者名稱")

    intro = Column('f_intro', String(256), doc=u"文章簡介")

    content = Column('f_content', String, doc=u"文章內容")

    _type = Column('f_type', Integer, nullable=False, default=10,
                   info={"news": 10, "product_light": 11, "product_green": 12, "program": 13, "other": 14},
                   doc=u"分類類別:(10.最新消息,11.產品資訊(燈具),12.產品資訊(綠建築),12.工程實績,13.其他")

    position = Column('f_position', Integer, nullable=False, default=1, doc=u"網站排序(不得為空)")

    image_id = Column(ForeignKey('t_images.f_image_id'), nullable=True, doc=u"圖片")

    category_id = Column(ForeignKey('t_category.f_category_id'), nullable=True, doc=u"分類")

    remark = Column('f_remark', String(512), doc=u'備註')

    _index_status = Column('f_index_status', Integer, nullable=False, default=11,
                           info={"show": 10, "hiden": 11, "delete": 12},
                           doc=u"首頁狀態:10.顯示,11.隱藏,12:封存")

    _status = Column('f_status', Integer, nullable=False, default=10,
                     info={"show": 10, "hiden": 11, "delete": 400},
                     doc=u"狀態:10.顯示,11.隱藏,12:封存")

    image = relationship("Images")

    category = relationship("Category")

    def __repr__(self):
        return '<CategoryObject (article_id={0})>'.format(self.article_id)

    @hybrid_property
    def index_status(self):
        if hasattr(self.__class__, '_index_status'):
            # 將數值改為對應內容自串
            info_dic = self.__class__._index_status.info
            for k in info_dic.keys():
                if info_dic[k] == self._index_status:
                    return k

    @index_status.setter
    def index_status(self, value):
        # 將對應內容自串改為數值
        if not str(value).isdigit():
            v = self.__class__._index_status.info.get(value)
            if not v:
                raise Exception('index_status column input value {} is error'.format(value))
            self._index_status = v
        else:
            raise Exception('index_status column input value_type {} is error')

    @index_status.expression
    def index_status(cls):
        return cls._index_status

    @hybrid_property
    def status(self):
        if hasattr(self.__class__, '_status'):
            # 將數值改為對應內容自串
            info_dic = self.__class__._status.info
            for k in info_dic.keys():
                if info_dic[k] == self._status:
                    return k

    @status.setter
    def status(self, value):
        # 將對應內容自串改為數值
        if not str(value).isdigit():
            v = self.__class__._status.info.get(value)
            if not v:
                raise Exception('status column input value {} is error'.format(value))
            self._status = v
        else:
            raise Exception('status column input value_type {} is error')

    @status.expression
    def status(cls):
        return cls._status

    @hybrid_property
    def type(self):
        if hasattr(self.__class__, '_type'):
            # 將數值改為對應內容自串
            info_dic = self.__class__._type.info
            for k in info_dic.keys():
                if info_dic[k] == self._type:
                    return k

    @type.setter
    def type(self, value):
        # 將對應內容自串改為數值
        if not str(value).isdigit():
            v = self.__class__._type.info.get(value)
            if not v:
                raise Exception('type column input value {} is error'.format(value))
            self._type = v
        else:
            raise Exception('type column input value_type {} is error')

    @type.expression
    def type(cls):
        return cls._type

    @classmethod
    def __getattributes__(cls):
        return [i[1:] if i[:1] == '_' else i for i in cls.__dict__.keys() if
                i[:1] != '_' or i == '_update_user_id' or i == '_create_user_id']

    @classmethod
    def __likeattribute__(cls, key_word):
        map_args = [i for i in cls.__dict__.keys() if key_word in i and i[:1] != '_']
        return map_args[0] if map_args else None

    def __json__(self, show_image=False):
        d = {
            'article_id': str(self.article_id),
            'category_id': str(self.category_id),
            'title': self.title,
            'author': self.author,
            'type': self.type,
            'updated': str(self.updated).split(' ')[0],
            'created': str(self.created).split(' ')[0],
            'create_by': str(self.create_by),
            'position': self.position,
            'image_id': str(self.image_id),
            'remark': self.remark,
            'status': self.status,
            'index_status': self.index_status,
            'intro': self.intro,
            'content': self.content,
        }

        d['category'] = self.category.__json__() if self.category else {}

        if show_image:
            d['image'] = self.image.__json__() if self.image else {}

        return d