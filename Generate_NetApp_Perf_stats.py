#!/usr/env/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""
#===============================================================#
#                                                               #
# $ID$                                                          #
#                                                               #
# perf_operation.py                                             #
#                                                               #
# Sample code for the usage of following APIs:                  #
#                       perf-object-list-info                   #
#                       perf-object-counter-list-info           #
#                       perf-object-instance-list-info          #
#                       perf-object-get-instances-iter-*        #
#                                                               #
changed from the sample script in the 5.2 manaeability API kit by jc18
# Copyright 2011 Network Appliance, Inc. All rights             #
# reserved. Specifications subject to change without notice.    #
#                                                               #
# This SDK sample code is provided AS IS, with no support or    #
# warranties of any kind, including but not limited to          #
# warranties of merchantability or fitness of any kind,         #
# expressed or implied.  This code is subject to the license    #
# agreement that accompanies the SDK.                           #
#                                                               #
#===============================================================#

IMPORTANT: an api enabled user must be defined on the system
This can be done on 7-Mode with;
useradmin role add api_only -c "created by jc18" -a api-*, login-http-admin
useradmin group add sandb_api -c "created by jc18 20140218" -r api_only
useradmin user add sandb_api_only -c "created by jc18 20140218" -g sandb_api

jc18 20140314
$Id$
"""


import sys
import json
import time
from collections import defaultdict
from socket import socket

sys.path.append("netapp-manageability-sdk-5.2/lib/python/NetApp")
from NaServer import *

def print_usage():
    print("perf_operation.py <filer> <user> <password> <operation> <value1>")
    print("[<value2>]\n")
    print("<filer>     -- Filer name\n")
    print("<user>      -- User name (will also use a ~/.netapp_api_key file)\n")
    print("<password>  -- Password (will also use a ~/.netapp_api_key file)\n")
    print("<operation> -- Operation to be performed: \n")
    print("\tobject-list   - Get the list of perforance objects in the system\n")
    print("\tinstance-list - Get the list of instances for a given performance object\n")
    print("\tcounter-list  - Get the list of counters available for a given performance object\n")
    print("\tget-counter-values - Get the values of the counters for all the instances of a performance object\n")
    print("[<value1>]  -- Depends on the operation \n")
    print("[<value2>]  -- Depends on the operation \n")
    sys.exit (1)

    
# perf-object-list-info operation
# Usage: perf_operation.py <filer> <user> <password> object-list
def get_object_list(s):
    list_in = NaElement("perf-object-list-info")
    # Invoke API
    out = s.invoke_elem(list_in)	

    if(out.results_status() == "failed"):
        print(out.results_reason() + "\n")
        sys.exit(2)

    obj_info = out.child_get("objects")
    result = obj_info.children_get()

    for obj in result:
        obj_name = obj.child_get_string("name")
        priv = obj.child_get_string("privilege-level")
        print("Object Name = " + obj_name + "\tPrivilege Level = " + priv + "\n")
        
    print("\n")
    

# perf-object-instance-list-info operation
# Usage: perf_operation.py <filer> <user> <password> instance-list <objectname>
def get_instance_list(s):
    if (args < 5):
        print ("Usage: perf_operation.py <filer> <user> <password> instance-list <objectname> \n")
        sys.exit (1)

    list_in = NaElement("perf-object-instance-list-info")
    obj_name = sys.argv[5]
    list_in.child_add_string("objectname", obj_name)

    # Invoke API
    out = s.invoke_elem(list_in)
    
    if(out.results_status() == "failed"):
        print(out.results_reason() + "\n")
        sys.exit(2)

    inst_info = out.child_get("instances")
    result = inst_info.children_get()
    
    for inst in result:
        inst_name = inst.child_get_string("name")
        print("Instance Name = " + inst_name + " \n")

    print("\n")


# perf-object-counter-list-info operation
# Usage: perf_operation.py <filer> <user> <password> counter-list <objectname>
def get_counter_list(s):
    if (args < 5) :
        print ("Usage: perf_operation.py <filer> <user> <password> counter-list <objectname>")
        sys.exit (1)

    list_in = NaElement("perf-object-counter-list-info")
    obj_name =sys.argv[5]
    list_in.child_add_string("objectname", obj_name)

    # Invoke API
    out = s.invoke_elem(list_in)
    
    if(out.results_status() == "failed"):
        print(out.results_reason() + "\n")
        sys.exit(2)
    		
    counter_info = out.child_get("counters")
    result = counter_info.children_get()
    
    for counter in result:
        counter_name = counter.child_get_string("name")
        print("Counter Name = " + counter_name + " \t\t\t")
        
        if (counter.child_get_string("base-counter")):
            base_counter = counter.child_get_string("base-counter")
            print("Base Counter = " + base_counter + "\t\t")
            
        else :
            print("Base Counter = none\t\t")

        privilege_level = counter.child_get_string("privilege-level")
        print("Privilege_level = " + privilege_level + "\t\t")

        if (counter.child_get_string("unit")) :
            unit = counter.child_get_string("unit")
            print("Unit = " + unit + "\t\t")

        else :
            print("Unit = None\t\t")

        print("\n")


# perf-object-get-instances-iter-* operation
# Usage: perf_operation.py <filer> <user> <password> get-counter-values <objectname> [ <counter1> <counter2>...]
 
def get_counter_values(filer, s):
    max_records = 10
    lines=[]
    now = int( time.time() )

    
    if (args < 3) :
        print ("Usage: perf_operation.py <filer> <user> <password> get-counter-values <objectname> [ <counter1> <counter2> ...]")
        sys.exit (1)

    perf_in = NaElement("perf-object-get-instances-iter-start")
    obj_name = sys.argv[2]
    perf_in.child_add_string("objectname", obj_name)
    counters = NaElement("counters")

    if ( args > 1 ) :
        i = 3
        
        while(i < len(sys.argv)):
            counters.child_add_string("counter", sys.argv[i])
            i = i + 1
        perf_in.child_add(counters)

    # Invoke API
    out = s.invoke_elem(perf_in)

    if(out.results_status() == "failed"):
	print("issue with filer: " + filer)
        print(out.results_reason() + "\n")
        sys.exit(2)
    
    iter_tag = out.child_get_string("tag")
    num_records = 1

    while(int(num_records) != 0):
        perf_in = NaElement("perf-object-get-instances-iter-next")
        perf_in.child_add_string("tag", iter_tag)
        perf_in.child_add_string("maximum", max_records)
        out = s.invoke_elem(perf_in)

        if(out.results_status() == "failed"):
            print(out.results_reason() + "\n")
            sys.exit(2)

        num_records = out.child_get_int("records")
	
        if(num_records > 0) :
            instances_list = out.child_get("instances")            
            instances = instances_list.children_get()

            for inst in instances:
                inst_name = inst.child_get_string("name")
                #print ("Instance = " + inst_name + "\n")
                counters_list = inst.child_get("counters")
                counters = counters_list.children_get()

                for counter in counters:
                    counter_name = counter.child_get_string("name")
                    counter_value = counter.child_get_string("value")
                    #print( \
                    #    "Instance " + 
                    #      inst_name + 
                    #     " Counter Name = " +  
                    #     counter_name + 
                    #     " Counter Value = " + 
                    #    counter_value 
                    #    )
                    name = filer + "." + inst_name + "." + counter_name
                    lines.append("%s %d %d" % (name, int(counter_value), now))

                    
	
    perf_in= NaElement("perf-object-get-instances-iter-end")
    perf_in.child_add_string("tag", iter_tag)
    out = s.invoke_elem(perf_in)

    if(out.results_status() == "failed"):
            print(out.results_reason() + "\n")
            sys.exit(2)

    return(lines)

def SendToGraphite(message):
    """
    takes an array of strings to send to the graphite server for graphing
    """
    CARBON_SERVER = 'pc7-dev.internal.sanger.ac.uk'
    CARBON_PORT = 2003

    # Establish carbon socket connection
    from socket import socket

    sock = socket()
    try:
        sock.connect( (CARBON_SERVER,CARBON_PORT) )
    except:
        print \
            "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" \
            % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
        sys.exit(1)
    
    sock.sendall(message)

def Get7ModeSystems():
    """
    import the JSON file of all the NetApp 7-Mode systems to check
    format:
        SevenMode = [ \
                    [ "netapp3a.internal.sanger.ac.uk", "sandb_api_only",
        "secretpassword"],
            [ "netapp3b.internal.sanger.ac.uk", "sandb_api_only",
            "secretpassword"],
                ]
    """
    datafile = open("7mode_systems.json", mode='r')
    try:
            SevenMode = json.load(datafile)

    except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
    return SevenMode

	
def main() :
    SevenMode = Get7ModeSystems()

    for toaster in SevenMode:
        drives_mapped = defaultdict(list)
        filer = toaster[0]
        user = toaster[1]
        pw = toaster[2]

        s = NaServer(filer, 1, 3)
        out = s.set_transport_type('HTTPS')

        if (out and out.results_errno() != 0) :
            r = out.results_reason()
            print ("Connection to filer failed: " + r + "\n")
            sys.exit(2)

        out = s.set_style('LOGIN')
    
        if (out and out.results_errno() != 0) :
            r = out.results_reason()
            print ("Connection to filer failed: " + r + "\n")
            sys.exit(2)

        out = s.set_admin_user(user, pw)

        if(command == "object-list"):
            get_object_list(s)

        elif(command == "instance-list"):
            get_instance_list(s)

        elif(command == "counter-list"):
           get_counter_list(s)

        elif(command == "get-counter-values"):
            message_lines = []
            #turn the filer FQDN into something more Graphite Friendly
            filername = filer.split(".")[0]
            message_lines = get_counter_values(filername, s)
            message = '\n'.join(message_lines) + '\n' 
            #print message
            SendToGraphite(message)


        else:
            print ("Invalid operation\n")
            print_usage()


"""  
start here
"""


args = len(sys.argv) - 1

if(args < 1):
    print_usage()
    
#filer = sys.argv[1]
#user = sys.argv[2]
#pw  = sys.argv[3]
command = sys.argv[1]

main()

