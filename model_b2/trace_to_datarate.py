##################################################
## map positions and data rate based on rings
##################################################
## Author: Paulo H. L. Rettore
## Status: open
## Date: 17/08/2020
##################################################
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sys
import scipy
from numpy.random.mtrand import uniform
from scipy.spatial.distance import cdist
import itertools
import glob
from PIL import Image


# create folder
def creatingFolders(dataFolder):
    if (os.path.isdir(dataFolder) == False):
        os.makedirs(dataFolder)


# plotting the states and its respective positions
def plot_states(trace_file, scenario, save_to, file_description, unit):
    trace = trace_file.copy()

    if unit == 'Kilometers':
        trace['x'] = trace['x'].apply(lambda x: x / 1000)
        trace['y'] = trace['y'].apply(lambda x: x / 1000)

    mask = trace['state'] == ""
    df_trajetory = trace[mask]
    df_states = trace[~mask]

    df = df_states

    # converting states to int
    states_temp = df['state'].tolist()
    states_temp_new = []
    for item in states_temp:
        if item == 'Base':
            states_temp_new.append(item)
        else:
            states_temp_new.append(int(item))
    df['state'] = states_temp_new

    # groups = df.groupby('state')
    groups = df.groupby(['state', 'node'])

    # state_color = ['red', 'gold', 'khaki', 'darkkhaki', 'darkseagreen', 'darkgreen']
    state_color = ['#CC0000', '#FFE66C', '#EBD367', '#D0B100', '#2B8C48', '#005E25']

    # Plot
    fig, ax = plt.subplots()
    fig.set_size_inches(5.5, 5.5)  # , forward=True)
    # ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
    # for name, group in groups:
    #     if name=='Base':
    #         ax.plot(group.x, group.y, color="purple", marker="^", linestyle='', ms=14, label=name)
    #     else:
    #         ax.plot(group.x, group.y, marker='o', linestyle='', ms=6, label=name, color = state_color[int(name)])

    for name, group in groups:
        if name[0] == 'Base':
            ax.plot(group.x, group.y, color="purple", marker="^", linestyle='', ms=14)  # , label=name[0])
        else:
            if name[1] == 0:
                ax.plot(group.x, group.y, marker='o', linestyle='', ms=6, label=name[0],
                        color=state_color[int(name[0])])
            elif name[1] == 1:
                ax.plot(group.x, group.y, marker='*', linestyle='', ms=6, color=state_color[int(name[0])])
            elif name[1] == 2:
                ax.plot(group.x, group.y, marker='d', linestyle='', ms=6, color=state_color[int(name[0])])
            else:
                ax.plot(group.x, group.y, marker=str(int(name[1])), linestyle='', ms=6, color=state_color[int(name[0])])

    ax.plot(df_trajetory.x, df_trajetory.y, marker='o', linestyle='', ms=1, label="")

    # Put a legend below current axis
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
    #          fancybox=True, shadow=True, fontsize=16, ncol=3)
    # ax.set_xlim([0, 300])
    # ax.set_ylim([0, 300])
    # ax.legend(loc='lower right',fontsize=14,ncol=1,handletextpad=0.01)
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),columnspacing=.1,
    #          fontsize=16,ncol=7,handletextpad=-.5, fancybox=False, shadow=False)
    leg = ax.legend(loc='best', columnspacing=.3,
                    fontsize=18, ncol=3, handletextpad=-.6, fancybox=False, shadow=False,
                    title=r'$\bf{States}$', title_fontsize=16)
    # leg.set_title('States', prop={'size': 14})
    # leg._legend_box.align = "left"
    # ax.legend(markerfirst=False)

    if unit == 'Kilometers':
        plt.xlabel('Kilometers', fontsize=20)
        plt.ylabel('Kilometers', fontsize=20)
    else:
        plt.xlabel('Meters', fontsize=20)
        plt.ylabel('Meters', fontsize=20)
    plt.xticks(fontsize=18, rotation=0)
    # plt.xticks(np.arange(50, 255, 50), fontsize=18, rotation=0)
    plt.yticks(fontsize=18, rotation=0)

    # plt.xticks(np.arange(min(df.x), max(df.x) + 1, 10))
    # plt.yticks(np.arange(min(df.y), max(df.y) + 1, 10))
    plt.grid(color='gray', linestyle='dashed')
    # plt.show(block=False)
    fig.tight_layout()
    # Shrink current axis's height by 10% on the bottom
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0 + box.height * -0.05,
    #                 box.width, box.height * 0.1])

    groups = df.groupby(['node'])
    for name, group in groups:
        if group.state.values.any() != 'Base':
            # ax.annotate(name, xy=(group.x[0], group.y[0]), xytext=(group.x[0] + 0.2, group.y[0] + 0.2),
            #             arrowprops=dict(facecolor='black', shrink=0.05))
            ax.annotate('Node ' + str(int(name) + 1), fontsize=16,
                        xy=(group.x.tail(1), group.y.tail(1)), xycoords='data',
                        xytext=(random.randint(-100, 00), random.randint(-100, 00)), textcoords='offset points',
                        bbox=dict(boxstyle="round", fc="0.8"),
                        arrowprops=dict(arrowstyle="->"))  # ,connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        else:
            ax.annotate('Command Post', fontsize=16,
                        xy=(group.x.tail(1), group.y.tail(1)), xycoords='data',
                        xytext=(40, -40), textcoords='offset points',
                        bbox=dict(boxstyle="round", fc="0.8"),
                        arrowprops=dict(arrowstyle="->"))

    plt.show()

    creatingFolders(save_to + "img/")

    fig.savefig(save_to + "img/" + "Trace_" + scenario.split('.')[0] + file_description + ".pdf", bbox_inches='tight',
                dpi=300)

    plt.close()


