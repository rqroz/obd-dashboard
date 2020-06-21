"""
OBD Session.
"""
import math
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database import DATABASE
from app.models import DictDataModel
from app.models.user import User


class OBDSession(DATABASE.Model, DictDataModel):
    """ Readings for GPS data from OBD sensors. """
    __tablename__ = "obd_session"

    protected_fields = ['user_id']

    id = Column(String(15), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    date = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship(User, uselist=False)

    car_states = relationship('CarState', uselist=True)

    @property
    def states(self):
        if not getattr(self, '_car_states', None):
            self._car_states = sorted(self.car_states, key=lambda state: state.timestamp)
        return self._car_states

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
            'car_states': self.states,
        }

    def get_profile(self):
        """ Resolves driver profile information """
        car_states = self.states
        values = {
            'throttle_position': [car.throttle_position for car in car_states],
            'speed': [car.speed for car in car_states],
            'engine_map': [car.engine.map for car in car_states],
            'engine_maf': [car.engine.maf for car in car_states],
            'engine_rpm': [car.engine.rpm for car in car_states],
            'engine_load': [car.engine.load for car in car_states],
            'engine_coolant_temp': [car.engine.coolant_temp for car in car_states],
            'fuel_lambda': [car.fuel.cmd_equivalence_ratio for car in car_states],
            'fuel_ratio': [car.fuel.ratio for car in car_states],
        }
        max_values = {key: max(value) for key, value in values.items()}
        keys = list(values.keys())

        number_of_metrics = len(keys)
        angle = 360 / number_of_metrics
        max_area = 3 * 1 * math.sqrt(3) / 2 # A_hex = 3 * L^2 * sqrt(3) / 2

        radar_values = []
        profile_values = []
        for idx in range(len(car_states)):
            data = {}
            profile = 0

            for key in keys:
                data[key] = values[key][idx]/max_values[key] if max_values[key] > 0 else 0

            for i, key in enumerate(data):
                next_key = keys[(i+1)%number_of_metrics]
                next_val = data[next_key]
                curr_val = data[key]
                area = (float(curr_val) * float(next_val) * math.sin(angle)) / 2
                profile += area / max_area

            radar_values.append(data)
            profile_values.append({'value': profile, 'date': car_states[idx].date})

        return {
            'radar': radar_values,
            'profile': profile_values,
        }
