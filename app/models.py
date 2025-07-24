import threading
import time

class URLStore:
    def __init__(self):
        self.data = {}  # short_code = {url, clicks, created_at}
        self.lock = threading.Lock()

    def save(self, short_code, original_url):
        with self.lock:
            self.data[short_code] = {
                "url": original_url,
                "clicks": 0,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
            }

    def get(self, short_code):
        with self.lock:
            return self.data.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.data:
                self.data[short_code]["clicks"] += 1
                return True
            return False

    def stats(self, short_code):
        with self.lock:
            return self.data.get(short_code)