def plot_animated_states(trace_file, scenario, save_to, file_description, unit):
    trace = trace_file.copy()

    if unit == 'Kilometers':
        trace['x'] = trace['x'].apply(lambda x: x / 1000)
        trace['y'] = trace['y'].apply(lambda x: x / 1000)

    mask = trace['state'] == ""
    df_trajetory = trace[mask]
    df_states = trace[~mask]

    df = df_states

    # converting states to int
    states_temp = df['state'].tolist()
    states_temp_new = []
    for item in states_temp:
        if item == 'Base':
            states_temp_new.append(item)
        else:
            states_temp_new.append(int(item))
    df['state'] = states_temp_new

    for i in range(0, len(df), 3):

        # groups = df.groupby('state')
        groups = df.iloc[0:i, :].groupby('state')

        # state_color = ['red', 'gold', 'khaki', 'darkkhaki', 'darkseagreen', 'darkgreen']
        state_color = ['#CC0000', '#FFE66C', '#EBD367', '#D0B100', '#2B8C48', '#005E25']

        # Plot
        fig, ax = plt.subplots()
        fig.set_size_inches(5.5, 4.5, forward=True)

        groups_base = df.groupby('state')
        for name, group in groups_base:
            if name == 'Base':
                ax.plot(group.x, group.y, color="purple", marker="^", linestyle='', ms=14, label=name)

        # ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
        for name, group in groups:
            if name != 'Base':
                ax.plot(group.x, group.y, marker='o', linestyle='', ms=6, label=name, color=state_color[int(name)])

        ax.plot(df_trajetory.x, df_trajetory.y, marker='o', linestyle='', ms=1, label="")

        # Put a legend below current axis
        # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
        #          fancybox=True, shadow=True, fontsize=16, ncol=3)

        # ax.set_xlim(0, 50)
        # ax.set_ylim(0, 50)
        ax.set_xlim([int(np.min(df['x']) - .5), int(np.max(df['x']) + 2)])
        ax.set_ylim([int(np.min(df['y']) - .5), int(np.max(df['y']) + 2)])

        # ax.legend(loc='lower right',fontsize=14,ncol=1,handletextpad=0.01)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.20), columnspacing=.1,
                  fontsize=16, ncol=7, handletextpad=-.5, fancybox=False, shadow=False)
        if unit == 'Kilometers':
            plt.xlabel('Kilometers', fontsize=18)
            plt.ylabel('Kilometers', fontsize=18)
        else:
            plt.xlabel('Meters', fontsize=18)
            plt.ylabel('Meters', fontsize=18)
        plt.xticks(fontsize=18, rotation=0)
        # plt.xticks(np.arange(50, 255, 50), fontsize=18, rotation=0)
        plt.yticks(fontsize=18, rotation=0)

        # plt.xticks(np.arange(min(df.x), max(df.x) + 1, 10))
        # plt.yticks(np.arange(min(df.y), max(df.y) + 1, 10))
        plt.grid(color='gray', linestyle='dashed')
        # plt.show(block=False)
        fig.tight_layout()
        # Shrink current axis's height by 10% on the bottom
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * -0.05,
                         box.width, box.height * 0.1])

        plt.show()

        creatingFolders(save_to + "img/gif/")

        # fig.savefig(save_to + "img/" + "Trace_" + scenario.split('.')[0] + file_description + ".pdf",
        #            bbox_inches='tight', dpi=300)
        fig.savefig(save_to + "img/gif/" + '{0:05}'.format(len(df.iloc[0:i, :])) + ".png", bbox_inches='tight', dpi=50)

        plt.close()

    # creating a gif file
    # filepaths
    fp_in = save_to + "img/gif/*.png"
    fp_out = save_to + "img/gif/Trace_" + scenario.split('.')[0] + file_description + ".gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=100, loop=0, quality=100, optimize=False)

    # remove the list of figures
    files = [f for f in os.listdir(save_to + "img/gif/") if os.path.isfile(save_to + "img/gif/" + f)]
    for f in files:
        if f.endswith(('.png')):  # This will only look at files ending with the above extensions!
            os.remove(save_to + "img/gif/" + f)


