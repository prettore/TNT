##################################################
## script to shape a specific data flow with UDP
# packets using qdisc
##################################################
## Author: Paulo H. L. Rettore
## Status: open
## Date: 23/10/2020
##################################################
import argparse
import subprocess
from subprocess import call
import time
import re
import json



# usefull links
# https://netbeez.net/blog/how-to-use-the-linux-traffic-control/
# https://medium.com/criteo-labs/demystification-of-tc-de3dfe4067c2
# http://tcn.hypert.net/tcmanual.pdf
# https://raspberry.redbrain.me/Scripte/Traffic_shaping.html
# https://wiki.linuxfoundation.org/networking/netem#delaying_only_some_traffic
# http://home.ifi.uio.no/paalh/students/AndersMoe.pdf
# tc -s qdisc ls dev eth0.101 # statistics

# get the radio datarate using SNMP - it needs sudo apt install snmp
def get_data_rate(version="2c", community="rwcom", dest="localhost", port="161", oids_types_value=""):

    command_str = "snmpget " + "-v " + version + " -c " + community + " " + dest + ":" + port + " " + oids_types_value

    #print("Connecting to the radio...")
    result = subprocess.getoutput(command_str)
    #print(result)

    # removing all characters keeping only the network state
    if "INTEGER:" in str(result):
        state = re.sub("[^0-9]", "", str(result).split("INTEGER:")[1])
        # print("Data rate state: "+str(state))
        return int(state)
    else:
        return -1

# function to get the radio buffer using SNMP
def get_buffer(version="2c", community="public", dest="localhost", port="161", oid="0", option=""):
    ## permet de faire un GET sur n'importe qu'elle valeur de la MIB ##
    command_str = "snmpget " + " " + option + " " + "-v " + version + " -c " + community + " " + dest + ":" + port + " " + oid

    result = subprocess.getoutput(command_str)

    # removing all characters keeping only the network state
    if "INTEGER:" in str(result):
        buffer = re.sub("[^0-9]", "", str(result).split("INTEGER:")[1])
        return round(int(buffer) * 100 / 131072, ndigits=2)
    else:
        return -1

# cleaning the radio buffer
def clear_buffer(version = "2c", community = "public", dest = "localhost", port = "161", oid="0"):
    #snmpset -v 1 -c rwcom 192.168.121.7:161 1.3.6.1.6.3.1.1.6.1.0 integer 1 1.3.6.1.4.1.4045.61005681.3.1.20.0 integer 1

    command_str = "snmpget " + "-v " + version + " -c " + community + " " + dest + ":" + port + " " + oid[0]
    result = subprocess.getoutput(command_str)

    if "INTEGER:" in str(result):
        value = re.sub("[^0-9]", "", str(result).split("INTEGER:")[1])

    command_str = "snmpset " + "-v " + version + " -c rwcom " + dest + ":" + port + " " + oid[0] + " integer "+ value +" " +oid[1]+" integer 1"
    #print(command_str)
    subprocess.getoutput(command_str)

    # # for test only
    # result = subprocess.Popen("ssh {user}@{host} {cmd}".format(user='tactics', host='10.132.26.160', cmd=command_str), shell=True,
    #                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    print("Cleaning the radio buffer...")

