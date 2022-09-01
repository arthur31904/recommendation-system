# coding=utf-8
from __future__ import unicode_literals
import inspect
import logging
import traceback
from sqlalchemy import asc, desc, exc
from .meta_module import now_func
from sqlalchemy.orm import Session
from fastapi import status
NOT_SET = object()
EMPTY_DIC = {}
EMPTY_LIST = []
import sys
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.logger import Logger, LogLevel
from core.exceptions import FatalError, HTTPException

class BaseService(object):
    """BaseService for CRUD"""
    TABLE = None

    def __init__(self, session, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.session = session
        assert self.TABLE is not None, 'Table is not set'

        """
        功能：增加 服務監測功能 阻擋 error 事件發生
        說明：抓取class的全部method,如果名稱開頭為 _ ,自動忽略,反之更新method掛載新功能
        """
        for method_name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method_name[:1] != '_':
                new_method = self.service_monitor(method)
                setattr(self, method_name, new_method)

    def service_monitor(self, method):
        def authorize_and_call(*args, **kw):
            try:
                result_data = method(*args, **kw)  # Call method
                return result_data
            except exc.SQLAlchemyError as err:
                Logger.log(LogLevel.ERROR, "db_error", "", err.code, traceback.format_exc())
                raise err

            except Exception as err:
                Logger.log(LogLevel.ERROR, "server_error", "", err.args, traceback.format_exc())
                # raise any unexpected error as HTTPException thus error handler can catch
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(err.args)
                )
            # finally:
                # self.session.close()
        return authorize_and_call

    def _relationship_obj_ud(self, obj, inpute_date):
        from copy import copy
        outpute = copy(inpute_date)
        for k in inpute_date.keys():
            if "add_" in k and inpute_date[k] is not NOT_SET:
                tag_attribute_key = obj.__likeattribute__(k[4:])
                if not tag_attribute_key: continue
                tag_attribute_value = getattr(obj, tag_attribute_key)
                if isinstance(inpute_date[k], list):
                    # new_tag_attribute_value = list(set(tag_attribute_value.extend(date[k])))
                    tag_attribute_value = list(set(tag_attribute_value) | set(inpute_date[k]))
                    setattr(obj, tag_attribute_key, tag_attribute_value)
                else:
                    tag_attribute_value.append(inpute_date[k])

                del outpute[k]

            if "del_" in k and inpute_date[k] is not NOT_SET:
                tag_attribute_key = obj.__likeattribute__(k[4:])
                if not tag_attribute_key: continue
                tag_attribute_value = getattr(obj, tag_attribute_key)
                if isinstance(inpute_date[k], list):
                    tag_attribute_value = list(set(tag_attribute_value) - set(inpute_date[k]))
                    setattr(obj, tag_attribute_key, tag_attribute_value)
                else:
                    tag_attribute_value.remove(inpute_date[k])

                del outpute[k]
        return obj, outpute

    def _get_by(self,db, **search_condition):

        session = db

        return session.query(self.TABLE) \
            .filter_by(**search_condition).first() \
            if search_condition else None

    def _get_list(self, query, order_by=EMPTY_DIC, group_by=EMPTY_LIST,
                  offset=None, limit=None, show_count=False,
                  **search_condition):
        """
        :param order_by: [(column_name, 1 or -1), (column_name, 1 or -1), ..],
                         ps. 1: 小->大, -1: 大->小
        :param group_by: [column_name, column_name, ..]
        """
        query = query.filter_by(**search_condition)
        count = query.count()
        table = self.TABLE
        if order_by:
            order_list = []
            for order in order_by:
                column_name = order[0]
                order = asc if order[1] == 1 else desc
                if hasattr(table, column_name):
                    order_list.append(order(getattr(table, column_name)))
            query = query.order_by(*order_list)
        if group_by:
            group_list = []
            for column_name in group_by:
                if hasattr(table, column_name):
                    group_list.append(getattr(table, column_name))
            query = query.group_by(*group_list)


        if offset is not None and int(offset) >= 0 and limit:
            # py2 and py3 compatible
            query = query.offset(offset).limit(limit)
        return (query.all(), count) if show_count else query.all()

    def _create(self,db, **data):
        obj = self.TABLE(**data)
        session = db
        session.add(obj)
        session.commit()
        session.refresh(obj)
        self.logger.info('[{0}][Create]:{1}'.format(self.TABLE.__name__, obj))
        return obj

    def _update(self,db, old_obj, **data):
        for column_name in data:
            if hasattr(old_obj, column_name):
                setattr(old_obj, column_name, data[column_name])
        old_obj.updated = now_func()
        session = db
        session.commit()
        session.refresh(old_obj)
        # self.session.flush()
        self.logger.info('[{0}][Update]:{1}'.format(self.TABLE.__name__, old_obj))
        return old_obj

    def _updates(self,db, conditions, **data):
        # data['updated'] = now_func()
        session = db
        # query = self.session.query(self.TABLE)
        query = session.query(self.TABLE)
        # query.update().where(**conditions).values(**data)
        query.filter_by(**conditions).update(data, synchronize_session='evaluate')
        # self.session.flush()
        session.commit()
        session.refresh()

        log_str = '<objects({0})>'.format(
            '&'.join(['{0}=={1}'.format(key, value) for key, value in conditions.items()]))
        self.logger.info('[{0}][UpdateS]:{1}'.format(self.TABLE.__name__, log_str))

    def _delete(self,db, old_obj):
        session = self.session
        session.delete(old_obj)
        session.commit()
        session.refresh()

        self.logger.warning('[{0}][Delete]:{1}'.format(self.TABLE.__name__, old_obj))

    def _deletes(self,db, conditions):
        session = db
        # query = self.session.query(self.TABLE)
        query = session.query(self.TABLE)
        query.filter_by(**conditions).delete()
        # self.session.flush()
        session.commit()
        session.refresh()

        log_str = '<objects({0})>'.format(
            '&'.join(['{0}=={1}'.format(key, value) for key, value in conditions.items()]))
        self.logger.warning('[{0}][DeleteS]:{1}'.format(self.TABLE.__name__, log_str))

    def _type_to_uuid(self, value):
        import uuid
        new_value = None
        if not str(value).isdigit():
            new_value = value if isinstance(value, uuid.UUID) else uuid.UUID(value)
        if not new_value:
            raise Exception("{0}'s column input value {1} is error".format(self.TABLE, value))

        return new_value