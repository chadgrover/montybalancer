from threading import Timer

def set_interval(callback, s=10):
    def wrapper():
        set_interval(callback, s)
        callback()

    t = Timer(s, wrapper)
    t.start()
    return t

