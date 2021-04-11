import json
import os
from utils.logger import get_logger


class ApiDataReader(object):
    """Get api data from json file"""
    logger = get_logger('ApiDataReader')

    def __init__(self, filepath):
        try:
            fp = open(filepath)
            with fp:
                data = json.load(fp)
                self._api_key = data['api_key']
                self._api_secret = data['api_secret']
                self._api_url = data['api_url']
                fp.close()
        except Exception as ex:
            self.logger.error(ex)

    @property
    def api_key(self):
        return self._api_key

    @property
    def api_secret(self):
        return self._api_secret

    @property
    def api_url(self):
        return self._api_url


class AppDataReader(object):
    """Get app data from json file"""
    logger = get_logger('ApiDataReader')

    def __init__(self, filepath):
        try:
            fp = open(filepath)
            with fp:
                data = json.load(fp)
                self._path_saved = data['path_saved']
                fp.close()
        except Exception as ex:
            self.logger.error(ex)

    @property
    def path_saved(self):
        return self._path_saved
