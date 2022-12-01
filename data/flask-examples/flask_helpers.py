import os, sys, time, threading, subprocess, contextlib

def output_thread(proc):
    for line in proc.stdout:
        print(line.decode('utf-8'), end='')
    print('Exiting output thread')

def run_flask_app(app_name):
    proc = subprocess.Popen(
        # [sys.executable, 'flask', 'run'],
        ['flask', 'run', '--no-reload'],
        env={
            **os.environ, 
            'FLASK_APP': app_name,
            'FLASK_ENV': 'development',
        },
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    # Wait for the port to bind
    for line in proc.stdout:
        line = line.decode('utf-8')
        print(line, end='')
        if ' * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)' in line:
            break
    else:
        print('== Error starting server ==')
        return None
    thd = threading.Thread(target=output_thread, args=(proc,))
    thd.setDaemon(True)
    thd.start()
    return proc


@contextlib.contextmanager
def running_app(app_name):
    proc = run_flask_app(app_name)
    try:
        yield proc
    finally:
        proc.kill()        
