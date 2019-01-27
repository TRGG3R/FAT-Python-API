def handle_error_response(resp):
    codes = {
        -1: FATAPIError,
        -32800: TokenNotFound,
        -32801: InvalidAddress,
        -32803: TransactionNotFound,
        -32804: InvalidTransaction,
        -32805: TokenSyncing,
        -32806: NoEC
    }
    error = resp.json().get('error', {})
    message = error.get('message')
    code = error.get('code', -1)
    data = error.get('data', {})

    raise codes[code](message=message, code=code, data=data, response=resp)


def params_token_validation_error():
    print('Token Validation Error: Please check that a valid ChainID is'
          ' present or both the token_id and issuer_id are included')


def params_token_validation_error_address():
    print('Please check that an FCT address is present. Also, please '
          'check that a valid ChainID is used or both the token_id and '
          'issuer_id are included')


def params_token_validation_error_nf_token():
    print('Please check that a non-fungible token is present. Also, '
          'please check that a valid ChainID is used or both the '
          'token_id and issuer_id are included')


def params_token_validation_error_entry_hash():
    print('Please check that an entry hash is present. Also, please '
          'check that a valid ChainID is used or both the token_id and '
          'issuer_id are included')


class FATAPIError(Exception):
    response = None
    data = {}
    code = -1
    message = "An unknown error occurred"

    def __init__(self, message=None, code=None, data=(), response=None):
        self.response = response
        if message:
            self.message = message
        if code:
            self.code = code
        if data:
            self.data = data

    def __str__(self):
        if self.code:
            return '{}: {}'.format(self.code, self.message)
        return self.message


class TokenNotFound(FATAPIError):
    pass


class InvalidAddress(FATAPIError):
    pass


class TransactionNotFound(FATAPIError):
    pass


class InvalidTransaction(FATAPIError):
    pass


class TokenSyncing(FATAPIError):
    pass


class NoEC(FATAPIError):
    pass
