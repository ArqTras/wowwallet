from requests import post as r_post
from json import dumps
from flask import current_app
from wowstash import config


def post_webhook(msg):
    if getattr(config, 'MM_ENABLED', False):
        try:
            if current_app.config["DEBUG"]:
                msg = "[DEBUG] " + msg
            data = {
                "text": msg,
                "channel": config.MM_CHANNEL,
                "username": config.MM_USERNAME,
                "icon_url": config.MM_ICON
            }
            res = r_post(config.MM_ENDPOINT, data=dumps(data))
            res.raise_for_status()
            return True
        except:
            return False
