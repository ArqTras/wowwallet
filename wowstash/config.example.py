# Site meta
SITE_NAME = 'webwallet.supportcryptonight.com'

# Daemon
DAEMON_PROTO = 'http'
DAEMON_HOST = 'node.supportarqma.com'
DAEMON_PORT = 1994
DAEMON_USER = ''
DAEMON_PASS = ''

# Wallets
WALLET_DIR = './data/wallets'
WOWNERO_IMAGE = 'arqma/arqma:v0.6.1.0'

# Security
PASSWORD_SALT = 'salt here' # database salts
SECRET_KEY = 'secret session key here' # encrypts the session token

# Session
PERMANENT_SESSION_LIFETIME = 1800 # 60 minute session expiry
SESSION_COOKIE_NAME = 'wowstash'
SESSION_COOKIE_DOMAIN = '127.0.0.1'
SESSION_COOKIE_SECURE = False
SESSION_USE_SIGNER = True
SESSION_PERMANENT = True

# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Database
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'wowstash'
DB_USER = 'wowstash'
DB_PASS = 'zzzzzzzzz'

# Development
TEMPLATES_AUTO_RELOAD = True

# Social
SOCIAL = {
    'envelope': 'mailto:admin@domain.co',
    'twitter': 'https://twitter.com/your_twitter_handle',
    'comment': 'https://webchat.freenode.net/?room=#wownero',
    'reddit': 'https://reddit.com/r/wownero'
}
