from tester import GRAPH_RESULT, TEST_RESULT, ARF_STEP, NUM_TEST
from tester.commands import computeTime

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


def write_test_result(index, res, timeout, rand_factor, retry, file_id):


    avg_time, pdr, e2e, p_success = computeTime('%s.json' % file_id)

    with open(TEST_RESULT, "a") as fw:
        line = []
        line.append("TEST.{0}".format(index))
        line.append("RES:{}".format(res))
        line.append("TO:{0}".format(timeout))
        line.append("ARF:{0}".format(rand_factor * ARF_STEP))
        line.append("RT:{0}".format(retry))
        line.append("ITERATION:{0}".format(NUM_TEST))
        line.append("AVG_TIME:{0}".format(avg_time))
        line.append("PDrop:{0}".format(pdr))
        line.append("E2E:{0}".format(e2e))
        line.append("P_SUCCESS:{0}".format(p_success))
        line.append("\n")
        fw.writelines(" ".join(line))
        fw.close()

    # Write Also graph file with the same data
    write_greph_file(index, res, timeout, rand_factor, retry, avg_time, pdr, e2e, p_success)


def write_greph_file(index, res, timeout, rand_factor, retry, avg_time, pdr, e2e, p_success):
    """
    Create a file for plot the info
    :return:
    """
    with open(GRAPH_RESULT, "a") as fw:
        line = []
        line.append("{0}".format(index))
        line.append("{0}".format(timeout))
        line.append("{0}".format(rand_factor * ARF_STEP))
        line.append("{0}".format(retry))
        line.append("{0}".format(NUM_TEST))
        line.append("{0}".format(avg_time))
        line.append("{0}".format(pdr))
        line.append("{0}".format(e2e))
        line.append("{0}".format(p_success))
        line.append("{0}".format(res))
        line.append("\n")
        fw.writelines("\t".join(line))
        fw.close()