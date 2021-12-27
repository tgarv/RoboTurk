# Stolen from https://stackoverflow.com/questions/15302883/python-in-linux-put-user-input-asynchronously-into-queue

import threading
import sys

bufferLock = threading.Lock()
inputBuffer = []


class InputThread(threading.Thread):
    def run(self):
        global inputBuffer
        print("starting input")
        while True:
            line = sys.stdin.readline()
            bufferLock.acquire()
            inputBuffer.insert(0, line)
            bufferLock.release()
