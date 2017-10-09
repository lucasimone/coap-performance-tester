import time
from coap_performance_tester import *
from coap_performance_tester.commands import *
from coap_performance_tester.write_output import *

def start_coap_client(to=1000, arf=1.1, ret=1, resource=DEF_RES):

    logger.debug("Start CoAP with Timeout={0}, ACK_RAND_FACTOR ={1}, RETRANSMISSION = {2}, N. GET: {3}"
                 .format(to, float(arf), ret, NUM_TEST))

    url = "%s/%s" % (COAP_SERVER, resource)
    params = 'java  -jar ./coap_performance_tester/lib/m2m-coap-client-1.jar -r {0} -n {1} -t {2} -f {3} {4} '\
             .format(ret, NUM_TEST, to, arf, url)
    os.system(params)
    logger.debug(params)
    time.sleep(1)


if __name__ == '__main__':
    filename = "demo.pcap"
    launch_sniffer(filename, IFC, other_filter='')
    start_coap_client(to=1000, arf=1.5, ret=1, resource="res1024")
    stop_sniffer()
    decode_json(filename)