# coding=utf8
from __future__ import unicode_literals
import hashlib
from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType
from .meta_module import (Base, TimestampTable, uuid4)

def crypto_key(column_name):
    secret_key = str.encode("commerce" + column_name)
    hash_key = hashlib.sha256()
    hash_key.update(secret_key)
    return hash_key.hexdigest()
