_last_capture = None


TIMEOUT_MIN = 1000
TIMEOUT_MAX = 1000
TIMEOUT_STEP = 10

ARF_MIN  = 15
ARF_MAX  = 15
ARF_STEP = .1

RETRY_MIN = 1
RETRY_MAX = 1

BLOCK_SIZE = 512

IFC = "lo0"
FILENAME = "data/capture"


TMPDIR = "tmp"
DATADIR = "data"
LOGDIR = "log"


COAP_SERVER = "coap://localhost:5683"
#RES_LIST = ["res128", "res256", "res512", "res1024"]

RES_LIST = ["res1280"]
DEF_RES  = "res1280"

NUM_TEST = 2

DATA_PATH   = "data"
TEST_RESULT = "report.txt"
GRAPH_RESULT = "e2e.dat"
