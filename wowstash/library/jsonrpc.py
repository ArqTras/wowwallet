import json
import requests
from wowstash import config

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
    def height(self):
        return self.make_rpc('get_height', {})

class Daemon(JSONRPC):
    def info(self):
        return self.make_rpc('get_info', {}, json_rpc=False)

    def height(self):
        return self.make_rpc('get_height', {}, json_rpc=False)


daemon = Daemon(proto=config.DAEMON_PROTO, host=config.DAEMON_HOST, port=config.DAEMON_PORT)
