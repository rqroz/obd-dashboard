"""
Abstract models.
"""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.database import DATABASE
from app.models import DictDataModel
from app.models.odb.session import ODBSession
from app.models.user import User


class ODBSensorMixin(DictDataModel):
    """ Base absctract class for ODB Sensors """
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def session_id(cls):
        return Column(String, ForeignKey(ODBSession.id))

    @declared_attr
    def session(cls):
        return relationship(ODBSession, uselist=False)


class ODBSensorValueMixin(ODBSensorMixin):
    """ Base absctract class for ODB Sensors """
    value = Column(Numeric, nullable=False)
