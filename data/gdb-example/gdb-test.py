import time
import threading

def main():
    threads = [threading.Thread(target=t1), threading.Thread(target=t2)]
    for t in threads:
        t.start()

def t1():
    while True:
        print('In thread 1')
        time.sleep(10)


def t2():
    while True:
        print('In thread 2')
        time.sleep(10)


if __name__ == '__main__':
        main()