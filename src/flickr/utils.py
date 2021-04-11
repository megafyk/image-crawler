import functools
import multiprocessing
import pathlib
import re
from typing import Dict

import requests

from utils import downloader, logger
from . import reader as flickr_reader

logger = logger.get_logger('flickr.utils')


def get_author_id(url):
    """Get flick author id from url.
    Parameters
    ----------
    url : str
        Image url.
    Returns
    -------
    str
        Flick author id
    """
    regex = re.compile(r'(photos)(\/)([a-zA-Z0-9]+([@_ -]?[a-zA-Z0-9])*)(\/)')
    return regex.search(url).group(3)


def get_author_info(url, api_url, api_key):
    """Get flick author info from url.
    Parameters
    ----------
    url : str
        Image url.
    Returns
    -------
    json
        Flick author info.
    """
    params = {
        'method': 'flickr.urls.lookupUser',
        'api_key': api_key,
        'url': url,
        'format': 'json',
        'nojsoncallback': '1'
    }
    return requests.get(api_url, params=params).json()


def get_photo_id(url):
    """Get flick photo id from url.
    Parameters
    ----------
    url : str
        Image url.
    Returns
    -------
    json
        Flick photo id.
    """
    regex = re.compile(r'(\/)(\d+)(\/)')
    return regex.search(url).group(2)


def is_valid_url(url):
    """Validate url.
    Parameters
    ----------
    url : str
        Image url.
    Returns
    -------
    bool
        True if url is valid, False otherwise.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://# domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url)


def read_urls(filepath):
    """ Read urls from files """
    urls_dict: Dict[str, str] = {}
    p = pathlib.Path(filepath)
    if not p.is_file():
        logger.warn('Wrong file path...')
        return urls_dict
    with open(p) as f:
        lines = f.readlines()
        for i, url in enumerate(lines):
            url = url.rstrip()
            if is_valid_url(url):
                author_id = get_author_id(url)
                if author_id in urls_dict:
                    if url in urls_dict[author_id]:
                        logger.warn('Duplicate url in lines: %d' % i)
                    else:
                        urls_dict[author_id].append(url)
                else:
                    urls_dict[author_id] = [url]
            else:
                logger.warn('Wrong url in line: %d', i)
        f.close()
    return urls_dict


def download_flickr_img(params, url, path_saved):
    """ Download an original image from flickr """
    r = requests.get(url, params)
    data = r.json()
    if r.status_code == 200 and ('sizes' in r.json()):
        downloader.download_img(
            data['sizes']['size'][-1]['source'], path_saved)


def download_flickr_imgs(urls_dict):
    """ Download image in multiprocess mode """
    api_data_reader = flickr_reader.ApiDataReader(
        filepath='flickr/flickr_api.json')
    app_data_reader = flickr_reader.AppDataReader(
        filepath='flickr/flickr_app.json')
    params = {
        'method': 'flickr.photos.getSizes',
        'api_key': api_data_reader.api_key,
        'photo_id': '',
        'format': 'json',
        'nojsoncallback': '1'
    }
    arr_params = []
    for key in urls_dict:
        for url in urls_dict[key]:
            params['photo_id'] = get_photo_id(url)
            arr_params.append(params)
    with multiprocessing.Pool() as pool:
        pool.map(functools.partial(
            download_flickr_img, url=api_data_reader.api_url, path_saved=app_data_reader.path_saved), arr_params)
