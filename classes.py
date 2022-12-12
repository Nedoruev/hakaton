from typing import List
import sqlalchemy
import datetime
import sqlalchemy as sa
from variables import *


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),)


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = sa.Column(sa.BigInteger, primary_key=True)
    token = sa.Column(sa.String(200), primary_key=True)
    password = sa.Column(sa.String(200), primary_key=True)
    name = sa.Column(sa.String(200), primary_key=True)
    role = sa.Column(sa.String(200), primary_key=True)
    disc = sa.Column(sa.String(200), primary_key=True)
    query: sqlalchemy.select


class Lessons(TimedBaseModel):
    __tablename__ = 'lessons'
    less_name = sa.Column(sa.String(200), primary_key=True)
    info = sa.Column(sa.String(10000), primary_key=True)
    query: sqlalchemy.select