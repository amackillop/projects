import os
import shutil

import urllib.request

import config


def download_file(url: str, path: str):
    with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def maybe_download_model():
    if not os.path.exists(config.MODELS):
        os.mkdir(config.MODELS)
        for fname, url in config.MODEL_URLS.items():
            download_file(url, config.MODELS + fname)


if __name__ == '__main__':
    maybe_download_model()
    

