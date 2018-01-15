import threading
import time


def worker(num):
    """thread worker function"""
    print('Worker: %s' % num)
    return


def wait(count):
    print('going to sleep', count)
    time.sleep(10)
    print('awake', count, time.clock())


threads = []


for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

t = threading.Thread(target=wait, args=('1',))
threads.append(t)
t.start()

print('thread is asleep, main is awake 1')
t = threading.Thread(target=wait, args=('2',))
threads.append(t)
t.start()
print('thread is asleep, main is awake 2')
inp = input('enter something')
print(inp)
print(threads)