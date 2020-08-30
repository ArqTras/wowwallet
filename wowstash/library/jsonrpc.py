import json
import requests
from six import integer_types
from decimal import Decimal
from wowstash import config


PICOWOW = Decimal('0.00000000001')

class JSONRPC(object):
    def __init__(self, proto, host, port, username='', password=''):
        self.endpoint = '{}://{}:{}/'.format(
            proto, host, port
        )
        self.auth = requests.auth.HTTPDigestAuth(
            username, password
        )

    def make_rpc(self, method, params={}, json_rpc=True):
        if json_rpc:
            endpoint = self.endpoint + "json_rpc"
        else:
            endpoint = self.endpoint + method

        try:
            r = requests.get(
                endpoint,
                data=json.dumps({'method': method, 'params': params}),
                auth=self.auth
            )
            if 'result' in r.json():
                return r.json()['result']
            elif 'error' in r.json():
                return r.json()['error']
            else:
                return r.json()
        except:
            return {}


class Wallet(JSONRPC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'height' in self.height():
            self.connected = True
        else:
            self.connected = False

    def height(self):
        return self.make_rpc('get_height', {})

    def new_address(self, account_index=0, label=None):
        data = {'account_index': account_index, 'label': label}
        _address = self.make_rpc('create_address', data)
        return (_address['address_index'], _address['address'])

    def get_address(self, account_index, subaddress_index):
        data = {'account_index': account_index, 'address_index': [subaddress_index]}
        subaddress = self.make_rpc('get_address', data)['addresses'][0]['address']
        return subaddress

    def get_balance(self, account_index, subaddress_index):
        data = {'account_index': account_index, 'address_indices': [subaddress_index]}
        _balance = self.make_rpc('get_balance', data)
        locked = from_atomic(_balance['per_subaddress'][0]['balance'])
        unlocked = from_atomic(_balance['per_subaddress'][0]['unlocked_balance'])
        return (float(locked), float(unlocked))

    def get_transfers(self, account_index, subaddress_index):
        data = {
            'account_index': account_index,
            'subaddr_indices': [subaddress_index],
            'in': True,
            'out': True,
            'pending': True,
            'failed': True,
            'pool': True
        }
        return self.make_rpc('get_transfers', data)


class Daemon(JSONRPC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def info(self):
        return self.make_rpc('get_info', {}, json_rpc=False)

    def height(self):
        return self.make_rpc('get_height', {}, json_rpc=False)


def to_atomic(amount):
    if not isinstance(amount, (Decimal, float) + integer_types):
        raise ValueError("Amount '{}' doesn't have numeric type. Only Decimal, int, long and "
                "float (not recommended) are accepted as amounts.")
    return int(amount * 10**11)

def from_atomic(amount):
    return (Decimal(amount) * PICOWOW).quantize(PICOWOW)

def as_wownero(amount):
    return Decimal(amount).quantize(PICOWOW)


daemon = Daemon(
    proto=config.DAEMON_PROTO,
    host=config.DAEMON_HOST,
    port=config.DAEMON_PORT,
    username=config.DAEMON_USER,
    password=config.DAEMON_PASS
)

wallet = Wallet(
    proto=config.WALLET_PROTO,
    host=config.WALLET_HOST,
    port=config.WALLET_PORT,
    username=config.WALLET_USER,
    password=config.WALLET_PASS
)
