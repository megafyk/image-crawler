import time
import tkinter as tk

from utils.logger import get_logger


class ClipboardWriter(object):
    # Clipboard's timer countdown
    CLIP_TIMER = 1
    logger = get_logger('ClipboardWriter')

    def __init__(self, filepath):
        self._filepath = filepath
        self._temp_clip = ""
        # clear clipboard
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.selection_clear()

    def run(self):
        """Run clipboard writer.
        Read and write url from clipboard every CLIP_TIMER tick.

        """
        try:
            while True:
                if self.is_has_new_clipboard(self._temp_clip):
                    url = self.read_clipboard()
                    self.logger.info("Has new url: %s", url)
                    self.write_to_file(url)
                self.logger.info("Waiting...")
                time.sleep(self.CLIP_TIMER)
        except KeyboardInterrupt:
            pass

    def is_has_new_clipboard(self, temp_clip):
        """Detech new url from clipboard.

        Parameters
        ----------
        temp_clip : str
            Url from clipboard.
        """
        try:
            return temp_clip != self.root.selection_get()
        except tk.TclError:
            return False

    def read_clipboard(self):
        """Set new clipboard to temp

        Returns
        -------
        _temp_clip : str
            Temporary clipboard
        """
        self._temp_clip = self.root.selection_get()
        return self._temp_clip

    def write_to_file(self, url):
        """Write url to file  

        Parameters
        ----------
        url : str
            Url
        """
        try:
            with open(self._filepath, 'a') as f:
                f.write(url + '\n')
                f.close()
        except Exception as ex:
            self.logger.error(ex)
