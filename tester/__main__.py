import errno
import time
from tester import *
from tester.commands import *
from tester.write_output import *

logger = logging.getLogger(__name__)


def start_coap_client(to=1000, arf=1.1, ret=1, resource=DEF_RES):

    logger.debug("Start CoAP with Timeout={0}, ACK_RAND_FACTOR ={1}, RETRANSMISSION = {2}, N. GET: {3}"
                 .format(to, float(arf), ret, NUM_TEST))

    url = "%s/%s" % (COAP_SERVER, resource)
    params = 'java  -jar ./tester/lib/m2m-coap-client-1.jar -r {0} -n {1} -t {2} -b {3} -f {4} {5} '\
             .format(ret, NUM_TEST, to, BLOCK_SIZE, -arf, url)
    os.system(params)
    logger.debug(params)
    time.sleep(1)


def execute_con_requests(i, timeout, rand_fact, retry, res):
    """
    FIXED those parameters the COAP Client is called to send NUM_TEST CON to COAP_SERVER.
    :param timeout:
    :param rand_fact:
    :param retry:
    :param res: this is the resource to query on the CoAP Server
    :return: ---
    """
    file_id = ('_'.join([FILENAME,
                         "to",
                         str(timeout),
                         "arf",
                         str(rand_fact),
                         "r",
                         str(retry),
                         str(res)
                         ]))
    file_name = '%s.pcap' % file_id
    launch_sniffer(file_name, IFC, other_filter='udp port 5683')
    start_coap_client(to=timeout, arf=rand_fact * ARF_STEP, ret=retry, resource=res)
    stop_sniffer()
    decode_json(file_name)
    write_test_result(i, res=res, timeout=timeout, rand_factor=rand_fact, retry=retry, file_id=file_id)



if __name__ == '__main__':

    if os.path.exists(DATADIR):
        os.rename(DATADIR, '_'.join([DATADIR, str(time.time())]))

    # generate dirs
    for d in TMPDIR, DATADIR, LOGDIR:
        try:
            os.makedirs(d)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    init_output_file()  # INIT FILE

    logger.debug("#####  START TEST  #######")
    index = 0

    for res in RES_LIST:
        rand_factor_variance = ARF_MIN
        for timeout_variance in range(TIMEOUT_MIN, TIMEOUT_MAX+TIMEOUT_STEP, TIMEOUT_STEP):
            for retry_variance in range(RETRY_MIN, RETRY_MAX+1):
                execute_con_requests(index,
                                     timeout=timeout_variance,
                                     rand_fact=rand_factor_variance,
                                     retry=retry_variance,
                                     res=res)

                index += 1
            rand_factor_variance += (ARF_STEP*10)

    logger.debug(">>>>>> TES IS OVER <<<<<<<<")
