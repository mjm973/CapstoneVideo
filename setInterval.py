# from https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval

import time, threading

class setInterval:
    def __init__(self, interval, callback, passSelf=False):
        self.interval = interval
        self.callback = callback
        self.stopEvent = threading.Event()
        self.passSelf = passSelf
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            if self.passSelf:
                self.callback(self)
            else:
                self.callback()

    def cancel(self):
        print("CANCELLING THREAD")
        self.stopEvent.set()
