##################################################
## Acquiring data from the test-bed
##################################################
## Author: Paulo H. L. Rettore
## Status: open
## Date: 19/10/2020
##################################################
import argparse
import csv
import os
import datetime
from collections import OrderedDict
from time import sleep
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2

#create folder
def creatingFolders(dataFolder):
    if (os.path.isdir(dataFolder) == False):
        os.makedirs(dataFolder)

def parse_string(string):
    """
    function to convert acquired data to string format
    @param string:  data
    @return:        data in string format if it exists else return None to fill 'null' value in the corresponding table record
    """
    if not string:
        return None
    else:
        return str(string)

#Checking if there is no data on the buffer anymore
def buffer_usage(host_db,port_db,database_name,user_db,password_db,start,end):
    """ Connect to the PostgreSQL database server """
    conn = None
    observations = 20 # rows with 0% buffer occupancy
    buffer_full = True
    try:
        # connect to the PostgreSQL server
        print('Connecting and acquiring data form the PostgreSQL database ('+database_name+')...')

        # ====== Connection ======
        # Connecting to PostgreSQL by providing a sqlachemy engine
        engine = create_engine(
            'postgresql://' + user_db + ':' + password_db + '@' + host_db + ':' + port_db + '/' + database_name, echo=False)


        sql = "SELECT * FROM public .radio_buffer"
        sql += " WHERE ("
        sql += " buffer_timestamp >= '" + start + "' AND buffer_timestamp <= '" + end +"'"
        sql += " )"
        sql += " ORDER BY buffer_timestamp ASC"

        # ====== Reading table ======
        # Reading PostgreSQL table into a pandas DataFrame
        df_buffer = pd.read_sql(sql, engine) # ***** Change Sharath script to collect float percentage

        if np.sum(df_buffer.tail(observations)['pr4g_queue_occupancy']) == 0:
            buffer_full = False
        else:
            print('Buffer usage: ' + str(np.array(df_buffer.tail(observations)['pr4g_queue_occupancy'])))
            buffer_full = True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return buffer_full

