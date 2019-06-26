import sys
import signal
import os
import jack
import threading
import numpy as np

import vamp
import librosa
from sklearn.preprocessing import MinMaxScaler
from scipy.signal import find_peaks

from ryu import *

ryu = RYU()

if sys.version_info < (3, 0):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
else:
    pass

argv = iter(sys.argv)
defaultclientname = os.path.splitext(os.path.basename(next(argv)))[0]
clientname = next(argv, defaultclientname)
servername = next(argv, None)

client = jack.Client(clientname, servername=servername)

if client.status.server_started:
    print("JACK server started")
if client.status.name_not_unique:
    print("unique name {0!r} assigned".format(client.name))

event = threading.Event()

def loudness (buff, sr):
    data = vamp.collect(buff, sr, "vamp-libxtract:loudness")
    vector = data['vector']
    L = vector[1]
    return L

def stft(buff, sr):

    maxDominant = 3
    dominant5 = []

    STFT = librosa.feature.chroma_stft(y=buff, hop_length=64, sr=sr, n_chroma=12, n_fft=1024)
    rowsum = np.sum(STFT, axis=1)
    sortsum = sorted(rowsum, reverse=True)

    for i in range(0, maxDominant):
        A = np.where(rowsum == sortsum[i])
        for a in A:
            dominant5.append(int(a[0]))

    print dominant5
    return dominant5

@client.set_process_callback
def process(frames):
    global ryu

    assert len(client.inports) == len(client.outports)
    assert frames == client.blocksize
    for i, o in zip(client.inports, client.outports):
        o.get_buffer()[:] = z = i.get_buffer()
        buff = np.frombuffer(z, dtype=np.float32)

        l = loudness(buff, client.samplerate)
        if l > 1.8:
           s = stft(buff, client.samplerate)
           action = s[0] + s[1] + s[2]
           print action

           if action == 0:
               ryu.left()
           elif action == 1:
               ryu.right()
           elif action == 2:
               ryu.jumpleft()
           elif action == 3:
               ryu.jumpright()
               ryu.superpunch(0)
               ryu.superpunch(1)
           elif action == 4:
               ryu.jumpup()
           elif action == 5:
               ryu.defenddown(0)
               ryu.fire(0)
               ryu.fire(1)
           elif action == 6:
               ryu.defendup(0)
           elif action == 7:
               ryu.defenddown(1)
           elif action == 8:
               ryu.defendup(1)
           elif action == 9:
               ryu.downkick()
               ryu.kick()
               ryu.superkick(0)
               ryu.superkick(1)
           elif action == 10:
               ryu.kick()
               ryu.superkick(0)
               ryu.superkick(1)
           elif action == 11:
               ryu.punch()
               ryu.fire(0)
               ryu.fire(1)
           else:
               ryu.superpunch(0)
               ryu.superpunch(1)

@client.set_shutdown_callback
def shutdown(status, reason):
    print("JACK shutdown!")
    print("status:", status)
    print("reason:", reason)
    event.set()

for number in 1, 2:
    client.inports.register("input_{0}".format(number))
    client.outports.register("output_{0}".format(number))

with client:

    capture = client.get_ports(is_physical=True, is_output=True)
    if not capture:
        raise RuntimeError("No physical capture ports")

    for src, dest in zip(capture, client.inports):
        client.connect(src, dest)

    playback = client.get_ports(is_physical=True, is_input=True)
    if not playback:
        raise RuntimeError("No physical playback ports")

    #for src, dest in zip(client.outports, playback):
    #    client.connect(src, dest)

    try:
        event.wait()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
