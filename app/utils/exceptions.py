class BaseException(Exception):

    def __init__(self, message:str, *args):
        self.message = message
        super().__init__(message, *args)

class ResourceNotFoundException(BaseException):
    ...

class BusinessException(BaseException):
    ...

class InvalidAmountException(BaseException):
    ...

class InsufficientBalanceException(BaseException):

    def __init__(self, *args):
        super().__init__("Insufficient balance to transfer.", *args)

class UnauthorizedWalletException(BaseException):
    ...