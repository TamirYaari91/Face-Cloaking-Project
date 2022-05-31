import logging
import threading
import time
# import connect_to_uni


def thread_func_face_off(name):
    logging.info("Thread %s: starting", name)
    # connect_to_uni.face_off_wrapper()
    time.sleep(10)
    logging.info("Thread %s: finishing", name)


def thread_func_algo2(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")
    face_off_thread = threading.Thread(target=thread_func_face_off, args=("face_off_thread",))
    algo2_thread = threading.Thread(target=thread_func_algo2, args=("algo2 thread",))
    logging.info("Main    : before running thread")
    face_off_thread.start()
    algo2_thread.start()
    logging.info("Main    : wait for the thread to finish")
    algo2_thread.join()
    face_off_thread.join()
    logging.info("Main    : all done")
