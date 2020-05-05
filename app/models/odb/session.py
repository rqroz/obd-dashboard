"""
ODB Session.
"""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database import DATABASE
from app.models import DictDataModel
from app.models.user import User


class ODBSession(DATABASE.Model, DictDataModel):
    """ Readings for GPS data from ODB sensors. """
    __tablename__ = "odb_session"

    id = Column(String(15), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship(User, uselist=False)
    engine_load_readings = relationship('EngineLoad', uselist=True)
    engine_rpm_readings = relationship('EngineRPM', uselist=True)
    fuel_level_readings = relationship('FuelLevel', uselist=True)
    fuel_ratio_readings = relationship('FuelRatio', uselist=True)
    gps_readings = relationship('GPSReading', uselist=True)
    speed_readings = relationship('Speed', uselist=True)
