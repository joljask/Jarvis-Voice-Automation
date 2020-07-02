import psutil
import time


class Jk_internet:
    def __init__(self):
        self.current_download()
        self.current_upload()

    def current_download(self):
        self.last_recieved = psutil.net_io_counters(pernic=False)[1]
        time.sleep(0.2)
        self.curent_recieved = psutil.net_io_counters(pernic=False)[1] - self.last_recieved
        return round(self.curent_recieved / 1000, 2)


    def current_upload(self):
        self.last_sent = psutil.net_io_counters(pernic=False)[2]
        time.sleep(0.2)
        self.current_sent = psutil.net_io_counters(pernic=False)[2] - self.last_sent
        return self.current_sent


