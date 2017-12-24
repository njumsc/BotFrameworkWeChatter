import time


def info(msg):
    print("[%s] %s" % (time.asctime(time.localtime(time.time())), msg))