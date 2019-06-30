import time
from pynput.keyboard import Key, Listener

attr = ['char', 'up', 'down', 'left', 'right']

def on_press(key):

    if hasattr(key, attr[0]):
        print time.time(), 0, key.char

    elif hasattr(key, attr[1]) or hasattr(key, attr[2]) or hasattr(key, attr[3]) or hasattr(key, attr[4]):
        k = ('{0}'.format(key))
        z = k.split('.')
        print time.time(), 0, z[1]

def on_release(key):

    if hasattr(key, attr[0]):
        print time.time(), 1, key.char

    elif hasattr(key, attr[1]) or hasattr(key, attr[2]) or hasattr(key, attr[3]) or hasattr(key, attr[4]):
        k = ('{0}'.format(key))
        z = k.split('.')
        print time.time(), 1, z[1]

    if key == Key.esc:
        return False

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
