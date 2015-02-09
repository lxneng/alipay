class AlipayException(Exception):
    '''Base Alipay Exception'''


class MissingParameter(AlipayException):
    """Raised when the create payment url process is missing some
    parameters needed to continue"""


class ParameterValueError(AlipayException):
    """Raised when parameter value is incorrect"""


class TokenAuthorizationError(AlipayException):
    '''The error occurred when getting token '''
