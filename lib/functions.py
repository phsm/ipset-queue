import sys
from socket import inet_pton, AF_INET, error
from subprocess import Popen, PIPE


def ipset_add(ipaddr):
    """
    First, check the IP address is a valid IPv4 one,
    Then, try to run "ipset add", if ipset exits with non-zero then
    drop a warning to the stderr
    """
    try:
        inet_pton(AF_INET, ipaddr)
    except error:
        sys.stderr.write(
            "The IP address supplied is invalid IPv4 one: \
            {}. Skipping\n".format(ipaddr)
        )
        return
    proc = Popen(
        ["/sbin/ipset", "add", "rq_whitelist", ipaddr],
        stdout=PIPE, stderr=PIPE
    )
    stdout, stderr = proc.communicate()
    if stdout or stderr:
        print(stdout, stderr)
