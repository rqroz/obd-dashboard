"""
Custom Encoders.
"""
from decimal import Decimal

from flask.json import JSONEncoder


class DefaultJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return JSONEncoder.default(self, obj)
