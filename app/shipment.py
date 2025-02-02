# app/shipment.py
from app import exceptions
from app.serializable import Serializable

class Shipment(Serializable):
    def __init__(self, data=None):
        """
        Initialize a new shipment instance

        :type data: dict
        """
        self.package_id = ""
        self.status = "pending"
        self.destination = ""
        self.weight = 0.0
        super().__init__(data)

    def validate(self, data=None):
        """
        Validate the Shipment data to ensure no fields are empty.
        
        :type data: dict
        """
        for field_name, field_val in (data or self.__dict__).items():
            if not field_val:
                raise exceptions.ContentNotSet(
                    f"No shipment fields should be empty, as {field_name} is."
                )
        super().validate(data)
