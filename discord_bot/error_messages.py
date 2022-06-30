class BaseCustomException(Exception):
    """Base class for all Custom Exceptions"""


class YouMadeAMistake(BaseCustomException):
    def __init__(self, value="If you see this message contact an Admin",
                 message=f'To Err is to be Human. You made a mistake'):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'There is an error with **{self.value}**\nCustom Message: {self.message}'