# reading trace files
def get_trace(trace_file, csv):
    if csv == "csv":
        trace = pd.read_csv(trace_file, sep=',')
        trace = trace[['node', 'x', 'y', 'time']]
    else:
        file_ = open(trace_file, 'r')
        raw_data = file_.readlines()
        file_.close()

        x = []
        y = []
        t = []
        node = []
        # trace = []
        for line in range(0, len(raw_data)):
            col = raw_data[line].split(" ")
            for elem in range(0, len(col), 3):
                t.append(col[elem])
                x.append(float(col[elem + 1]))
                y.append(float(col[elem + 2]))
                node.append(int(line))
                # trace.append(str(col[elem+1]) + "," + str(col[elem+2]) + "," + str(col[elem]))

        # Create a DataFrame object
        trace = pd.DataFrame(columns=['node', 'x', 'y', 'time'])
        trace['node'] = node
        trace['x'] = x
        trace['y'] = y
        trace['time'] = t

    # trace = pd.DataFrame(dict(x=x, y=y, time=t))

    return (trace)


# getting the correspondent state based on a location
def datarate_match(trace, rings, center):
    nodeList = trace[['x', 'y']]  # trace.iloc[:, 1:3]
    # node = [[str(center), str(center)]]
    node = [[(center[0]), (center[1])]]

    # for line in range(0, len(trace)):
    #    col = trace[line].split(",")
    #    nodeList.append([col[0],col[1]])
    # node.append([str(center), str(center)])
    # dist = scipy.spatial.distance.cdist(node,nodeList)
    node_distance = cdist(nodeList, node, 'euclidean')
    node_datarate = []
    i = 0
    for dist in node_distance:
        for key in rings:
            lim_inf = float(rings[key].split(",")[0])
            lim_sup = float(rings[key].split(",")[1])
            if lim_inf <= dist <= lim_sup:
                node_datarate.append(key)
                break

        print(str(i) + ' state ' + str(node_datarate[i]) + ' distance ' + str(dist))
        i = i + 1

    trace['state'] = node_datarate
    # trace['dist_nodes'] = node_distance
    # print(trace)

    return trace


# linear interpolation
def lerp(v0, v1, i):
    return v0 + i * (v1 - v0)


# creating n points between x and y using linear interpolation
def getEquidistantPoints(trace, n):
    node_id = trace.loc[0, 'node']
    new_trace = pd.DataFrame(columns=trace.columns.values)
    for line in range(1, len(trace)):
        x = trace.loc[line - 1, 'x']
        y = trace.loc[line - 1, 'y']
        t = trace.loc[line - 1, 'time']

        x_1 = trace.loc[line, 'x']
        y_1 = trace.loc[line, 'y']
        t_1 = trace.loc[line, 'time']

        time_interval = float(t_1) - float(t)
        current_time = float(t)
        for i in range(n):
            p1 = lerp(float(x), float(x_1), 1. / n * i)
            p2 = lerp(float(y), float(y_1), 1. / n * i)

            new_trace = new_trace.append({'node': node_id, 'x': p1, 'y': p2, 'time': current_time}, ignore_index=True)

            add_time = time_interval / n
            current_time = current_time + add_time

        # filling the last state
        if line == len(trace) - 1:
            new_trace = new_trace.append({'node': node_id, 'x': x_1, 'y': y_1, 'time': t_1}, ignore_index=True)

    return new_trace


