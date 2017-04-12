#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import logging
import json

from tester import NUM_TEST

# init logging to stnd output and log files
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
logger.addHandler(sh)
logger.propagate = True


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
        elif what == 'coap.type':
            return pkt["_source"]['layers']['coap']['coap.type']
        else:
            raise Exception("{0} is not a valid parameter".format(what))
    except:
        logger.error("Error while parsing json conversation")
        raise Exception("Error while parsing json conversation")


def computeTime(json_file) -> (float, int):
    with open(json_file) as file:
        pkts = json.load(file)
        file.close()

    count_ack = 0
    mids = dict()
    wrong_pkts = 0
    for pkt in pkts:
        frame_id = extract_field(pkt, 'frame_id')
        if 'coap' in  pkt["_source"]['layers']:
            con_type  = int(extract_field(pkt, 'coap.type'))
            time = extract_field(pkt, 'time_delta_displayed')
            mid  = extract_field(pkt, 'coap.mid')
            if mid not in mids.keys():
                mids[mid] = []
            mids[mid].append(float(time))

            if con_type == 2 :
               con_type += 1
        else:
            wrong_pkts += 1
            logger.debug("SKIP packet frame id {0} because it is not a coap message".format(frame_id))

    con_time = []
    for mid, v in mids.items():
        con_time.append(sum(v) - v[0])

    try:
        t0 = float(extract_field( pkts[0], 'time_epoch'))
        tf = float(extract_field( pkts[len(pkts)-1], 'time_epoch'))
        e2e = tf - t0
    except:
        logger.error("Unable to read the packets")

    p_success = (con_type/NUM_TEST) * 100
    avarage = sum(con_time)/len(con_time)
    logger.info ("Avarage time: %f" % avarage)
    n_cons = len(pkts) - wrong_pkts
    expeted_cons = NUM_TEST *2 # with ACK
    pdr = (n_cons - expeted_cons)/expeted_cons * 100
    return (avarage, pdr, e2e, p_success)

