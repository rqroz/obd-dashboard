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

    protected_fields = ['user_id']

    id = Column(String(15), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship(User, uselist=False)

    engine_load_readings = relationship('EngineLoad', uselist=True)
    engine_rpm_readings = relationship('EngineRPM', uselist=True)
    engine_map_readings = relationship('ManifoldPressure', uselist=True)
    engine_maf_readings = relationship('MassAirFlow', uselist=True)
    engine_voltage_readings = relationship('EngineVoltage', uselist=True)
    engine_coolant_temp_readings = relationship('EngineCoolantTemp', uselist=True)

    speed_readings = relationship('Speed', uselist=True)

    fuel_level_readings = relationship('FuelLevel', uselist=True)
    fuel_ratio_readings = relationship('FuelRatio', uselist=True)
    fuel_lambda_readings = relationship('FuelLambda', uselist=True)

    gps_readings = relationship('GPSReading', uselist=True)
