import time
import random
import threading

def main():
    threads = [
        threading.Thread(target=target, args=(f'T{i}',))
        for i in range(8)
    ]
    for t in threads:
        t.setDaemon(True)
        t.start()
    while True:
        time.sleep(10)
        print(f'Main thread, checking in...')
    

def target(name):
    print(f'Starting thread {name}')
    while True:
        time.sleep(30 * random.random())
        print(f'Thread {name}, checking in')
    
if __name__ == '__main__':
    main()
