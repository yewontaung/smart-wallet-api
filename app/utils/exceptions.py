class BaseException(Exception):

    def __init__(self, message:str, *args):
        self.message = message
        super().__init__(message, *args)

class ResourceNotFoundException(BaseException):
    ...

class BusinessException(BaseException):
    ...