# computing distance and speed of such a trace
def add_dist_speed(trace):
    trace['distance'] = pd.Series(0)
    trace['speed'] = pd.Series(0)
    trace['acc'] = pd.Series(0)

    for line in range(1, len(trace)):
        x = trace.loc[line - 1, 'x']  # trace.iloc[line-1,1]
        y = trace.loc[line - 1, 'y']  # trace.iloc[line-1,2]
        t = trace.loc[line - 1, 'time']  # trace.iloc[line-1,3]

        x_1 = trace.loc[line, 'x']  # trace.iloc[line,1]
        y_1 = trace.loc[line, 'y']  # trace.iloc[line,2]
        t_1 = trace.loc[line, 'time']  # trace.iloc[line,3]

        # dist = cdist([node], [node_1], 'euclidean')
        dist = round(np.math.sqrt((float(x_1) - float(x)) ** 2 + (float(y_1) - float(y)) ** 2), ndigits=3)
        if float(t_1) - float(t) != 0:
            speed = round(dist / (float(t_1) - float(t)), ndigits=3)
        else:
            speed = 0

        trace.loc[line, 'distance'] = dist  # trace.iloc[line, 6] = speed
        trace.loc[line, 'speed'] = speed  # trace.iloc[line, 6] = speed
        s = trace.loc[line - 1, 'speed']  # trace.iloc[line - 1, 6]
        s_1 = trace.loc[line, 'speed']

        if float(t_1) - float(t) != 0:
            acc = round((float(s_1) - float(s)) / (float(t_1) - float(t)), ndigits=3)
        else:
            acc = 0

        trace.loc[line, 'acc'] = acc  # trace.iloc[line, 7] = acc

    return trace


# creating a static node as a reference to other nodes
def add_static_node(trace, node_reference, number_of_nodes):
    end_time = pd.to_numeric(trace['time']).max()

    static_node = pd.DataFrame(columns=trace.columns.values)
    static_node = static_node.append(
        {'node': int(number_of_nodes), 'x': node_reference[0], 'y': node_reference[1], 'time': 0, 'state': "Base"},
        ignore_index=True)
    static_node = static_node.append(
        {'node': int(number_of_nodes), 'x': node_reference[0] + 0.1, 'y': node_reference[1] + 0.1, 'time': end_time,
         'state': "Base"},
        ignore_index=True)
    static_node = pd.concat([trace, static_node])

    return static_node


