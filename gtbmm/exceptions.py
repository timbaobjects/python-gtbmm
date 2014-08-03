class AuthenticationError(Exception):
    pass


class InvalidAccountError(AuthenticationError):
    message = 'Invalid Account'


class IncorrectPinError(AuthenticationError):
    message = 'Incorrect PIN'


class LoginRequiredError(AuthenticationError):
    message = 'Login Required'


class InvalidRequestError(Exception):
    pass


class PaymentError(Exception):
    pass


class PaymentBelowMinimumError(PaymentError):
    message = 'Less Than Minimum Payment Amount'


class PaymentAboveMaximumError(PaymentError):
    message = 'More Than Maximum Payment Amount'


class PaymentInvalidError(PaymentError):
    message = 'Invalid Payment Amount'


class InsufficientFundsError(PaymentError):
    message = 'Insufficient Funds'


class PaymentSelfReferenceError(PaymentError):
    message = 'Cannot Pay Self'


class IncorrectDestionationAccountError(PaymentError):
    message = 'Incorrect Destination Account'


class InvalidDestionationAccountError(PaymentError):
    message = 'Invalid Destination Account'


class InactiveDestionationAccountError(PaymentError):
    message = 'Inactive Destination Account'


EXCEPTIONS_MAP = {
    # Invalid Account
    '11': InvalidAccountError,

    # Insufficient Funds
    '16': InsufficientFundsError,

    # Incorrect PIN
    '29': IncorrectPinError,

    # More than maximum payment
    '106': PaymentAboveMaximumError,

    # Less than minimum payment
    '107': PaymentBelowMinimumError,

    # Invalid Payment Account
    '128': InactiveDestionationAccountError,

    # Invalid Amount
    '212': PaymentInvalidError,

    # Cannot Pay Self
    '295': PaymentSelfReferenceError,

    # Invalid Request
    '546': InvalidRequestError,

    # Login Required
    '631': LoginRequiredError,

    # Unknown Payment Account
    '687': IncorrectDestionationAccountError,

    # Invalid Payment Account
    '2020': InvalidDestionationAccountError,
}
