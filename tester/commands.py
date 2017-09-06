#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import logging
import json

from tester import NUM_TEST, GRAPH_RESULT

# init logging to stnd output and log files
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.propagate = True


def init_output_file():

    with open(GRAPH_RESULT, "a") as fw:
        line = []
        line.append("#TEST")
        line.append("RESOURCE")
        line.append("TO")
        line.append("ARF")
        line.append("RT")
        line.append("N.GET")
        line.append("AVG_TIME")
        line.append("PDrop")
        line.append("E2E")
        line.append("P_SUCCESS")
        line.append("\t")
        fw.writelines(" ".join(line))
        fw.close()


def launch_sniffer(filename, filter_if, other_filter=None):
    logger.info('Launching packet capture..')

    if other_filter is None:
        other_filter = ''

    if (filter_if is None ) or (filter_if == ''):
        sys_type = platform.system()
        if sys_type == 'Darwin':
            filter_if = 'lo0'
        else:
            filter_if = 'lo'
            # TODO windows?

    # lets try to remove the filename in case there's a previous execution of the TC
    try:
        params = 'rm ' + filename
        os.system(params)
    except:
        pass

    params = 'tcpdump -K -i ' + filter_if + ' -s 200 ' + '  -w ' + filename + ' ' + other_filter + ' &'
    os.system(params)
    logger.info('Creating process tcpdump with: %s' % params)

    # TODO we need to catch tcpdump: <<tun0: No such device exists>> from stderr

    return True


def decode_json(filename):

    logger.info('Execute TSHARK to dissect as JSON file')
    json_filename = os.path.splitext(filename)[0] + '.json'

    params = 'tshark -r {0} -l -n -x -T json > {1}'.format(filename, json_filename)
    os.system(params)
    logger.info('Dissect PCAP as JSON using this command: %s' % params)
    return True


def stop_sniffer():
    proc = subprocess.Popen(["pkill", "-INT", "tcpdump"], stdout=subprocess.PIPE)
    proc.wait()
    logger.info('Packet capture stopped')
    return True

def stop_sniffer_with(filename):
    ps_line = os.popen("ps -alx | grep tcpdump | grep [{0}]{1}".format(filename[0], filename[1:])).read()
    if ps_line:
        pid = ps_line.split()[0]
        print(ps_line, pid)
        #proc = subprocess.Popen(["kill", "-INT", pid], stdout=subprocess.PIPE)
        #proc.wait()
        #os.killpg(os.getpgid(int(pid)), signal.SIGTERM)
        logger.info('Packet capture stopped')



def extract_payload(pkt) -> str:

    protocol = pkt["_source"]['layers']['frame']['frame.protocols']
    payload = ""
    if 'coap' in protocol:
        coap = pkt["_source"]['layers']['coap']
        if 'coap.payload' in coap:
            # logging.debug("Frame n. {0} - {2} - SIZE:{1} bytes - IPv6:{3} - TIMESTAMP: {4}"
            #              .format(frame_id, pkt_size, protocol, ipv6, timestamp))
            if 'data-text-lines' in coap['coap.payload']:
                payload = coap['coap.payload']['data-text-lines']
                # logging.debug("PAYLOAD ===> {0}".format(coap['coap.payload']['data-text-lines']))
            else:
                # logging.debug("PAYLOAD ===> {0}".format(coap['coap.payload']))
                payload = coap['coap.payload']
    return str(payload)


def extract_field(pkt, what) -> str:
    try:
        if what == 'frame_id':
            return pkt["_source"]['layers']['frame']['frame.number']
        elif what == 'time_epoch':
            return pkt["_source"]['layers']['frame']['frame.time_epoch']
        elif what == 'time_delta_displayed':
            return pkt["_source"]['layers']['frame']['frame.time_delta_displayed']
        elif what == 'pkt_size':
            return pkt["_source"]['layers']['frame']['frame.len']
        elif what == 'protocol':
            return pkt["_source"]['layers']['frame']['frame.protocols']
        elif what == 'payload':
            return extract_payload(pkt)
        elif what == 'coap_payload_size':
            #print(">>>> " + pkt["_source"]['layers']['coap']['coap.payload'])
            return pkt["_source"]['layers']['coap']['coap.payload'].split(",")[1].split(":")[1]
        elif what == 'timestamp':
            return pkt["_source"]['layers']['frame']['frame.time']
        elif what == 'src':
            return pkt["_source"]['layers']['ipv6']['ipv6.src']
        elif what == 'dst':
            return pkt["_source"]['layers']['ipv6']['ipv6.dst']
        elif what =='ipv6':
            return pkt["_source"]['layers']['ipv6']['ipv6.addr']
        elif what == 'coap.mid':
            return pkt["_source"]['layers']['coap']['coap.mid']
        elif what == 'coap.token':
            return pkt["_source"]['layers']['coap']['coap.token']
        elif what == 'coap.res':
            return pkt["_source"]['layers']['coap']['coap.opt.uri_path']
        elif what == 'coap.type':
            return pkt["_source"]['layers']['coap']['coap.type']
        else:
            raise Exception("{0} is not a valid parameter".format(what))
    except:
        logger.error("Error while parsing json conversation")
        raise Exception("Error while parsing json conversation")


