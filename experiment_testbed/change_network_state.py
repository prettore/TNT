##################################################
## stript to change the data rate based on a
# trace file
##################################################
## Author: Paulo H. L. Rettore
## Status: open
## Date: 02/10/2020
##################################################
import argparse
import pandas as pd
import os
import sys
from datetime import datetime
import time
import socket
import struct

# IP_Radio = '192.168.121.7'  # co-veh
# IP_Radio  = '192.168.111.2' #re1
# IP_Radio  = '192.168.110.9' #hq2

# IP_Radio = '192.168.110.9' #r1
# IP_Radio = '192.168.111.2' #r3
# IP_Radio='192.168.121.7' # Radio IP address r2
# IP_RaspberryPi = '10.132.1.130'
IP_RaspberryPi = '192.168.1.141'

# print("Start Time:"+time.ctime())
print('Started fkie-everchanging-datarate')

# reading trace files
def get_trace(node, file_):
    df_trace = pd.read_csv(file_)
    df_trace['node'] = df_trace['node'].astype(int)
    trace_node = df_trace.groupby('node')
    state_interval = []
    state = []
    position_and_time = []
    for n in trace_node.groups:
        if node == n:
            trace = trace_node.get_group(n)
            # for row in trace:
            for line in range(1, len(trace)):
                t = float(trace.loc[line - 1, "time"])
                t_1 = float(trace.loc[line, "time"])
                if line == 1:
                    state.append(int(float(trace.loc[line-1, "state"])))
                    state_interval.append(t_1 - t)
                    position_and_time.append(str(str(trace.loc[line - 1, "x"]) + "," + str(trace.loc[line - 1, "y"]) + "," +
                                                 str(trace.loc[line - 1, "time"])))

                state.append(int(float(trace.loc[line, "state"])))
                state_interval.append(t_1 - t)
                position_and_time.append(str(str(trace.loc[line, "x"]) + "," + str(trace.loc[line, "y"])+ "," +
                        str(trace.loc[line, "time"])))

    return state, state_interval, position_and_time

# Send the disruption time to the Raspberry pi controlling the relay
def sendDisruptionTime(ipAddress, servicePort, disconnectionTime):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ipAddress, servicePort))
    # the server needs to read like: disruption_interval_data = float(struct.unpack('f', data)[0])
    s.sendall(struct.pack('f', disconnectionTime))
    #s.sendall(bytes([20]))
    data = s.recv(1024)
    print('Received', repr(data))

# Set the radio datarate using SNMP
# it needs sudo apt install snmp
def set(version="2c", community="rwcom", dest="localhost", port="161", oids_types_values=[("", "", ""), ("", "", "")]):
    ## permet de faire un SET sur n'importe qu'elle valeur de la MIB ##
    oids_types_values_trad = ""
    for i in oids_types_values:
        oids_types_values_trad = oids_types_values_trad + str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " "
    set = os.popen(
        "snmpset " + "-v " + version + " -c " + community + " " + dest + ":" + port + " " + str(oids_types_values_trad))
    # res = set.readlines()
    # return res

# change the radio data rate and disconnect the network
def state_change(traceFile,IP_Radio,gps_folder):
    # path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    path = os.path.abspath(os.path.dirname(__file__))

    # Dictionary with list object in values
    #state_machine_dic = {
    #    'sequence': [],
    #    'state': [],
    #    'datetime': [],
    #    'status': []
    #}

    # Sequences of states defined to change the network state and state time interval
    state_queue, time_interval, position_and_time = get_trace(0, path + "/" + traceFile)

    las_state = -1
    for i in range(len(state_queue)):

        #state_machine_dic['sequence'].append(i)
        #state_machine_dic['state'].append(state_queue[i])
        #state_machine_dic['datetime'].append(datetime.now())

        # writing the node position simulating gps readings
        with open(gps_folder+'gps.csv', 'w') as file:
            file.write(position_and_time[i])

        if state_queue[i] == 0:
            # PORT,SWITCH ADDRESS, SWITCH USER, SWITCH PASSWORD, DISCONNECTION TIME IN SECONDS
            print('Sequence %d, State %d, Datetime %s -- disconnected for %f second' % (
                i, state_queue[i], datetime.now(), time_interval[i]))

            #state_machine_dic['status'].append("Disconnected")
            sendDisruptionTime(IP_RaspberryPi, 2002, time_interval[i])
        else:
            # change the radio data rate only if it changes from the last state
            if las_state != int(state_queue[i]):
                set(version="1", community="rwcom", dest=IP_Radio, port="161",
                    oids_types_values=[("1.3.6.1.4.1.4045.61005681.3.3.17.0", "integer", str(state_queue[i]))])

                print('Sequence %d, State %d, Datetime %s -- connected for %f second' % (
                i, state_queue[i], datetime.now(), time_interval[i]))

            las_state = int(state_queue[i])
            #state_machine_dic['status'].append("Connected")

            time.sleep(time_interval[i])

    # df = pd.DataFrame.from_dict(state_machine_dic)
    # df.to_csv('state_machine.csv',index=False)

# simulating GPS writing
def state_change_debug(traceFile):
    path = os.path.abspath(os.path.dirname(__file__))

    # Sequences of states defined to change the network state and state time interval
    state_queue, time_interval, position_and_time = get_trace(0, path + "/" + traceFile)

    las_state = -1
    for i in range(len(state_queue)):

        # writing the node position simulating gps readings
        with open('gps.csv', 'w') as file:
            file.write(position_and_time[i])

        if state_queue[i] == 0:
            # PORT,SWITCH ADDRESS, SWITCH USER, SWITCH PASSWORD, DISCONNECTION TIME IN SECONDS
            print('Sequence %d, State %d, Datetime %s -- disconnected for %f second' % (
                i, state_queue[i], datetime.now(), time_interval[i]))
        else:
            # change the radio data rate only if it changes
            if las_state != int(state_queue[i]):

                print('Sequence %d, State %d, Datetime %s -- connected for %f second' % (
                    i, state_queue[i], datetime.now(), time_interval[i]))

            las_state = int(state_queue[i])

        time.sleep(time_interval[i])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Ever-changing network scenario!")
    parser.add_argument("-t", "--traceFile", help="Input trace file", type=str, required=True)
    parser.add_argument("-radio", "--radio", help="Radio IP", type=str, required=True)
    parser.add_argument("-gps", "--gpsFolder", help="Save GPS readings", type=str, required=True)
    args = parser.parse_args()

    if args.traceFile and args.radio and args.gpsFolder:
        state_change(str(args.traceFile), str(args.radio), str(args.gpsFolder))
        #state_change_debug(str(args.traceFile))
    else:
        print("Exiting the experiment! There are no enough arguments")