# get statistics from queue discipline
def get_queue_stats():

    command_str = 'tc -s class show dev ' + args.interface
    result_rate = str(subprocess.getoutput(command_str))

    # "class htb 1:2 root leaf 2: prio rate 4800bit ceil 4800bit burst 1599b cburst 1599b"
    # rate_str = re.search(re.escape('rate ') + "(.*)" + re.escape(' ceil'), result_rate).group(1)
    # queued_str = re.search(re.escape('overlimits ') + "(.*)" + re.escape('requeues'), result_rate).group(1)
    #rate_str = re.findall(re.escape('rate ') + "(.*)" + re.escape(' ceil'), result_rate)[1]
    queued_str = re.findall(re.escape('overlimits ') + "(.*)" + re.escape('requeues'), result_rate)[1]

    command_str = 'tc -s -j qdisc show dev ' + args.interface
    result = str(subprocess.getoutput(command_str))
    #result = str(subprocess.check_output(command_str,shell= True))

    result_js = json.loads(result)

    total_packet = "0"
    packet_over = "0"
    packet_drops = "0"
    queue_len = "0"
    for rule in result_js:
        if "htb" == rule['kind']:
            total_packet = str(rule['packets'])
            packet_over =  queued_str.strip() #str(rule['overlimits'])
            packet_drops = str(rule['drops'])
            queue_len = str(rule['qlen'])

    # writing if the packet queue is empty or not
    if queue_len == "0":
        with open('packet_queue.txt', 'w') as file:
            file.write('False')
    else:
        with open('packet_queue.txt', 'w') as file:
            file.write('True')

    return total_packet,packet_over,packet_drops,queue_len

# function to create the qdisc
def setting_initial_rules():
    # delliting rules
    call('tc qdisc del dev ' + str(args.interface) + ' root', shell=True)
    # creating rules - buffer using HTB and filtering destination ip and UDP packets

    # call('tc qdisc add dev ' + str(args.interface) + ' handle 1: root htb', shell=True)
    # call('tc class add dev ' + str(args.interface) + ' parent 1: classid 1:1 htb rate ' +
    #      str(int(datarate_dic[current_rate])) + 'bit', shell=True)
    # call('tc filter add dev ' + str(args.interface) + ' parent 1: protocol ip prio 1 u32 '
    #                                                   'match ip dst ' + str(args.dest) +
    #      ' match ip protocol 17 0xff flowid 1:1', shell=True)

    # increasing the queue len - Root qdisc and default queue length:
    call('ip link set dev ' + str(args.interface) + ' txqueuelen 10000', shell=True)
    call('tc qdisc add dev ' + str(args.interface) + ' root handle 1: htb default 1', shell=True)
    call('tc class add dev ' + str(args.interface) + ' parent 1: classid 1:1 htb rate '+
         str(args.rate) + 'bit', shell=True)
    call('tc filter add dev ' + str(args.interface) + ' parent 1: protocol ip prio 1 u32 '
                                               ' match ip dst ' +  str(args.dest) +
                                                ' match ip src ' + str(args.src) +
                                               ' match ip protocol 17 0xff flowid 1:2', shell=True)  # match ip dport 8999 0xffff
    call('tc class add dev ' + str(args.interface) + ' parent 1:1 classid 1:2 htb rate ' + str(int(datarate_dic[current_rate])) + 'bit',
         shell=True) #ceil 9600bit


