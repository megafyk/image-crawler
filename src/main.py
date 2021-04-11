import pathlib
from typing import Dict

from flickr import utils as flickr_utils
from utils.clipboard import ClipboardWriter
from utils.logger import get_logger

logger = get_logger('app')


def write_urls():
    """ Write urls from clipboard to file """
    file_path = input('Enter your file path: ')
    p = pathlib.Path(file_path)
    if not p.is_file():
        logger.warning('Wrong file path, set file path to default abc.txt')
        file_path = "abc.txt"
    writer = ClipboardWriter(file_path)
    writer.run()
    return file_path


if __name__ == "__main__":
    urls_dict: Dict[str, str] = {}

    while True:
        try:
            filepath = write_urls()
            urls_dict = flickr_utils.read_urls(filepath)
        except KeyboardInterrupt:
            pass
        logger.info('Processing %d raw urls...' % sum(len(v)
                                                      for v in urls_dict.values()))
        flickr_utils.download_flickr_imgs(urls_dict)
        isContinue = input('Do you want to continue? (y/n): ').lower() == 'y'
        if not isContinue:
            break
