from tester import GRAPH_RESULT, TEST_RESULT, ARF_STEP, NUM_TEST, DATA_PATH
from tester.commands import computeTime

def init_output_file(path = DATA_PATH, num_test=NUM_TEST):

    filename = "/".join([".", path, TEST_RESULT])
    with open(filename, "a") as fw:
        line = []
        line.append ( "COMPUTE PATH:%s with %d tests " %(path, num_test))
        line.append("\n\n")
        fw.writelines(" ".join(line))
        fw.close()


def write_test_result(index, res, timeout, rand_factor, retry, file_id, path=DATA_PATH, num_test=NUM_TEST):

    filename = "/".join([".", path, TEST_RESULT])
    avg_time, pdr, e2e, p_success = computeTime('%s.json' % file_id, num_test=num_test)

    with open(filename, "a") as fw:
        line = []
        line.append("\n")
        line.append("------ TEST n.{0}\n".format(index))
        line.append("|- FILENAME: {}\n".format(file_id))
        line.append("|- Resource :{}\n".format(res))
        line.append("|- Timeout:{0}\n".format(timeout))
        line.append("|- Acknowledgement Random Factor (ARF) :{0}\n".format(rand_factor))
        line.append("|- RT:{0}\n".format(retry))
        line.append("|- ITERATION:{0}\n".format(num_test))
        line.append("|- AVG_TIME:{0}\n".format(avg_time))
        line.append("|- PDrop:{0}\n".format(pdr))
        line.append("|- E2E:{0}\n".format(e2e))
        line.append("|- Prob SUCCESS: {0}\n".format(p_success))
        line.append("\n")
        fw.writelines(" ".join(line))
        fw.close()

    #get path



    write_greph_file(index, res, timeout, rand_factor, retry, avg_time, pdr, e2e, p_success, path)


def write_greph_file(index, res, timeout, rand_factor, retry, avg_time, pdr, e2e, p_success, path):
    """
    Create a file for plot the info
    :return:
    """
    filename = "/".join([".", path, GRAPH_RESULT])

    with open(filename, "a") as fw:
        line = []
        line.append("{0}".format(index))
        line.append("{0}".format(timeout))
        line.append("{0}".format(rand_factor))
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