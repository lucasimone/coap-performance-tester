#!/usr/bin/env bash
echo "################################"
echo "Start a CoAP Server on port 5683"
echo "################################"
java -jar coap_libs/src_server/target/coap_server-1.0-SNAPSHOT.jar 0.0.0.0 5683