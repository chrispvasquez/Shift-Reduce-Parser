import time
import datetime

class Timer:
    def __init__(self):
        self._start_time = None
        self.elapsed_timee = None
    def start(self):
        self._start_time = time.perf_counter()

    def stop(self):

        self.elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

    def getTime(self):

        return str(datetime.timedelta(seconds=self.elapsed_time))