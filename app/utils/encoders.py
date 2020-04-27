"""
Custom Encoders.
"""
import datetime

from decimal import Decimal

from flask.json import JSONEncoder


class DefaultJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        return JSONEncoder.default(self, obj)
