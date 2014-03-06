#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Ping With Pictures
    Usage:

    pingp.py ipaddr1 <ipaddr2> <ipaddr3> <-s>

    scritp will try to use system ping command to ping target ipaddres
    and use the ping response time draw plot, if multi ipaddress givent
    will overprint them in one picture

Author: ryan.qian@gmail.com
"""

import re
import os
import sys
import threading
import subprocess
from lib.common import os_check, ping_cmd_choose
import matplotlib.pyplot as plt
import prettyplotlib as ppl

thread_list = []
ping_results = {}

def usage():
    print
    print "Usage: pingp.py ipaddr1 <ipaddr2> <ipaddr3> <-s>"
    print
    print "\t At least proivde one target ipaddress to ping"
    print "\t -s to silent the ping output. "
    print


def multi_ping(ping_cmd, targets, verbose):
    for i in targets:
        ping_results[i] = []
        t = threading.Thread(target=do_ping, args=(ping_cmd, i, verbose))
        thread_list.append(t)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        try:
            thread.join()
        except (KeyboardInterrupt, SystemExit):
            print '\n! Received keyboard interrupt, quitting threads.\n'
            #pass


def do_ping(ping_cmd, ipaddr, verbose):

    ping_cmd = ping_cmd.split()
    ping_cmd.append(ipaddr)
    #print len(ipaddr)
    #print ping_cmd
    sub = subprocess.Popen(ping_cmd,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    pattern = '.*time=([0-9\.]*) ms'
    try:
        while True:
            line = sub.stdout.readline()
            #TODO
            #print 'Raw line', line
            if line.startswith('64'):
                if verbose:
                    print line.rstrip()
                m = re.findall(pattern, line)
                if m:
                    ping_results[ipaddr].append(m[0])
                else:
                    ping_results[ipaddr].append('0')
            elif line == '':
                break
            else:
                continue
    except KeyboardInterrupt:
        sub.terminate()
    finally:
        sub.terminate()


def new_make_plot(out_fn):
    fig, ax = plt.subplots(1)

    for k in ping_results.keys():
        x_data = []
        y_data = []
        for i, resp_time in enumerate(ping_results[k]):
            x_data.append(i)
            y_data.append(resp_time)

        ppl.plot(ax, x_data, y_data, label=k, linewidth=0.75)

    ppl.legend(ax)
    #ax.set_title('test')
    fig.savefig(out_fn)

    print "Saved to file: %s" % out_fn



def main():
    os_name = os_check()
    #if os_name != 'linux':
        #print "Exit, This script can only run on Linux"
        #sys.exit(1)

    targets = sys.argv[1:]
    if len(targets) < 1:
        usage()
        sys.exit(1)

    multi_ping('ping', targets, 1)

    #print ping_results

    if ping_results != {}:
        new_make_plot('/tmp/o.png')


if __name__ == '__main__':
    main()
