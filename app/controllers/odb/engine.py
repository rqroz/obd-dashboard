"""
ODB Controller
"""
import pandas

from sqlalchemy.sql import func

from app.constants.odb import (
    ODBSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers.odb import BaseODBController
from app.models.odb.session import ODBSession
from app.models.odb.engine import EngineLoad
from app.models.user import User


class EngineControllerError(Exception):
    """ Exception class for EngineController """
    pass


class EngineController(BaseODBController):
    """
    Controller class for Engine-related data manipulations.
    """
    def get_engine_load_avg(self, user: User):
        """
        Returns the average engine load considering the complete history of a certain user.
        """
        return (
            self.db_session.query(func.avg(EngineLoad.value))
                            .filter(EngineLoad.session.has(user_id=user.id))
        ).scalar()

    def register_engine_load_from_csv(self, session: ODBSession, csv: pandas.DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine load from CSV for the current user.
        """
        for idx, row in csv.iterrows():
            try:
                eng_load = EngineLoad(
                    session_id=session.id,
                    value=row[CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.LOAD]],
                    date=self._resolve_date_from_csv_row(row),
                )
            except:
                continue

            self.db_session.add(eng_load)

        if flush:
            self.db_session.flush()
        else:
            self.db_session.commit()
