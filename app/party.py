from app import exceptions
from app.serializable import Serializable

class Party(Serializable):
    def __init__(self, data=None):
        """
        Initialize a new shipment Party instance.

        :type data: dict
        """
        self.name = ""
        self.address = ""
        super().__init__(data)  # Initializes the parent class

    def validate(self, data=None):
        """
        Validate the Party data to ensure no fields are empty.

        :type data: dict
        """
        for field_name, field_val in (data or self.__dict__).items():
            if not field_val:
                raise exceptions.ContentNotSet(
                    f"No shipment party fields should be empty, as {field_name} is."
                )
        super().validate(data)  # Calls the validate method of the parent class
