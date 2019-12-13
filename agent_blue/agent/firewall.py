import sys
import os


class Firewall():
    def add_firewall_rule(self, json_file=None):

        command = "sudo iptables -F"
        p = os.system("%s" % (command))
        command = "sudo iptables -P INPUT ACCEPT"
        p = os.system("%s" % (command))
        command = "sudo iptables -P OUTPUT ACCEPT"
        p = os.system("%s" % (command))
        command = "sudo iptables -P FORWARD ACCEPT"
        p = os.system("%s" % (command))

        command = "sudo iptables -A OUTPUT -m string --string 'nc.traditional' --algo kmp -j DROP"
        p = os.system("%s" % (command))
        command = "sudo iptables -A INPUT -m string --string 'nc.traditional' --algo kmp -j DROP"
        p = os.system("%s" % (command))
        command = "sudo iptables -A OUTPUT -m string --string '-e /bin/bash' --algo kmp -j DROP"
        p = os.system("%s" % (command))
        command = "sudo iptables -A INPUT -m string --string '-e /bin/bash' --algo kmp -j DROP"
        p = os.system("%s" % (command))
        
        if(json_file is not None):
            with open(json_file, 'r') as file:
                data = json.load(file)
                for command in data["commands"]:
                    p = os.system("%s" % (command))

