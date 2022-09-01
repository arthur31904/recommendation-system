# coding=utf-8
from __future__ import unicode_literals

import uuid
from datetime import datetime

# from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy import Column, DateTime, Integer, Unicode, engine_from_config
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy.types import LargeBinary, TypeDecorator

_now_func = [func.utc_timestamp]


def uuid4():
    return uuid.uuid4()


def set_now_func(func):
    """Replace now function and return the old function."""
    old = _now_func[0]
    _now_func[0] = func
    return old


def get_now_func():
    """Return current now func."""
    return _now_func[0]


def now_func():
    """Return current datetime."""
    func = get_now_func()
    return func()


def setup_database_setting(**settings):
    """Setup database session."""
    if 'engine' not in settings:
        # pool = {"pool_size": 20, "max_overflow": 0}
        from sqlalchemy.pool import NullPool
        settings['engine'] = (engine_from_config(settings)) #, poolclass=NullPool

    if 'session' not in settings:
        settings['session'] = scoped_session(
            sessionmaker(
                # extension=ZopeTransactionExtension(keep_session=True),
                bind=settings['engine']
            )
        )

    set_now_func(datetime.utcnow)
    return settings


class TimestampTable(object):
    created = Column(DateTime, nullable=False, default=now_func)
    updated = Column(DateTime, nullable=False, default=now_func)
    update_user_id = Column(Integer, nullable=True, doc=u'最後一次修改者')
    create_user_id = Column(Integer, nullable=True, doc=u'創建者')


class DefaultTable(object):
    created = Column(DateTime, nullable=False, default=now_func)
    updated = Column(DateTime, nullable=False, default=now_func)
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(32), unique=True, index=True, nullable=False)

    def __unicode__(self):
        return self.name or self.id


class DefaultTableWithDisplayName(DefaultTable):
    display_name = Column(Unicode(255))

    def __unicode__(self):
        return self.display_name or self.name or self.id


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Use UUID in Postgresql, LargeBinary for others.
    Receive and return Python uuid() object.
    """
    impl = LargeBinary

    @staticmethod
    def load_dialect_impl(dialect):
        # `as_uuid` default to be False.
        # If set to False, the column takes `hex`.
        # If set to True, the column takes uuid.UUID object.
        type_ = UUID(as_uuid=True)\
            if dialect.name == 'postgresql' else LargeBinary(16)
        return dialect.type_descriptor(type_)

    @staticmethod
    def process_bind_param(value, dialect):
        if value:
            if isinstance(value, uuid.UUID):
                return value if dialect.name == 'postgresql' else value.bytes
            else:
                raise ValueError('value {} is not a valid uuid.UUID'
                                 .format(value))
        else:
            return None

    @staticmethod
    def process_result_value(value, dialect):
        if dialect.name == 'postgresql':
            return value if value else None
        else:
            return uuid.UUID(bytes=value) if value else None

    @staticmethod
    def is_mutable():
        return False
