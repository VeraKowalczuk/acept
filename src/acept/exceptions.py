"""Module for exceptions."""


class ValueOutsideRangeError(ValueError):
    """
    Exception raised when a value is outside the allowed range.
    """

    def __init__(self, min_value: int, max_value: int, data_type: str = "DWD TRY"):
        """
        Initialize the exception, that will be raised when a value is outside the allowed range.

        :param min_value: minimum allowed value
        :param max_value: maximum allowed value
        :param data_type: name of the data type that is checked
        """
        self.min_value = min_value
        self.max_value = max_value
        self.message = f"{data_type} data has max range: year_start={self.min_value}, year_end={self.max_value}."
        super().__init__(self.message)
