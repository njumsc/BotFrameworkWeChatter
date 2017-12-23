import config

def auth_header(more={}):
    base = {"Authorization": "Bearer " + config.bot_secret_key}
    base.update(more)
    return base