if __name__ == '__main__':

    read_from = os.path.dirname(os.path.abspath(__file__)) + '/data/bonn_motion/'
    save_to = os.path.dirname(os.path.abspath(__file__)) + '/data/uhf/'

    creatingFolders(save_to)

    # scenario = 'GaussMarkov.csv'#'GaussMarkov.movements'
    # scenario = 'Boundless.csv'#'Boundless.movements'
    # scenario = 'ManhattanGrid.csv'
    # scenario = 'RandomWalk.csv'
    # scenario = 'ProbRandomWalk.csv'
    # scenario = 'RandomWaypoint.movements'#'RandomWaypoint.csv'

    # VHF scenarios and reference point
    # scenario = 'GaussMarkov_VHF.csv' ; reference_point = [20000, 0000]
    # scenario = 'ManhattanGrid_VHF.csv'; reference_point = [0000, 20000]
    # scenario = 'ManhattanGrid2_VHF.csv'; reference_point = [0000, 32000]
    # scenario = 'ProbRandomWalk_VHF.csv' ; reference_point = [20000, 0000] # traces['y'] = traces['y'].apply(lambda x: x * 12)
    # scenario = 'RandomWaypoint_VHF.csv' ; reference_point = [0000, 20000]

    # UHF scenarios and reference point
    # scenario = 'ManhattanGrid_UHF.csv'
    # reference_point = [200, 5000]
    # scenario = 'GaussMarkov_UHF.csv'
    scenario = 'GaussMarkov2_UHF.csv'  # (nodes move together)
    reference_point = [500, 2500]
    # scenario = 'GaussMarkov_WIFI.csv'
    # reference_point = [25, 140]

    file_description = "_NtoN_"  # "" # node to base station ("") or node to node ("_NtoN_")

    # position x and y are the same
    # reference_point = 120
    # reference_point = [0000, 20000]
    # defines the radius distance (10m, 100m,1000m...)
    magnitude = 200  # 10-WIFI  200-UHF 2000-VHF

    datarate_rings = dict(
        [(5, "0.0," + str(2 * magnitude)),
         (4, str(2 * magnitude + 0.00001) + "," + str(4 * magnitude)),
         (3, str(4 * magnitude + 0.00001) + "," + str(6 * magnitude)),
         (2, str(6 * magnitude + 0.00001) + "," + str(8 * magnitude)),
         (1, str(8 * magnitude + 0.00001) + "," + str(10 * magnitude)),
         (0, str(10 * magnitude + 0.00001) + "," + str(50 * magnitude))])

    traces = get_trace(read_from + scenario, scenario.split(".")[1])

    # temporary ajustment for extend the communication area
    # instead of generate those scenarios again and redo experiments
    # traces['x'] = traces['x'].apply(lambda x: x * 100)
    # traces['y'] = traces['y'].apply(lambda x: x * 12)

    trace_node = traces.groupby('node')

    trace_nodes = pd.DataFrame()
    for n in trace_node.groups:
        trace = trace_node.get_group(n).reset_index()
        trace.drop(['index'], axis='columns', inplace=True)
        # trace = getEquidistantPoints(trace, 5)

        trace = datarate_match(trace, datarate_rings, reference_point)

        trace = add_dist_speed(trace)

        # plot_states(trace)

        # trace.to_csv(save_to +'node'+str(n)+"_"+scenario.replace(".movements","")+'.csv', mode='w', index=False)

        trace_nodes = pd.concat([trace_nodes, trace])

    # adding static node
    trace_nodes = add_static_node(trace_nodes, reference_point, n + 1)

    # showing the trace files in 2-dimensions
    # plot_animated_states(trace_nodes,scenario,save_to,file_description,'Kilometers')
    plot_states(trace_nodes, scenario, save_to, '', 'Kilometers')

    # saving the trace
    # trace_nodes.to_csv(save_to +'Trace_'+scenario.replace(".movements","")+'.csv', index=False)
    trace_nodes.to_csv(save_to + 'Trace_' + scenario.split('.')[0] + '.csv', index=False)

    if file_description == '_NtoN_':
        df_grouped = trace_nodes.groupby(['node'])

        df_node1 = df_grouped.get_group(0).reset_index()
        df_node1.drop(['index'], axis='columns', inplace=True)
        df_node2 = df_grouped.get_group(1).reset_index()
        df_node2.drop(['index'], axis='columns', inplace=True)
        df_node3 = df_grouped.get_group(2).reset_index()
        df_node3.drop(['index'], axis='columns', inplace=True)

        # node_distance = cdist(df_node1[['x', 'y']], df_node2[['x', 'y']], 'euclidean')

        for row in range(0, len(df_node1)):
            node_distance = cdist([(df_node1.loc[row, 'x'], df_node1.loc[row, 'y'])],
                                  [(df_node2.loc[row, 'x'], df_node2.loc[row, 'y'])], 'euclidean')

            for key in datarate_rings:
                lim_inf = float(datarate_rings[key].split(",")[0])
                lim_sup = float(datarate_rings[key].split(",")[1])
                if node_distance >= lim_inf and node_distance <= lim_sup:
                    df_node1.loc[row, 'state'] = key
                    df_node2.loc[row, 'state'] = key
                    break

        trace_nodes = pd.concat([df_node1, df_node2, df_node3])

        plot_states(trace_nodes, scenario, save_to, file_description, 'Kilometers')

        # plot_animated_states(trace_nodes,sequence_type+gaps_type+trace_type+file_description,save_to,'Kilometers')

        # saving the trace
        trace_nodes.to_csv(save_to + 'Trace_' + scenario.split('.')[0] + file_description + '.csv', index=False)

        # exporting trace to be analyzed in Bonn motion
        # with open(save_to+'node'+str(n)+"_"+gaps_type+trace_type+'_bm.dat', 'w') as filehandle:
        #    filehandle.writelines("%s " % place for place in trace_bonn_motion)

    sys.exit()
