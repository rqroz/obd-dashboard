"""
OBD Specific models
"""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric

from app.database import DATABASE
from app.models import DictDataModel
from app.models.user import User


class OBDSensorUnit(DATABASE.Model, DictDataModel):
    """
    OBD Sensor unit deifnition.
    """
    __tablename__ = "obd_sensor_unit"

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)


class OBDSensor(DATABASE.Model, DictDataModel):
    """
    OBD Sensor definition.
    """
    __tablename__ = "obd_sensor"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    short_name = Column(String(20), nullable=False)


class OBDSensorUser(Database.Model, DictDataModel):
    """
    Sensor-User relation.
    """
    __tablename__ = "obd_sensor_user"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey(User.id))
    sensor = Column(Integer, ForeignKey(OBDSensor.id))
    unit = Column(Integer, ForeignKey(OBDSensorUnit.id))


class OBDSensorValue(Database.Model, DictDataModel):
    """
    Value of a sensor attached to a user.
    """
    __tablename__ = "obd_sensor_value"

    id = Column(Integer, primary_key=True)
    su = Column(Integer, ForeignKey(OBDSensorUser.id))
    value = Column(Numeric, nullable=False)
    date = Column(Datetime, default=datetime.datetime.utcnow)
