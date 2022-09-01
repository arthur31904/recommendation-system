# coding=utf-8
from __future__ import unicode_literals

import logging

from sqlalchemy import asc, desc

from ..models import now_func

NOT_SET = object()
EMPTY_DIC = {}
EMPTY_LIST = []

class BaseProvider(object):
    """Base Provider model for CRUD"""
    TABLE = None

    def __init__(self, session, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.session = session
        assert self.TABLE is not None, 'Table is not set'

    def _get_by(self, **search_condition):
        if search_condition:
            query = self.session.query(
                self.TABLE).filter_by(**search_condition)
            return query.first()
        else:
            return None

    def _get_list(self, query, order_by=None, group_by=None,
                  offset=None, limit=None, show_count=False,
                  **search_condition):
        query = query.filter_by(**search_condition)
        count = query.count()
        if order_by:
            order_list = []
            for o in order_by:
                column_name = o[0]
                order = asc if o[1] == 1 else desc
                if hasattr(self.TABLE, column_name):
                    order_list.append(order(getattr(self.TABLE, column_name)))
            query = query.order_by(*order_list)
        if group_by:
            group_list = []
            for column_name in group_by:
                if hasattr(self.TABLE, column_name):
                    group_list.append(getattr(self.TABLE, column_name))
            query = query.group_by(*group_list)
        if offset >= 0 and limit:
            query = query.offset(offset).limit(limit)
        if show_count:
            return query.all(), count
        return query.all()

    def _create(self, **data):
        obj = self.TABLE(**data)
        session = self.session
        session.add(obj)
        session.flush()
        self.logger.info('Create {0}'.format(obj))
        return obj

    def _update(self, old_obj, **data):
        for column_name in data:
            if hasattr(old_obj, column_name):
                setattr(old_obj, column_name, data[column_name])
        old_obj.updated = now_func()
        self.session.flush()
        self.logger.info('Update {0}'.format(old_obj))
        return old_obj

    def _remove(self, old_obj):
        session = self.session
        session.delete(old_obj)
        session.flush()
        self.logger.warn('Remove {0}'.format(old_obj))
