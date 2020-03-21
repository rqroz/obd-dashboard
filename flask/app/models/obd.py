"""
OBD Specific models
"""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from app.database import DATABASE
from app.models import DictDataModel
from app.models.user import User


class OBDSensorUnit(DATABASE.Model, DictDataModel):
    """
    OBD Sensor unit deifnition.
    """
    __tablename__ = "obd_sensor_unit"

    id = Column(Integer, primary_key=True)
    label = Column(String(10), nullable=False)


class OBDSensor(DATABASE.Model, DictDataModel):
    """
    OBD Sensor definition.
    """
    __tablename__ = "obd_sensor"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    short_name = Column(String(50), nullable=False)
    label = Column(String(20), nullable=False)


class OBDSensorUser(DATABASE.Model, DictDataModel):
    """
    Sensor-User relation.
    """
    __tablename__ = "obd_sensor_user"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    sensor_id = Column(Integer, ForeignKey(OBDSensor.id))
    unit_id = Column(Integer, ForeignKey(OBDSensorUnit.id))

    user = relationship(User, uselist=False)
    sensor = relationship(OBDSensor, uselist=False)
    unit = relationship(OBDSensorUnit, uselist=False)

    def to_dict(self, include_protected=False):
        return {
            'id': self.id,
            'user': self.user.to_dict(include_protected),
            'sensor': self.sensor.to_dict(include_protected),
            'unit': self.unit.to_dict(include_protected),
        }


class OBDSensorValue(DATABASE.Model, DictDataModel):
    """
    Value of a sensor attached to a user.
    """
    __tablename__ = "obd_sensor_value"

    id = Column(Integer, primary_key=True)
    su = Column(Integer, ForeignKey(OBDSensorUser.id))
    value = Column(Numeric, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
