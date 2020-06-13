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

    car_states = relationship('CarState', uselist=True)

    @classmethod
    def create(cls, db_session, **kwargs):
        instance = cls(**kwargs)
        db_session.add(instance)
        db_session.flush()
        return instance

    def to_flat_data(self):
        """ Flattens the data for the current session states """
        return {
            'id': self.id,
            'date': self.date,
            'car_states': [state.to_flat_data() for state in self.car_states],
        }