if __name__ == '__main__':

    datarate_dic = dict([(6,"1000000"),(5,"9600"),
         (4,"4800"),(3,"2400"),(2,"1200"),
         (1,"600"), (0,"100")])

    # rule_arg = ""
    parser = argparse.ArgumentParser(description="Shaping the data-flow!")
    parser.add_argument("-i", "--interface", help="The interface to be shaped", type=str,
                        required=True)
    parser.add_argument("-rate", "--rate", help="Sustained maximum rate in bit", type=str, default=9600)#, required=True)
    parser.add_argument("-dest", "--dest", help="Destination IP/mask", type=str, default='192.168.110.1/24')
    parser.add_argument("-src", "--src", help="Source IP/mask", type=str, default='192.168.121.1/24')
    parser.add_argument("-radio", "--radio", help="Radio IP", type=str, default='192.168.121.7')
    parser.add_argument("-bt", "--threshold", help="Buffer threshold in %", type=str, default=10)
    args = parser.parse_args()

    if args.interface and args.radio and args.dest and args.src:# and args.rate and args.burst and args.latency:# and args.radio:

        # cleaning the radio buffer
        clear_buffer(version="1", community="public", dest=str(args.radio), port="161",
                     oid=["1.3.6.1.6.3.1.1.6.1.0", "1.3.6.1.4.1.4045.61005681.3.1.20.0"])
        # get the data rate from the radio
        current_rate = get_data_rate(version="1", community="rwcom", dest=str(args.radio), port="161",
                                     oids_types_value="1.3.6.1.4.1.4045.61005681.3.3.17.0")

        # if something happen collecting the data rate and buffer -> keep the last tc qdisc
        if current_rate != -1:
            setting_initial_rules()# function to create the qdisc

        #buffer_size = 128000
        last_buffer = 0
        last_rate = 0
        flush_pct = 5
        flag_flush = False
        warning_threshold_pct = 10
        rate_decrease_pct = 30
        new_rate = int(datarate_dic[current_rate])
        monitoring_time = 2
        try:
            while True:
                # get the data rate from the radio
                current_rate = get_data_rate(version="1", community="rwcom", dest=str(args.radio), port="161",
                                             oids_types_value="1.3.6.1.4.1.4045.61005681.3.3.17.0")
                # get the buffer from the radio
                current_buffer = get_buffer(version="1", community="public", dest=str(args.radio), port="161",
                                 oid="1.3.6.1.4.1.4045.61005681.3.2.1.2.0", option="")

                # if something happen collecting the data rate and buffer -> keep the last tc qdisc
                if (current_rate != -1) and (current_buffer != -1):
                    #real_rate = (current_buffer * buffer_size) /monitoring_time

                    if not flag_flush:
                        # Buffer occupancy is greater than the threshold set
                        # reduce 30% of the current rate
                        if current_buffer >= int(args.threshold):
                            new_rate = int(max(int(datarate_dic[0]), int(new_rate) - (int(new_rate)*rate_decrease_pct/100)))# reduce 30% of the current rate
                            flag_dequeued = str(new_rate)
                        # Buffer occupancy is lesser than the threshold set
                        # speeding up the packet rate until reach the warning threshold area
                        elif abs(current_buffer - int(args.threshold)) > warning_threshold_pct:
                            new_rate = args.rate#datarate_dic[6]
                            flag_dequeued = str(new_rate)#'Unlimited'
                        # Buffer occupancy is in the warning threshold area
                        # use the same data rate from the radio to define the packet delivery rate
                        else:
                            new_rate = int(datarate_dic[current_rate])
                            flag_dequeued = str(new_rate)
                        # Buffer flush detected
                        # reduce the packet delivery rate to the minimum as possible
                        if last_buffer - current_buffer >= flush_pct and last_buffer - current_buffer != 0:
                            new_rate = int(datarate_dic[0])# reduce the dequeued rate to minimum
                            flag_dequeued = str(new_rate)
                            flag_flush = True
                            print('***Radio buffer flushed*** Reducing the dequeue rate...')
                    # leaving the flush area
                    else:
                        if last_buffer < current_buffer:
                        #if last_rate != current_rate:
                            flag_flush = False

                    call('tc class replace dev ' + str(args.interface) + ' parent 1:1 classid 1:2 htb rate ' +
                         str(new_rate) + 'bit', shell=True)
                    total_pckt,pckt_over,pckt_drops,queue_len = get_queue_stats()

                    print('Nominal/Dequeue rate: ' + datarate_dic[current_rate] +'/'+(flag_dequeued)+' bit/s  Buffer:  '+str(current_buffer)+
                         ' % Queue packet total/queued/drop/len: '+total_pckt+'/'+pckt_over+'/'+pckt_drops+'/'+queue_len+ ' Sleeping: '+str(monitoring_time)+'s')

                    last_buffer = current_buffer
                    last_rate = current_rate

                    #print("Current data rate: " + datarate_dic[last_rate] + "bit  Buffer usage:  "+str(current_buffer)+
                    #      " % IPD: "+str(new_delay)+' ms sleeping: '+str(monitoring_time)+'s')
                else:
                    total_pckt, pckt_over, pckt_drops, queue_len = get_queue_stats()
                    print("Contextual monitoring fails")

                time.sleep(monitoring_time)
        finally:
            print("\nExiting the experiment! Removed tc qdisc rules.")
            call('tc qdisc del dev ' + str(args.interface) + ' root', shell=True)

    else:
        print("Exiting the experiment! There are no enough arguments")
