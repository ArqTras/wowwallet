from docker import from_env, APIClient
from docker.errors import NotFound
from socket import socket
from wowstash import config
from wowstash.models import User
from wowstash.library.jsonrpc import daemon

class Docker(object):
    def __init__(self):
        self.client = from_env()
        self.wownero_image = getattr(config, 'WOWNERO_IMAGE', 'lalanza808/wownero')
        self.wallet_dir = getattr(config, 'WALLET_DIR', './data/wallets')
        self.listen_port = 34569

    def create_wallet(self, user_id):
        u = User.query.get(user_id)
        command = f"""wownero-wallet-cli \
        --generate-new-wallet /wallet/{u.id}.wallet \
        --restore-height {daemon.info()['height']} \
        --password {u.wallet_password} \
        --mnemonic-language English \
        --daemon-address {config.DAEMON_PROTO}://{config.DAEMON_HOST}:{config.DAEMON_PORT} \
        --daemon-login {config.DAEMON_USER}:{config.DAEMON_PASS} \
        --log-file /wallet/{u.id}-create.log
        --command version
        """
        container = self.client.containers.run(
            self.wownero_image,
            command=command,
            auto_remove=True,
            name=f'create_wallet_{u.id}',
            remove=True,
            detach=True,
            volumes={
                f'{self.wallet_dir}/{u.id}': {
                    'bind': '/wallet',
                    'mode': 'rw'
                }
            }
        )
        return container.short_id

    def start_wallet(self, user_id):
        u = User.query.get(user_id)
        command = f"""wownero-wallet-rpc \
        --non-interactive \
        --rpc-bind-port {self.listen_port} \
        --wallet-file /wallet/{u.id}.wallet \
        --rpc-login {u.id}:{u.wallet_password} \
        --password {u.wallet_password} \
        --daemon-address {config.DAEMON_PROTO}://{config.DAEMON_HOST}:{config.DAEMON_PORT} \
        --daemon-login {config.DAEMON_USER}:{config.DAEMON_PASS} \
        --log-file /wallet/{u.id}-rpc.log
        """
        container = self.client.containers.run(
            self.wownero_image,
            command=command,
            auto_remove=True,
            name=f'start_wallet_{u.id}',
            remove=True,
            detach=True,
            ports={
                f'{self.listen_port}/tcp': None
            },
            volumes={
                f'{self.wallet_dir}/{u.id}': {
                    'bind': '/wallet',
                    'mode': 'rw'
                }
            }
        )
        return container.short_id

    def get_port(self, container_id):
        client = APIClient()
        port_data = client.port(container_id, self.listen_port)
        host_port = port_data[0]['HostPort']
        return int(host_port)

    def container_exists(self, container_id):
        try:
            self.client.containers.get(container_id)
            return True
        except NotFound:
            return False
