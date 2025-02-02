from app import exceptions


class Serializable:
    def __init__(self, data=None):
        """
        Create a new Serializable object

        :param data: dict
        """
        if data is not None:
            self.unserialize(data)

    def validate(self, data=None):
        """
        Make sure given data matches the object it populates and is in proper format

        :param data: dict
        """
        for field_name, field_val in (data or self.__dict__).items():
            if not field_val and (field_name != "id" if data is None else True):
                raise exceptions.ContentNotSet(
                    "No serializable object fields should be empty, as %s is"
                    % field_name
                )

    def serialize(self):
        """
        Return the object serialized into a dict

        :return: dict
        """
        return {
            k: self.__dict__[k].serialize() if isinstance(v, Serializable) else v
            for k, v in self.__dict__.items()
        }

    def unserialize(self, data):
        """
        Use given dict data to populate the object.
        Make sure it is properly validated!

        :param data: dict
        :return: Serializable
        """
        self.validate(data)
        if set(data.keys()) | {"id"} != set(self.__dict__.keys()) | {"id"}:
            raise exceptions.ContentNotSet("Keys must match object fields")
        _data = {
            k: self.__dict__[k].unserialize(v)
            if isinstance(self.__dict__[k], Serializable)
            else v
            for k, v in data.items()
        }
        self.__dict__.update(_data)
        return self
