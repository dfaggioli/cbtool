#!/usr/bin/env bash

#/*******************************************************************************
# This source code is provided as is, without any express or implied warranty.
#
# cb_restart_mongos.sh - 
#
#
# @author Joe Talerico, jtaleric@redhat.com
#/*******************************************************************************

source $(echo $0 | sed -e "s/\(.*\/\)*.*/\1.\//g")/cb_ycsb_common.sh

START=`provision_application_start`

SHORT_HOSTNAME=$(uname -n| cut -d "." -f 1)

# Remove all previous configurations
sudo rm -rf ${MONGODB_DATA_DIR}/configdb/*

pos=1

for db in $mongo_ips
do
    if [[ $(cat /etc/hosts | grep -c "mongo$pos ") -eq 0 ]]
    then    
        sudo sh -c "echo $db mongo$pos mongodb-$pos >> /etc/hosts"
    fi
    ((pos++))
done

#
# Start Mongos 
#
sudo pkill -9 -f configdb
sudo screen -S MGSS -X quit
sudo screen -d -m -S MGSS
sudo screen -p 0 -S MGSS -X stuff "sudo mongos --configdb ${mongocfg_ip}:27019$(printf \\r)"

wait_until_port_open 127.0.0.1 27017 20 5

STATUS=$?

if [[ ${STATUS} -eq 0 ]]
then
        syslog_netcat "MongoDB Sharding server running"
else
        syslog_netcat "MongoS Sharding server failed to start"
fi

#
# Add Shards
#
pos=1
for db in $mongo_ips
do
    mongo --host ${mongos_ip}:27017 --eval "sh.addShard(\"mongo$pos:27017\")"
    syslog_netcat " Adding the following shard: mongo$pos:27017 "
    ((pos++))
done

provision_application_stop $START

exit 0