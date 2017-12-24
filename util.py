import config, shutil, urllib

def auth_header(more={}):
    base = {"Authorization": "Bearer " + config.bot_secret_key}
    base.update(more)
    return base

def or_empty(s):
    return s if s else ""

def download_file(url, filepath):
    with urllib.request.urlopen(urllib.parse.quote(url, safe='/:?=')) as response, open(filepath, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
