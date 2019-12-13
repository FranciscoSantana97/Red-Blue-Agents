import sys
import os


class Snort():
    # install snort
    # def install_snort():
    #   command = "sudo sh " + os.getcwd() + "/install/install_snort.sh"
    #   if (os.system("%s" % (command)) != 0):
    #       print("Installing Snort Failed......")
    #       sys.exit()
    #   else:
    #       print("Snort Installed")

    # start snort
    def snort_start(self, interface_name):
        command = "snort -A console -i " + str(interface_name) + " -c /etc/snort/snort.conf"
        if (os.system("sudo gnome-terminal -- bash -c '%s'" % (command)) != 0):
            print("Starting Snort Failed......")
            sys.exit()
        else:
            print("Snort Started")

    # add some snort rules from USER RULE FILE
    def add_snort_rule(self, rule_file_path):
        with open("/etc/snort/rules/local.rules", 'a+') as file:
            with open(rule_file_path, 'r') as rfile:
                for line in rfile:
                    file.write(line)
