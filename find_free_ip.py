#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" find_free_ip.py ipaddr

    provide ip address, then script find free ip address which can be used
    within this subnet.

Author: ryan.qian@gmail.com
"""

import os
import sys
import ipcalc
import socket
import threading
import subprocess
from lib.common import os_check, ping_cmd_choose
from time import sleep

PING_COUNT = 3
non_pingable_ips = []
non_reolvable_ips = []


def usage():
    print
    print "Usage: find_free_ip.py <ip address>/<netmask> "
    print
    print "\t default netmask is 255.255.255.0 if not indicate"
    print "\t can also use 24, 21 as netmask "
    print


def do_ping(ping_cmd, ipaddr):
    """ Return True if pingable
    """
    result = True
    ping_result = 1
    try:
        ping_result = subprocess.check_call(
            ping_cmd, shell=True, stdout=subprocess.PIPE)
    except:
        pass

    if ping_result != 0:
        result = False
        non_pingable_ips.append(ipaddr)

    return result


def reverse_check(ipaddr):
    hostname = None
    try:
        hostname = socket.gethostbyaddr(ipaddr)[0]
    except:
        pass

    if hostname:
        return True
    else:
        non_reolvable_ips.append(ipaddr)
        return False


def calculate_network(tgt_ipaddr):
    all_ips = []
    if '/' in tgt_ipaddr:
        ip, netmask = tgt_ipaddr.split('/')
        if not netmask:
            netmask = '255.255.255.0'
    else:
        ip = tgt_ipaddr
        netmask = '255.255.255.0'
    ip_net = "%s/%s" % (ip, netmask)
    subnet = ipcalc.Network(ip_net)
    for i in subnet:
        all_ips.append(str(i))

    return all_ips


def main():
    if len(sys.argv) != 2:
        usage()
        exit(1)

    tgt_ipaddr = sys.argv[1]
    os = os_check()
    all_ips = calculate_network(tgt_ipaddr)

    t_ping_list = []
    t_reverse_list = []

    for ip in all_ips:
        ping_cmd = ping_cmd_choose(os, ip)
        # print ping_cmd
        t_ping = threading.Thread(target=do_ping, args=(ping_cmd, ip))
        t_ping_list.append(t_ping)

        t_reverse = threading.Thread(target=reverse_check, args=[ip])
        t_reverse_list.append(t_reverse)

    for thread in t_ping_list:
            thread.start()
    for thread in t_ping_list:
            thread.join()

    for thread in t_reverse_list:
            thread.start()
    for thread in t_reverse_list:
            thread.join()

    # print "Unpingable ip address:", non_pingable_ips
    # print "UnResolvable ip address:", non_reolvable_ips

    free_ips = list(set(non_pingable_ips) & set(non_reolvable_ips))
    print "Free IPs inside network %s are:" % tgt_ipaddr
    for i in sorted(free_ips, key=lambda item: socket.inet_aton(item)):
        print i


if __name__ == '__main__':
    main()
