#/usr/bin/env python
import subprocess, sys, json, os
import xml.etree.ElementTree as elemTree

TEMP = "temp_nfsop"

def save_state(interface, state):
    with open(interface, "w") as f:
        f.write(json.dumps(state))

def parse_report(src):
    tree = elemTree.parse(src)
    root = tree.getroot()

    host = root.find("host")
    os = host.find("os")
    osmatch = os.find("osmatch")
    osclass = osmatch.find("osclass")
    os = osclass.attrib["osfamily"].lower()

    ports = host.find("ports")
    port = ports.findall("port")
    temps = []
    for e in port:
        temps.append((e.attrib["protocol"].lower(), e.attrib["portid"]))
    ports = temps

    return (os, ports)

interface = sys.argv[1]
ip = None
state = None
with open(interface, "r") as f:
    state = json.load(f)
    ip = state["address"]

try:
    sys, ports = parse_report(TEMP)
except:
    try:
        p = subprocess.Popen(["sudo", "nmap", ip, "-sV", "-p", "1-9999", "-O", "-oX", TEMP ])
        p.communicate()
    except OSError:
        state["error"] = "not found nmap"
        save_state(interface, state)
        sys.exit(0)
    sys, ports = parse_report(TEMP)

state["os"] = sys
state["ports"] = ports

save_state(interface, state)
