import threading
import time
import keyboard


event = threading.Event()

def stop():
    event.set()
    print("stopped")

keyboard.add_hotkey("ctrl+f1", stop)

while not event.is_set():
