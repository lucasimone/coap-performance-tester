COAP TESTING TOOL
---------------------
This projct aims to test the performance of the CoAP protocol by automatically changinging some parameters such as Timeout, ACK_RAND_FACTOR and Retransmission.
Base on the e2e delay some KPI will be computed such as Packet Delivery Ratio (PRD). All those information, with the pcap and json dissected files will be stored in the ./data folder


## Getting Started

TODO: ...


## Prerequisites
This project requires the following components

* A linux based OS with
    * JAVA
    * Coap Server [Californium](https://www.eclipse.org/californium/)
    * Python (2.x or 3.x)
    * [TSHARK](https://www.wireshark.org/docs/man-pages/tshark.html)
    * [TCPDUMP](http://www.tcpdump.org/)



## Installing

```bash
clone https://github.com/lucasimone/coap-performance-tester.git
cd mqtt-performance-tester
pip install -r requirements.txt
```

## Run the testing tool
To run the test use the following commands:
```bash
./start_test.sh
```


## Create performance report

To make the test simpler, the report is generated post-mortem.
Please use the following script to create it, providing the root folder where all the PCAP files are stored.
```bash
gen_report.sh
```


## Authors

* [Luca Lamorte](mailto:luca.lamorte@gmail.com) - Initial work - [M2M SAT Project](https://artes.esa.int/projects/m2msat)

See also the list of [contributors](contributors.md) who participated in this project.


## Acknowledgments

## MIT License
Copyright (c) 2017, Luca Lamorte
All rights reserved.