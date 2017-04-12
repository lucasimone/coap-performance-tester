import errno
import time
from tester import *
from tester.commands import *


def start_coap_client(to=1000, arf=1.1, ret=1):
    global logger
    logger.debug("Start CoAP with Timeout={0}, ACK_RAND_FACTOR ={1}, RETRANSMISSION = {2}, N. GET: {3}"
                 .format(to, float(arf), ret, NUM_TEST))

    params = 'java  -jar ./tester/lib/m2m-coap-client-1.jar -r {0} -n {1} -t {2} -f {3} {4} '\
             .format(ret, NUM_TEST, to, arf, URL)
    os.system(params)



if __name__ == '__main__':


    if os.path.exists(DATADIR):
        os.rename(DATADIR, ('_').join([DATADIR, str(time.time())]))

    # generate dirs
    for d in TMPDIR, DATADIR, LOGDIR:
        try:
            os.makedirs(d)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise






    logger.debug("START TEST...")
    index = 0
    for timeout_variance in range(TIMEOUT_MIN, TIMEOUT_MAX, TIMEOUT_STEP):
        for rand_factor_variance in range(ARF_MIN, ARF_MAX):
            for retry_variance in range(RETRY_MIN, RETRY_MAX):

                file_id = ('_'.join([FILENAME,
                                    "to",
                                    str(timeout_variance),
                                    "arf",
                                    str(rand_factor_variance),
                                    "r",
                                    str(retry_variance),
                                    ]))
                file_name = '%s.pcap' % file_id
                launch_sniffer(file_name, IFC, other_filter='udp port 5683')
                start_coap_client(to=timeout_variance, arf=rand_factor_variance*ARF_STEP, ret=retry_variance)
                stop_sniffer()
                decode_json(file_name)
                avg_time, pdr, e2e = computeTime('%s.json'%file_id)
                with open(TEST_RESULT, "a") as fw:
                    fw.writelines(
                        "TEST.{0} TO:{1} ARF:{2} RT:{3} ITERATION:{4} AVG_TIME:{5} PDR:{6} E2E:{7}\n"
                            .format(index, timeout_variance, rand_factor_variance * ARF_STEP,
                            retry_variance, NUM_TEST, avg_time, pdr, e2e))
                    fw.close()

                index+=1
    logger.debug("TEST is over!")