#collecting data from the data base
def collect_db_data(host_db,port_db,database_name,user_db,password_db,start,end,source_ip,dest_ip,output,round,buffer):#,schema):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting and acquiring data form the PostgreSQL database ('+database_name+')...')

        # ====== Connection ======
        # Connecting to PostgreSQL by providing a sqlachemy engine
        engine = create_engine(
            'postgresql://' + user_db + ':' + password_db + '@' + host_db + ':' + port_db + '/' + database_name, echo=False)

        if buffer=='True':
            sql = "SELECT * FROM public .radio_buffer"
            sql += " WHERE ("
            sql += " buffer_timestamp >= '" + start + "' AND buffer_timestamp <= '" + end +"'"
            sql += " )"
            #sql += " ORDER BY buffer_timestamp ASC"

            # ====== Reading table ======
            # Reading PostgreSQL table into a pandas DataFrame
            df_buffer = pd.read_sql(sql, engine)
            # adding experient round
            df_buffer['round'] = round
            # filtering the data frames by columns
            buffer_columns = ['buffer_timestamp', 'data_throughput', 'pr4g_queue_occupancy', 'round']
            df_buffer = df_buffer[buffer_columns]

        sql = "SELECT * FROM public .packet_sniffer"
        sql += " WHERE ("
        sql += " packet_timestamp >= '" + start + "' AND packet_timestamp <= '" + end + "'"
        if source_ip != "":
            sql += " AND source_ip = '"+source_ip+ "'"#'192.168.121.1'"
        if dest_ip != "":            sql += " AND destination_ip = '"+dest_ip+ "'"#'192.168.110.1'"
        sql += " AND protocol = 'DATA_RAW'"   # DATA_RAW should mean UDP hopefully
        sql += " )"
        #sql += " ORDER BY buffer_timestamp ASC"

        # ====== Reading table ======
        # Reading PostgreSQL table into a pandas DataFrame
        df_sniffer = pd.read_sql(sql, engine)
        # adding experient round
        df_sniffer['round'] = round
        # filtering the data frames by columns
        packet_columns = ['packet_id', 'packet_timestamp', 'source_ip', 'destination_ip', 'protocol',
                               'packet_length', 'round']  # , 'payload_length', 'payload','round']
        df_sniffer = df_sniffer[packet_columns]


        # saving test-bed data experiments
        # if os.path.isfile(path +'/data/statistics/'+ "tb_"+database_name+"_pckts_" +output):
        #     if buffer=='True':
        #         df_buffer.to_csv(path +'/data/statistics/'+ "tb_"+database_name+"_buffer_" +output, mode='a', index=False,header=False)
        #     df_sniffer.to_csv(path +'/data/statistics/'+ "tb_"+database_name+"_pckts_" +output, mode='a', index=False,header=False)
        # else:
        # saving statistics
        if buffer=='True':
            if os.path.isfile(path +'/data/statistics/'+ "tb_"+database_name+"_buffer_" +output):
                df_buffer.to_csv(path +'/data/statistics/'+ "tb_"+database_name+"_buffer_" +output, mode='a', index=False, header=False)
            else:
                df_buffer.to_csv(path + '/data/statistics/' + "tb_" + database_name + "_buffer_" + output, index=False)
        if os.path.isfile(path + '/data/statistics/' + "tb_" + database_name + "_pckts_" + output):
            df_sniffer.to_csv(path +'/data/statistics/'+ "tb_"+database_name+"_pckts_" +output, mode='a', index=False, header=False)
        else:
            df_sniffer.to_csv(path + '/data/statistics/' + "tb_" + database_name + "_pckts_" + output, index=False)


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':

    path = os.path.dirname(os.path.abspath(__file__))
    creatingFolders(path+'/data/statistics/')

    parser = argparse.ArgumentParser(description="Data acquisition process!")
    parser.add_argument("-host", "--host_db", help="Data base host ip", type=str, default='192.168.1.99')#'10.132.25.223')#"laptop2.stabko.rhnlab.fkie.fraunhofer.de"
    parser.add_argument("-port", "--port_db", help="Data base host port", type=str, default='5432')
    parser.add_argument("-name", "--database_name", help="Data base name", type=str, required=True)
    parser.add_argument("-user", "--user_db", help="Data base user", type=str, default='tactics')
    parser.add_argument("-pass", "--password_db", help="Data base password", type=str, default='tactics')

    #parser.add_argument("-schema", "--schema", help="Experiment schema", type=str, required=True)
    parser.add_argument("-start", "--start", help="Experiment starts", type=str, required=True)
    parser.add_argument("-end", "--end", help="Experiment ends", type=str)
    parser.add_argument("-source", "--source", help="Source IP", type=str, default='')
    parser.add_argument("-dest", "--dest", help="Destination IP", type=str, default='')
    parser.add_argument("-o", "--outputFile", help="The file name that you wish to write data into", type=str, required=True)

    parser.add_argument("-r", "--expRound", help="The experiment round. Used to compute standard error and confidence interval", type=str,
                        default='0')
    parser.add_argument("-buffer", "--buffer", help="Collect buffer data", type=str, default='True')

    args = parser.parse_args()

    if args.database_name and args.outputFile and args.start and args.end:
        #start the data acquisition only if there is no data on the buffer anymore
        if args.buffer == 'True':
            buffer_full = True
            experiment_end = args.end
            while buffer_full:
                buffer_full = buffer_usage(args.host_db,args.port_db,args.database_name,args.user_db,args.password_db,
                        args.start,experiment_end)
                if buffer_full:
                    sleeping = np.random.uniform(10, 60, 1)
                    print('Sleeping for '+str(int(sleeping[0]))+' seconds, cause there still data on the buffer...')
                    sleep(sleeping)
                    now = datetime.datetime.now()
                    experiment_end = now.strftime("%Y-%m-%d %H:%M:%S")

            collect_db_data(args.host_db,args.port_db,args.database_name,args.user_db,args.password_db,
                    args.start,experiment_end,args.source,args.dest,args.outputFile,args.expRound,args.buffer)
        else:
            collect_db_data(args.host_db, args.port_db, args.database_name, args.user_db, args.password_db,
                         args.start, args.end, args.source, args.dest, args.outputFile, args.expRound, args.buffer)
    else:
        print("Exiting of Packet Capture App! There are no enough arguments")