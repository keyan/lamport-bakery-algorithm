"""
An implementation of Lamport's Bakery Algorithm.
"""
import threading
import time


class Lock(object):
    def __init__(self, num_threads):
        self.num_threads = num_threads

        # These arrays represent shared memory between threads. The
        # algorithm can be used for interprocess synchronization so
        # long as a sufficient means of shared memory can be
        # implemented.
        self.choosing = [0 for _ in xrange(num_threads)]
        self.numbers = [0 for _ in xrange(num_threads)]

    def acquire(self, thread_id):
        # Note, there is no atomic guarantee here when setting choosing
        # to 1 and selecting a number. But Lamport proves that it does
        # not matter if the subsequent read incorrect for any thread
        # in the below loop.
        self.choosing[thread_id] = 1
        self.numbers[thread_id] = 1 + max(self.numbers)
        self.choosing[thread_id] = 0

        for j in xrange(self.num_threads):
            # Another thread is choosing its number, wait until safe.
            while self.choosing[j] != 0:
                pass
            # If number is 0, we know the thread is either done or never
            # requested a number. If number is not 0, we can still
            # proceed if our number is lower. In the case of tie,
            # thread_id breaks the tie.
            while self.numbers[j] != 0 and (self.numbers[j], j) < (self.numbers[thread_id], thread_id):
                pass

        # After checking all values in the choosing/numbers arrays, it
        # is safe to provide the lock and for the thread to access its
        # critical section.
        return True

    def release(self, thread_id):
        self.numbers[thread_id] = 0


def safe_modify_state():
    global lock
    global safe_counter

    thread_id = int(threading.current_thread().name)
    try:
        lock.acquire(thread_id)
        tmp = safe_counter
        time.sleep(0.01)
        safe_counter = tmp + 1
        print safe_counter
    finally:
        lock.release(thread_id)


def unsafe_modify_state():
    global unsafe_counter

    tmp = unsafe_counter
    time.sleep(0.001)
    unsafe_counter = tmp + 1
    print unsafe_counter


if __name__ == '__main__':
    num_threads = 100
    lock = Lock(num_threads)

    # Trying to increment to 100 and print without locking results in
    # undeterministic weird output.
    unsafe_counter = 0
    thread_pool = [threading.Thread(group=None, target=unsafe_modify_state, name=i)
                   for i in xrange(num_threads)]
    for thread in thread_pool:
        thread.start()

    safe_counter = 0
    thread_pool = [threading.Thread(group=None, target=safe_modify_state, name=i)
                   for i in xrange(num_threads)][1:]
    for thread in thread_pool:
        thread.start()
