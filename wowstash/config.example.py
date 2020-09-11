# Site meta
SITE_NAME = 'WOW Stash'

# Daemon
DAEMON_PROTO = 'http'
DAEMON_HOST = 'node.suchwow.xyz'
DAEMON_PORT = 34568
DAEMON_USER = ''
DAEMON_PASS = ''

# Wallet
WALLET_PROTO = 'http'
WALLET_HOST = 'localhost'
WALLET_PORT = 9999
WALLET_USER = 'yyyyy'
WALLET_PASS = 'xxxxx'

# Security
PASSWORD_SALT = 'salt here' # database salts
SECRET_KEY = 'secret session key here' # encrypts the session token

# Session
PERMANENT_SESSION_LIFETIME = 1800 # 60 minute session expiry
SESSION_TYPE = 'redis'
SESSION_COOKIE_NAME = 'wowstash'
SESSION_COOKIE_SECURE = False
SESSION_USE_SIGNER = True
SESSION_PERMANENT = True
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
