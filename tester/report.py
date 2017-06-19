import glob
import os

from tester.write_output import *
#data_path = input("Please enter data path: ")


###### CAMBIA SOLO QUESTI VALORI!!!!!

num_test = 500
data_path = "on18off2"
#######################################

path = "./%s/" % data_path
index  = 0



init_output_file(data_path, num_test)  # INIT FILE

for filename in glob.glob(os.path.join(path, '*.json')):

    file_id = filename.replace(data_path, "")
    file_id = filename.replace(".json", "")

    file_info = filename.replace("%scaputure_"%data_path, "")

    file_info = file_info.split("_")
    timeout = file_info[1]
    rand_factor = file_info[3]
    retry = file_info[5]
    res = file_info[6]


    # write line for this filename
    write_test_result(index, res, timeout, rand_factor, retry, file_id, data_path, num_test)

    index += 1