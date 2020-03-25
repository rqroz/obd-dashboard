"""
Tasty tasty data models
"""


class DictDataModel(object):
    """
    Mixin class to give some convenience methods for dictionary
    rendering of a model's data
    """
    private_fields = []
    protected_fields = []

    def to_dict(self, include_protected=False):
        columns = [x.name for x in self.__table__.columns]
        restricted_fields = (self.private_fields + self.protected_fields)
        data = {
            key: getattr(self, key) for key in columns
            if key not in restricted_fields
        }
        if include_protected:
            data.update({
                key: getattr(self, key) for key in columns
                if key in self.protected_fields
            })
        return data
