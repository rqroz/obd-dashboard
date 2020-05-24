"""
ODB Controller
"""
from app.controllers.odb import BaseODBSensorController
from app.models.odb.fuel import (
    FuelLevel,
    FuelRatio,
    FuelLambda,
)
from app.models.user import User


class FuelController(BaseODBSensorController):
    """
    Controller class for Engine-related data manipulations.
    """
    MODEL_MAP = {
        'lambda': FuelLambda,
        'level': FuelLevel,
        'ratio': FuelRatio,
    }

    def get_latest_fuel_level(self, user: User):
        """ Get's the last fuel level value for the current user """
        level = (
            self.db_session.query(FuelLevel.value)
                            .filter(FuelLevel.session.has(user_id=user.id))
                            .order_by(FuelLevel.date.desc())
                            .first()
        )

        if level:
            return level.value
        return None
