import json
import time
import argparse
import monitoring
import snort
import firewall
import static_defense


# if S --> snort / if M --> monitor(T with time)
def main():
    parser = argparse.ArgumentParser(description='ADD Attack Simulation.\
        Blue team Agent.')
    parser.add_argument('-B', help='Run basic check. \
        If want to run without any file, put N.', type=str, default=None)
    parser.add_argument('-L', help='Enable rsyslog. \
        Put N for disable rsyslog', type=str, default=None, choices=('Y', 'N'))
    parser.add_argument('-C', help='Change configuration file. \
        If want to run without any file, put N.', type=str, default=None)
    parser.add_argument('-S', help='Input Snort Rule file.',
                        type=str, default=None)
    parser.add_argument('-I', help='Snort Interface.',
                        type=str, default=None)
    parser.add_argument('-M', help='Input Monitoring file list.',
                        type=str, default=None)
    parser.add_argument('-T', help='Start time of monitoring.',
                        type=int, default=None)
    parser.add_argument('-F', help='ADD iptable rule file.' ,
                        type=str, default=None)
    args = parser.parse_args()

    sd = static_defense.StaticDefense()
    if args.B is not None:
        if args.B == "N":
            sd.basic_check()
        else:
            sd.basic_check(args.B)

    if args.L == "Y":
        sd.enable_log()
    elif args.L == "N":
        command = "sudo service rsyslog stop"
        sd._cmd_run(command)

    if args.C is not None:
        if args.C == "N":
            sd.change_file()
        else:
            sd.change_file(args.C)

    sn = snort.Snort()
    if (args.S is not None) and (args.I is not None):
        if args.S != "N":
            sn.add_snort_rule(args.S)
        sn.snort_start(args.I)

    mr = monitoring.Monitor()
    if args.M is not None:
        with open(args.M, 'r') as file:
            data = json.load(file)
        files = data["files"]
        mr.file_hash(files)

        if args.T is None:
            t = int(time.time())
            while(1):
                mr.monitoring(files, t)
                time.sleep(30)
        else:
            while(1):
                mr.monitoring(files, args.T)
                time.sleep(30)

    fw = firewall.Firewall()
    if args.F is not None:
        if args.F != "N":
            fw.add_firewall_rule(args.F)
        else:
            fw.add_firewall_rule()


if __name__ == "__main__":

    main()
