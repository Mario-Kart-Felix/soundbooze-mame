import subprocess

def query():

    def _winid():
        cmd = "xdotool search --pid `pgrep mame`"
        r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v = r.read()
        return hex(int(v.decode()))

    def _geometry(winid):
        cmd ='xdotool getwindowgeometry ' + winid
        r =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        v = r.read()
        return v.decode()

    w = _winid()
    g = _geometry(w)
    gs = g.split(' ')

    pos =  gs[4].split(',') 
    size = gs[9][:-1].split('x')

    x = int(pos[0]) - 10
    y = int(pos[1]) - 30

    width = int(size[0]) 
    height = int(size[1])

    return w, width, height, x, y
