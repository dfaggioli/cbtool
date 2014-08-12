#!/usr/bin/env python
#/*******************************************************************************
# Copyright (c) 2012 IBM Corp.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#/*******************************************************************************
'''
This is a Python example of how to provision a virtual machine through CloudBench

This assumes you have already attached to a cloud through the GUI or CLI.
'''

from time import sleep
from sys import path
import os
import fnmatch

_home = "/home/cbtool" 
_api_endpoint = "20.0.0.20"
_cloud_name = "myopenstack"
_workload = "cassandra_ycsb"

#
# 
#
def checking_sla (self, _yaml) :
    return true;

for _path, _dirs, _files in os.walk(os.path.abspath(_home)):
    for _filename in fnmatch.filter(_files, "code_instrumentation.py") :
        path.append(_path.replace("/lib/auxiliary",''))
        break

from lib.api.api_service_client import *

api = APIClient("http://" + _api_endpoint + ":7070")

_launched_ais = []

try :
    error = False
    vm = None

    _cloud_attached = False
    for _cloud in api.cldlist() :
        if _cloud["name"] == _cloud_name :
            _cloud_attached = True
            _cloud_model = _cloud["model"]
            break

    if not _cloud_attached :
        print "Cloud " + _cloud_name + " not attached"
        exit(1)

    ai_return_state=True

    print "Launching AI %s" % _workload
    print "Guest, Provison complete, Network accessible, Last Known state"
    while ai_return_state :
#----------------------- Create Apps over time ----------------------------------
        app = api.appattach(_cloud_name, _workload)
	vms = [ val.split("|")[0] for val in app["vms"].split(",")]
        for vm in vms :
	    _guest_data = api.get_latest_management_data(_cloud_name,vm)
	    print "%s ,%s, %s, %s" % (_guest_data["cloud_hostname"], 
							_guest_data["mgt_003_provisioning_request_completed"],
							_guest_data["mgt_004_network_acessible"],
							_guest_data["last_known_state"])
        _launched_ais.append(app)
        ai_return_state=check_sla(app)

    print "Removing all AIs"
    api.appdetach(_cloud_name, app["uuid"])

except APIException, obj :
    error = True
    print "API Problem (" + str(obj.status) + "): " + obj.msg

except APINoSuchMetricException, obj :
    error = True
    print "API Problem (" + str(obj.status) + "): " + obj.msg

except KeyboardInterrupt :
    print "Aborting this VM."

except Exception, msg :
    error = True
    print "Problem during experiment: " + str(msg)

finally :
    if app is not None :
        try :
            if error :
                print "Destroying VM..."
                api.appdetach(_cloud_name, app["uuid"])
        except APIException, obj :
            print "Error finishing up: (" + str(obj.status) + "): " + obj.msg
