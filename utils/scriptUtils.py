import time

def repeat_script(callback, interval=0.5):
    """Recibe un script y un intervalo en ms, repetirá dicho script de manera infinita dejando una pausa entre cada repetición """
    while True:
        callback()
        time.sleep(interval)