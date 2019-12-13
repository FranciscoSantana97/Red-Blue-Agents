#/usr/bin/env python
import sys, json

misudo = []

def save_state(interface, state):
    with open(interface, "w") as f:
        f.write(json.dumps(state))

def is_sudofind(src):
    keyword1 = "(root)"
    keyword2 = "NOPASSWD:"
    keyword3 = "/usr/bin/find"

    src = src.strip()
    if not src.startswith(keyword1):
        return False

    src = src[len(keyword1):].strip()
    if not src.startswith(keyword2):
        return False

    src = src[len(keyword2):].strip()
    src = src.split(",")
    for i in range(0, len(src)):
        src[i] = src[i].strip()

    if not keyword3 in src:
        return False

    return True

interface = sys.argv[1]
sudo = ""
sudofind = False

with open(interface, "r") as f:
    state = json.load(f)
    sudo = state["sudo"]

lines = sudo.split("\n")
for line in lines:
    line = line.strip()

    if is_sudofind(line) and not sudofind:
        sudofind = True
        misudo.append("sudofind")

if len(misudo) != 0:
    state["misudo"] = misudo
    print ("SAVE!!!")
else:
    print ("NOT SAVE!!!")

del state["sudo"]
save_state(interface, state)

