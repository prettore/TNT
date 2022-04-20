##################################################
## stript to perform experiments automatically
##################################################
## Author: Paulo H. L. Rettore
## Status: open
## Date: 20/10/2020
##################################################
import base64
import os
import subprocess
import sys
from time import sleep
import datetime
import threading

# create folder
def creating_folders(dataFolder):
    if (os.path.isdir(dataFolder) == False):
        os.makedirs(dataFolder)

class myThread(threading.Thread):
    def __init__(self, command):
        threading.Thread.__init__(self)
        self.cmd = command

    def run(self):
        print("Starting " + self.cmd)
        os.system(self.cmd)
        print("Exiting " + self.cmd)

def get_time_interval(delta_time_sec):
    now = datetime.datetime.now()#datetime.datetime.strptime("2020-10-21 09:00:00", "%Y-%m-%d %H:%M:%S")  # datetime.datetime.now()
    end_time = now + datetime.timedelta(seconds=delta_time_sec)
    start_time = now.strftime("%Y-%m-%d %H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Start time =", start_time)
    print("End time =", end_time, " (estimated)")

    return start_time,end_time

# Checking buffer usage
def buffer_usage():
    print("Checking buffer state\n")
    start_time, end_time = get_time_interval(experiment_duration)
    acquire_data_sender = 'python3 tb_data_acquisition.py -name sender -start "' + start_time + '" -end "' + end_time + \
                          '" -source "' + source_ip + '" -dest "' + dest_ip + '" -o Markov_' + experiment_desc + '.csv'
    os.system(acquire_data_sender)
    print("Check the csv buffer file\n")

# performing experiment over a given trace
def executing_experient(file_name,experiment_duration,round_number):
    # Checking buffer usage
    #buffer_usage()
    try:
        '''
            Evaluating scenarios
        '''
        for i in range(0,round_number):
            print("\nStarting the test-bed experiment... " + file_name + " " + str(i + 1) + " round\n")

            start_time,end_time = get_time_interval(experiment_duration)

            print("Changing the network...\n")
            # The raspberrypi needs to be on and the server needs to be up
            # first copy the trace files to the sender node
            # scp -r * tactics@10.132.26.160:/home/tactics/virtual_tactical_network/data/
            #changing the network
            thread1 = myThread(changing_network_client) # Create new threads
            thread1.start()# Start new Threads

            print("Creating the data flow\n")

            thread2 = myThread(exec_data_flow_server)# Create new threads
            thread2.start()# Start new Threads
            sleep(5)# waiting to establish signaling connection
            os.system(exec_data_flow_client)


            sleep(experiment_duration)
            #control mechanism to block the data acquisition til the packet queue is empty
            queue_has_packet = True
            while queue_has_packet:
                result = subprocess.getoutput(check_packet_queue_status)
                if result != 'True':
                    queue_has_packet = False
                else:
                    print("Waiting the packet queue get empty...")
                    sleep(10)
            end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("End time =", end_time, " (estimated)")

            print("Log the experiment...\n")
            #logs_ITG = 'sudo python ITGDec_Stats_Parser.py -i receiver.log -o statistics_Markov_Filled_'+experiment_desc+'.csv -t 2 -r '+str(i+1)
            #os.system(logs_ITG)
            acquire_data_sender = 'python3 tb_data_acquisition.py -name sender -start "' +start_time+'" -end "' +end_time+\
                           '" -source "' +source_ip+ '" -dest "' +dest_ip+ '" -o '+file_name+'_'+experiment_desc+'.csv -r '+str(i+1)
            os.system(acquire_data_sender)
            acquire_data_receiver = 'python3 tb_data_acquisition.py -name receiver -start "' +start_time+'" -end "' +end_time+\
                           '" -source "' +source_ip+ '" -dest "' +dest_ip+ '" -o '+file_name+'_'+experiment_desc+'.csv -r '+str(i+1) +\
                                    ' -buffer False'
            os.system(acquire_data_receiver)

            os.system(kill_data_flow_server) # stop the server application
            os.system(kill_process_client)  # stop the client process

        logs_IP = 'python3 tb_packet_processing.py -s tb_sender_pckts_'+file_name+'_'+experiment_desc+\
                  '.csv -r tb_receiver_pckts_'+file_name+'_'+experiment_desc+'.csv -o tb_ip_statistics_'+file_name+'_'+\
                  experiment_desc+'.csv'
        os.system(logs_IP)

            #print("Waiting for the experiment...\n")
            #sleep(experiment_interval)

    finally:
        print("\nExiting the auto-experiment! Removing process.")
        os.system(kill_data_flow_server) # stop the server application
        os.system(kill_process_client)  # stop the client process


if __name__ == '__main__':

    start_time = datetime.now()
    path = os.path.dirname(os.path.abspath(__file__))
    stat_dir = start_time.strftime('%Y-%m-%d_%H-%M-%S') + "/"
    statistics_dir = path + '/data/statistics/' + stat_dir
    creating_folders(statistics_dir)

    #trace_list = ["Trace_Test.csv"]
    #trace_list = ["Trace_Stable.csv"]
    trace_list = ["Trace_Markov.csv","Trace_Markov_Filled.csv","Trace_Markov_Filled_Shortest.csv","Trace_GaussMarkov_VHF.csv","Trace_ManhattanGrid_VHF.csv", "Trace_ProbRandomWalk_VHF.csv","Trace_RandomWaypoint_VHF.csv"]
    experiment_desc = '1000p1to50p_20t'
    round_number = 1
    experiment_interval = 60
    experiment_duration = 11000

    ssh_coveh = '192.168.1.103'#'10.132.25.172'
    ssh_hq2 = '192.168.1.101'#'10.132.25.171'
    source_ip = '192.168.121.1'
    dest_ip = '192.168.110.1'


    for trace in trace_list:
        # setting commands to be executed remotely
        changing_network_client = 'cat change_network_state.py  | ssh tactics@'+ssh_coveh+' python - ' \
                                  '-t /tnt/data/'+trace+' -radio "192.168.121.7"'
        exec_data_flow_server = 'cat itg_receiver.py  | ssh tactics@'+ssh_hq2+' python - -close False'
        kill_data_flow_server = 'cat itg_receiver.py  | ssh tactics@'+ssh_hq2+' python - -close True'
        kill_process_client = 'cat kill_ssh_process.py  | ssh tactics@'+ssh_coveh+' python -'
        exec_data_flow_client = 'cat itg_sender.py  | ssh tactics@'+ssh_coveh+' python - '
        check_packet_queue_status = 'ssh tactics@'+ssh_coveh+' cat /home/tactics/tnt/packet_queue.txt'

        '''
        First create ssh key and save it in rhe receiver and sender nodes
        ssh-keygen -t rsa "your_email@domain.com"
        Sender(192.168.121.1) -> ssh-copy-id tactics@10.132.26.160
        Receiver(192.168.110.1) -> ssh-copy-id tactics@10.132.25.30
        '''
        file_name = trace.replace('Trace_', '').replace('.csv', '')

        executing_experient(file_name,experiment_duration,round_number)
        sleep(experiment_interval)

