import os

import requests
from utils.logger import get_logger

logger = get_logger('utils.downloader')


def download_img(url, path_saved):
    """Download image from chunk.
    Parameters
    ----------
    url : str
        Image url.
    path_saved : str
        Directory where to save image file.v
    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        filename = url.rsplit('/', 1)[1]
        with open(os.path.join(path_saved, filename), 'wb') as f:
            chunk_size = 128
            for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
                f.write(chunk)
            f.close()
