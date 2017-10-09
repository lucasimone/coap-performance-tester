import logging
import os
from coap_performance_tester.commands import launch_sniffer, stop_sniffer

logger = logging.getLogger(__name__)

def start_coap_client(to=1000, arf=1.1, ret=1, resource='res1024'):

    logger.debug("Start CoAP with Timeout={0}, ACK_RAND_FACTOR ={1}, RETRANSMISSION = {2}, N. GET: {3}"
                 .format(to, float(arf), ret, 1))

    url = "%s/%s" % ('localhost:5683', resource)
    params = 'java  -jar ./coap_performance_tester/lib/m2m-coap-client-1.jar -r {0} -n {1} -t {2} -f {3} {4} '\
             .format(ret, 1, to, arf, url)
    os.system(params)


if __name__ == '__main__':
    launch_sniffer("demo.pcap", 'lo0 ', other_filter='udp port 5683')
    #start_coap_client()
    #stop_sniffer()

