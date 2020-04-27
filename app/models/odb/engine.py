"""
Engine-related OBD Readings.
"""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from app.database import DATABASE
from app.models import DictDataModel
from app.models.odb import ODBSession
from app.models.user import User


class EngineLoad(DATABASE.Model, DictDataModel):
    """ Readings for GPS data from ODB sensors. """
    __tablename__ = "odb_engine_load"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey(ODBSession.id))
    value = Column(Numeric, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship(ODBSession, uselist=False)