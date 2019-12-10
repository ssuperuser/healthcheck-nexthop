import os
import sys
import subprocess
import ipaddress


arg_names = ['command', 'ip', 'interface']
args = dict(zip(arg_names, sys.argv))

ip = args.get('ip')
# below we define that default iface is "lo"
if args.get('interface'):  # if is provided as a second argument
    interface = args.get('interface')
else:
    interface = "lo"


# Return the appropriate version number: 4 for IPv4, 6 for IPv6.
def ip_ver(ip_unknown_version):
    return ipaddress.ip_address(ip_unknown_version).version


def is_reachable(**kwargs):
    with open(os.devnull, "wb") as limbo:
        if ip_ver(ip) == 4:
            result = subprocess.Popen(["ping", "-c", "2", ip, "-I", interface, "-W 1", "-i 0.01"], stdout=limbo,
                                      stderr=limbo).wait()
            return result
        elif ip_ver(ip) == 6:
            result = subprocess.Popen(["ping6", "-c", "2", ip, "-I", interface, "-W 1", "-i 0.01"], stdout=limbo,
                                      stderr=limbo).wait()
            return result
        else:
            exit(1)


if is_reachable(ip=ip, interface=interface) == 0:
    print("alive")
elif is_reachable(ip=ip, interface=interface) == 0:
    print("alive")
else:
    print("dead")

exit(0)