def computeTime(json_file, num_test=NUM_TEST) -> (float, int):
    with open(json_file) as file:
        pkts = json.load(file)
        file.close()


    payload_size = 0
    old_token = ""
    old_mid = ""
    wait_for_final_ack = False
    coap_msg_lost = 0
    coap_msg_success = 0
    initial_time = 0
    final_time = 0
    e2e_full_payload = []
    wrong_pkts  = 0
    pkt_index   = 0
    total_size  = 0
    ack_size = 0
    for pkt in pkts:

        frame_id = extract_field(pkt, 'frame_id')
        size = int(extract_field(pkt, 'pkt_size'))

        if 'coap' in  pkt["_source"]['layers']:
            pkt_index += 1
            total_size += size  # TOTAL AMOUNT OF DATA TRANSMITTED IN A COAP COMMUNICATION
            coap_type = int(extract_field(pkt, 'coap.type'))
            mid = extract_field(pkt, 'coap.mid')
            token = extract_field(pkt, 'coap.token')
            epoch_time = float(extract_field(pkt, 'time_epoch'))

            if coap_type == 0:  # CON MESSAGE

                # CASE 1: RETRANSMISSION because the MID and TOKEN are the same
                if token == old_token and mid == old_mid:
                    logger.debug("-- Packet n. {2} Retransmission Mid:{0}, Token:{1} - TIME_MS:{3}".format(mid, token, pkt_index, epoch_time))

                # Case 2: PAYLOAD FRAGMENTATION: New MID but same TOKEN
                elif token == old_token:
                    logger.debug("-- Packet n. {2} Payload Fragmented MID:{0}, Token:{1}".format(mid, token, pkt_index))

                # Case 3: New Conversation - New MID, new TOKEN
                else:
                    logger.debug("-------------------")
                    # Case 3.1 - if we are waiting a ACK this means that we have lost the ACK
                    if wait_for_final_ack:
                        coap_msg_lost += 1
                        final_time = epoch_time
                        logger.debug("PACKET n. {0} didn't get ACK - Packet lost :(".format(pkt_index-1))
                    # Case 3.2 - A new message and before everything was acknowledged.
                    else:
                        coap_msg_success += 1
                        logger.debug("PACKET n. {0} get ACK - Packet SUCCESS !!! ".format(pkt_index-1))
                        # Since is a successful delivery we add the amount of size at the total payload sent
                        payload_size += ack_size

                    e2e = final_time - initial_time     # TIME to SUCCESSFULLY (or NOT) TRANSFER a FULL PAYLOAD
                    e2e_full_payload.append(e2e)
                    logger.debug("PACKET n. {1} E2E Latency is {0}  [{2} - {3}]".format(e2e, pkt_index-1, final_time, initial_time))
                    ack_size = 0
                    initial_time = epoch_time  # START TIME
                    logger.debug("-------------------")
                    logger.debug("-- Packet n. {2} New Request    MID:{0}, Token:{1} - T_START:{3}"
                                 .format(mid, token, pkt_index, initial_time))

                # As a new CON we need to RESET each COUNTER
                wait_for_final_ack = True   # we need to get another ACK for this CON
                old_token = token
                old_mid = mid

            elif coap_type == 2:  # ACK MESSAGE

                # MID and TOKEN should match the ACK otherwise there is a error on the flow
                # since everything is sequential.
                if token == old_token:
                    final_time = epoch_time
                    wait_for_final_ack = False
                    ack_size += int(extract_field(pkt, 'coap_payload_size'))
                else:
                    logger.error("This situation is IMPOSSIBLE!")

        # NOT a CoAP message - SKIP IT
        else:
            wrong_pkts += 1
            logger.debug("SKIP packet frame id {0} because it is not a coap message".format(frame_id))

    p_success = coap_msg_success / (coap_msg_lost+coap_msg_success) * 100
    average = sum(e2e_full_payload) / (coap_msg_lost+coap_msg_success)

    efficency = payload_size * 1.0 / total_size
    logger.info(" #################################### ")
    logger.info(" Summary RESULT")
    logger.info(" #################################### ")
    logger.info(" ")
    logger.info(" N. of packets sent are     : {0}".format(coap_msg_lost+coap_msg_success))
    logger.info(" N. of packets TRANSMITTED  : {0}".format(coap_msg_success))
    logger.info(" N. of packets LOST         : {0}".format(coap_msg_lost))
    logger.info(" Average Latency time (e2e) : {0}".format(average))
    logger.info(" Total Data transmitted     : {0}".format(total_size))
    logger.info(" Total Payload transmitted  : {0}".format(payload_size))
    logger.info(" Efficiency (Payload/SIZE)  : {0}".format(efficency))
    logger.info(" Success probability        : {0}".format(p_success))
    logger.info(" OTHER PACKETS probability  : {0}".format(wrong_pkts))

    return average, efficency, 0, p_success, coap_msg_success, coap_msg_lost




if __name__ == '__main__':
    computeTime("../data/coap-tester-10.0_blocksize/70a/capture_to_1200_arf_12_r_4_res128.json", 500)