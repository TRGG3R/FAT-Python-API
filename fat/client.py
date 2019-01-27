import random
import string
from urllib.parse import urlparse, urljoin  # noqa
from .exceptions import (handle_error_response, params_token_validation_error,
                         params_token_validation_error_address,
                         params_token_validation_error_nf_token,
                         params_token_validation_error_entry_hash)
from .session import FATAPISession


class BaseAPI(object):
    def __init__(self, chain_id=None, token_id=None, issuer_id=None,
                 fat_address=None, fct_address=None, host=None,
                 version='v2', username=None, password=None, certfile=None):
        """
         Instantiate a new API client.
         Args:
             fat_address (str): A default Factom Asset Token address to
             use for transactions.
             fct_address (str): A default factoid address to use for
                 transactions. Factoids will be spent from this address.
             host (str): Hostname, including http(s)://, of the factomd
             or factom-walletd instance to query.
             version (str): API version to use. This should remain 'v2'.
             username (str): RPC username for protected APIs.
             password (str): RPC password for protected APIs.
             certfile (str): Path to certificate file to verify for TLS
                 connections (mostly untested).
         """
        self.chain_id = chain_id
        self.token_id = token_id
        self.issuer_id = issuer_id
        self.fat_address = fat_address
        self.fct_address = fct_address
        self.version = version

        if host:
            self.host = host

        self.session = FATAPISession()

        if username and password:
            self.session.init_basic_auth(username, password)

        if certfile:
            self.session.init_tls(certfile)

    @property
    def url(self):
        return urljoin(self.host, self.version)

    def _xact_name(self):
        return 'TX_{}'.format(''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6)))

    def _request(self, method, params=None, id=0):
        data = {
            'jsonrpc': '2.0',
            'id': id,
            'method': method,
        }
        if params:
            data['params'] = params

        resp = self.session.request('POST', self.url, json=data)

        if resp.status_code >= 400:
            handle_error_response(resp)

        return resp.json()['result']


class ParamsToken(object):
    def __init__(self, chain_id=None, token_id=None, issuer_id=None):
        self.chain_id = chain_id
        self.token_id = token_id
        self.issuer_id = issuer_id

    def paramstoken_valid(self):
        if (self.chain_id is not None and len(self.token_id) is 0 and
            self.issuer_id is None) or \
                (self.chain_id is None and len(self.token_id) is not 0 and
                 self.issuer_id is not None):
            return True
        else:
            return False


class FATd(BaseAPI):

    host = 'http://localhost:8078/v0'

    def get_balance(self, chain_id=None, token_id=None, issuer_id=None,
                    fct_address=None):
        if ParamsToken.paramstoken_valid(self) is True and fct_address is not \
                None:
            if chain_id is not None:
                return self._request('get-balance', {
                    'chain-id': chain_id,
                    'fa-address': fct_address
                })
            else:
                return self._request('get-balance', {
                    'token-id': token_id,
                    'issuer-id': issuer_id,
                    'fa-address': fct_address
                })
        else:
            raise params_token_validation_error_address()

    def get_issuance(self, chain_id=None, token_id=None, issuer_id=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-issuance', {
                    'chain-id': chain_id
                })
            else:
                return self._request('get-issuance', {
                    'token-id': token_id,
                    'issuer-id': issuer_id
                })
        else:
            raise params_token_validation_error()

    def get_issuance_entry(self, chain_id, token_id=None, issuer_id=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-issuance-entry', {
                    'chain-id': chain_id
                })
            else:
                return self._request('get-issuance-entry', {
                    'token-id': token_id,
                    'issuer-id': issuer_id
                })
        else:
            raise params_token_validation_error()

    def get_stats(self, chain_id=None, token_id=None, issuer_id=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-stats', {
                    'chain-id': chain_id
                })
            else:
                return self._request('get-stats', {
                    'token-id': token_id,
                    'issuer-id': issuer_id
                })
        else:
            raise params_token_validation_error()

    def get_transaction(self, chain_id=None, token_id=None, issuer_id=None,
                        entry_hash=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-transaction', {
                    'chain-id': chain_id,
                    'entryhash': entry_hash
                })
            else:
                return self._request('get-transaction', {
                    'token-id': token_id,
                    'issuer-id': issuer_id,
                    'entryhash': entry_hash
                })
        else:
            raise params_token_validation_error_entry_hash()

    def get_transaction_entry(self, chain_id=None, token_id=None,
                              issuer_id=None, entry_hash=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-transaction-entry', {
                    'chain-id': chain_id,
                    'entryhash': entry_hash
                })
            else:
                return self._request('get-transaction-entry', {
                    'token-id': token_id,
                    'issuer-id': issuer_id,
                    'entryhash': entry_hash
                })
        else:
            raise params_token_validation_error_entry_hash()

    def get_nf_token(self, chain_id=None, token_id=None, issuer_id=None,
                     nf_token_id=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-transaction', {
                    'chain-id': chain_id,
                    'nf-token-id': nf_token_id
                })
            else:
                return self._request('get-transaction', {
                    'token-id': token_id,
                    'issuer-id': issuer_id,
                    'nf-token-id': nf_token_id
                })
        else:
            raise params_token_validation_error_nf_token()

    def send_transaction(self, chain_id=None, token_id=None, issuer_id=None,
                         tx=None, raw_entry=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('send-transaction', {
                    'chain-id': chain_id,
                    'tx': tx,
                    'signaturesRcds': raw_entry
                })
            else:
                return self._request('send-transaction', {
                    'token-id': token_id,
                    'issuer-id': issuer_id,
                    'tx': tx,
                    'signaturesRcds': raw_entry
                })
        else:
            raise params_token_validation_error()

    def get_daemon_tokens(self, chain_id=None, token_id=None, issuer_id=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-daemon-tokens', {
                    'chain-id': chain_id
                })
            else:
                return self._request('get-daemon-tokens', {
                    'token-id': token_id,
                    'issuer-id': issuer_id
                })
        else:
            raise params_token_validation_error()

    def get_daemon_properties(self, chain_id=None, token_id=None, issuer_id=None):
        if ParamsToken.paramstoken_valid(self) is True:
            if chain_id is not None:
                return self._request('get-daemon-properties', {
                    'chain-id': chain_id
                })
            else:
                return self._request('get-daemon-properties', {
                    'token-id': token_id,
                    'issuer-id': issuer_id
                })
        else:
            raise params_token_validation_error()
