# -*- coding: utf-8 -*-
import time
from queue import Queue
import myio
import threading


def do_io(thread_name, que, store):
    while True:
        data = que.get()
        if data == None:
            time.sleep(0.1)
        store.putData(data)
        data.clear()

class myThread(threading.Thread):
    def __init__(self, name, que, store):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = que
        self.store = store
        # self.counter = counter
    def run(self):
        print ("Starting ", self.name)
       # 获得锁，成功获得锁定后返回True
       # 可选的timeout参数不填时将一直阻塞直到获得锁定
       # 否则超时后将返回False
        # threadLock.acquire()
        do_io(self.name, self.queue, self.store)
        # 释放锁
        # threadLock.release()