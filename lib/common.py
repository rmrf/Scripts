import sys

def os_check():
    """ Support linux, sunos, macos
    """
    p = sys.platform
    os = None
    if 'linux' in p:
        os = 'linux'
    elif 'sunos' in p:
        os = 'solaris'
    elif 'darwin' in p:
        os = 'macos'
    else:
        print "Unsupported OS, only support linux, sunos, macos"
        exit(1)

    return os


def ping_cmd_choose(os, ipaddr):
    ping_cmd = None
    if os:
        if os == 'linux':
            ping_cmd = "/bin/ping -c %d %s " % (PING_COUNT, ipaddr)
        elif os == 'solaris':
            ping_cmd = "/usr/sbin/ping %s %d" % (ipaddr, PING_COUNT)
        elif os == 'macos':
            ping_cmd = "/sbin/ping -c %d %s" % (PING_COUNT, ipaddr)

    return ping_cmd


