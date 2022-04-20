##################################################
## stript to generate positions based on rings
##################################################
## Author: Paulo H. L. Rettore
## Status: open
## Date: 01/07/2020
##################################################
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sys
import scipy
from itertools import cycle
from numpy.random.mtrand import uniform
from scipy.spatial.distance import cdist
import itertools
from model_b1 import ever_changing_sequence
import glob
from PIL import Image


# create folder
def creatingFolders(dataFolder):
    if (os.path.isdir(dataFolder) == False):
        os.makedirs(dataFolder)


# plotting the states and its respective positions
def plot_states(trace_file, scenario, save_to, unit):
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

    groups = df.groupby(['state', 'node'])

    # state_color = ['red', 'gold', 'khaki', 'darkkhaki', 'darkseagreen', 'darkgreen']
    state_color = ['#CC0000', '#FFE66C', '#EBD367', '#D0B100', '#2B8C48', '#005E25']

    # Plot
    fig, ax = plt.subplots()
    fig.set_size_inches(5.5, 5, forward=True)
    # ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
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

    # ax.set_xlim(0, 50)
    # ax.set_ylim(0, 50)
    # ax.set_xlim([int(np.min(df['x'])), int(np.max(df['x']) + 5)])
    # ax.set_ylim([int(np.min(df['y'])), int(np.max(df['y']) + 5)])

    # ax.legend(loc='lower right',fontsize=14,ncol=1,handletextpad=0.01)
    # leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.20),columnspacing=.1,
    #          fontsize=16,ncol=7,handletextpad=-.5, fancybox=False, shadow=False)#, title=r'$\bf{States}$')
    leg = ax.legend(loc='center right', columnspacing=.3,
                    fontsize=18, ncol=2, handletextpad=-.6, fancybox=False, shadow=False,
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
                        xytext=(random.randint(-20, 100), random.randint(-100, 30)), textcoords='offset points',
                        bbox=dict(boxstyle="round", fc="0.8"),
                        arrowprops=dict(arrowstyle="->"))  # ,connectionstyle="angle,angleA=0,angleB=90,rad=10"))
        else:
            ax.annotate('Command Post', fontsize=16,
                        xy=(group.x.tail(1), group.y.tail(1)), xycoords='data',
                        xytext=(20, 80), textcoords='offset points',
                        bbox=dict(boxstyle="round", fc="0.8"),
                        arrowprops=dict(arrowstyle="->"))

    plt.show()

    creatingFolders(save_to + "img/")

    fig.savefig(save_to + "img/" + scenario + ".pdf", bbox_inches='tight', dpi=300)

    plt.close()


# plotting the states and its respective positions
def plot_animated_states(trace_file, scenario, save_to, unit):
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
        ax.set_xlim([int(np.min(df['x'])), int(np.max(df['x']) + 5)])
        ax.set_ylim([int(np.min(df['y'])), int(np.max(df['y']) + 5)])

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

        # fig.savefig(save_to+"img/" +scenario+".pdf",bbox_inches='tight',dpi=300)
        fig.savefig(save_to + "img/gif/" + '{0:05}'.format(len(df.iloc[0:i, :])) + ".png", bbox_inches='tight', dpi=50)

        plt.close()

    # creating a gif file
    # filepaths
    fp_in = save_to + "img/gif/*.png"
    fp_out = save_to + "img/gif/" + scenario + ".gif"

    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=100, loop=0, quality=100, optimize=False)

    # remove the list of figures
    files = [f for f in os.listdir(save_to + "img/gif/") if os.path.isfile(save_to + "img/gif/" + f)]
    for f in files:
        if f.endswith(('.png')):  # This will only look at files ending with the above extensions!
            os.remove(save_to + "img/gif/" + f)


# creating a sequence of states based on a pendulum
def generatePendulumStates(n_states, elements):
    state_sequence = []

    rev_elements = elements[::-1]
    elements = elements + rev_elements[1:len(rev_elements) - 1]

    i = 0
    pool = cycle(elements)
    for item in pool:
        state_sequence.append(item)
        if i == n_states:
            break
        i = i + 1

    print(state_sequence)
    return state_sequence


# creating a sequence of states based on normal distrib. with prob.
def generateRandomStates(n_states, elements, probabilities):
    state_sequence = np.random.choice(elements, n_states, p=probabilities)
    print(state_sequence)
    return state_sequence


# selecting the next node based on the shorsted distance
def closestNode(node, innerRing, outerRing, center, sample):
    nodeList = []
    while (len(nodeList) <= sample):
        x, y = generatePoints(innerRing, outerRing, center)
        nodeList.append([x, y])

    # dist = scipy.spatial.distance.cdist(node,nodeList)
    shortest_node = nodeList[cdist([node], nodeList, 'euclidean').argmin()]
    return shortest_node


# creating a position based on rings
def generatePoints(innerRing, outerRing, center):
    theta = uniform(0, 2 * np.pi)
    r = np.sqrt(uniform(float(innerRing) ** 2, float(outerRing) ** 2))  # draw from sqrt distribution

    # meaning that the reference has a different location of 0.0 x 0.0
    if center[0] != 0 and center[1] != 0:
        x_coord = center[0] + r * np.cos(theta)
        y_coord = center[1] + r * np.sin(theta)
        if x_coord < 0.0 or y_coord < 0.0:
            while (x_coord < 0.0 or y_coord < 0.0):
                theta = uniform(0, 2 * np.pi)
                r = np.sqrt(uniform(float(innerRing) ** 2, float(outerRing) ** 2))  # draw from sqrt distribution
                x_coord = center[0] + r * np.cos(theta)
                y_coord = center[1] + r * np.sin(theta)
    else:
        # positive values - this cannot follows a normal distr.
        # x_coord = r * abs(np.cos(theta))
        # y_coord = r * abs(np.sin(theta))
        # or - This follows a normal distr.
        while (x_coord < 0.0 or y_coord < 0.0):
            theta = uniform(0, 2 * np.pi)
            r = np.sqrt(uniform(float(innerRing) ** 2, float(outerRing) ** 2))  # draw from sqrt distribution
            x_coord = r * np.cos(theta)
            y_coord = r * np.sin(theta)

    return round(x_coord, ndigits=2), round(y_coord, ndigits=2)


# getting the correspondent state based on a location
def datarate_match(x, y, rings, center):
    nodeList = [[x, y]]
    node = [[(center[0]), (center[1])]]

    node_distance = cdist(nodeList, node, 'euclidean')
    node_datarate = 0
    # i = 0
    for dist in node_distance:
        for key in rings:
            lim_inf = float(rings[key].split(",")[0])
            lim_sup = float(rings[key].split(",")[1])
            if lim_inf <= dist <= lim_sup:
                node_datarate = key
                break
        # print(str(i) +' state '+str(node_datarate[i]))
        # i = i +1

    # trace['state'] = node_datarate
    # print(trace)

    return node_datarate


# linear interpolation
def lerp(v0, v1, i):
    return v0 + i * (v1 - v0)


# creating n points between x and y using linear interpolation
def getEquidistantPoints(trace, n, rings, center):
    node_id = trace.loc[0, 'node']
    new_trace = pd.DataFrame(columns=trace.columns.values)
    for line in range(1, len(trace)):
        x = trace.loc[line - 1, 'x']
        y = trace.loc[line - 1, 'y']
        t = trace.loc[line - 1, 'time']
        s = trace.loc[line - 1, 'state']

        x_1 = trace.loc[line, 'x']
        y_1 = trace.loc[line, 'y']
        t_1 = trace.loc[line, 'time']
        s_1 = trace.loc[line, 'state']

        time_interval = float(t_1) - float(t)
        current_time = float(t)
        for i in range(n):
            p1 = lerp(float(x), float(x_1), 1. / n * i)
            p2 = lerp(float(y), float(y_1), 1. / n * i)
            if i == 0:
                new_trace = new_trace.append({'node': node_id, 'x': p1, 'y': p2, 'time': current_time, 'state': s},
                                             ignore_index=True)
            else:
                state = datarate_match(p1, p2, rings, center)
                new_trace = new_trace.append({'node': node_id, 'x': p1, 'y': p2, 'time': current_time, 'state': state},
                                             ignore_index=True)
            add_time = time_interval / n
            current_time = current_time + add_time

        # filling the last state
        if line == len(trace) - 1:
            new_trace = new_trace.append({'node': node_id, 'x': x_1, 'y': y_1, 'time': t_1, 'state': s_1},
                                         ignore_index=True)

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


# creating traces
def creatingTraces(trace_type, motion_type, state_sequence, state_time_interval, state_time,
                   reference_point, n, datarate_rings, n_interpolation):
    # creating a sequence of positions
    trace = pd.DataFrame(columns=['node', 'x', 'y', 'time', 'state', 'distance', 'speed', 'acc'])
    trace_bonn_motion = []
    changes = []
    x = np.zeros(number_of_states)
    y = np.zeros(number_of_states)
    for i in range(len(state_sequence)):
        # random generation based on short distance
        if trace_type == "_Shortest":
            if i == 0:
                x, y = generatePoints(datarate_rings[state_sequence[i]].split(",")[0],
                                      datarate_rings[state_sequence[i]].split(",")[1], reference_point)
            else:
                node = [trace.loc[i - 1, 'x'], trace.loc[i - 1, 'y']]
                x, y = closestNode(node, datarate_rings[state_sequence[i]].split(",")[0],
                                   datarate_rings[state_sequence[i]].split(",")[1], reference_point, 1000)
        else:
            # random generation
            x, y = generatePoints(datarate_rings[state_sequence[i]].split(",")[0],
                                  datarate_rings[state_sequence[i]].split(",")[1], reference_point)

        if i == 0:  # first point shows in time 0
            trace = trace.append({'node': int(n), 'x': x, 'y': y, 'time': 0, 'state': state_sequence[i]},
                                 ignore_index=True)
            trace_bonn_motion.append("0 " + str(x) + " " + str(y))
        else:
            trace = trace.append({'node': int(n), 'x': x, 'y': y, 'time': state_time, 'state': state_sequence[i]},
                                 ignore_index=True)
            trace_bonn_motion.append(str(state_time) + " " + str(x) + " " + str(y))
            state_time = state_time + state_time_interval

    if motion_type == "_Filled":
        trace = getEquidistantPoints(trace, n_interpolation, datarate_rings, reference_point)

    trace = add_dist_speed(trace)

    # plot_states(trace)

    return trace


if __name__ == '__main__':

    save_to = os.path.dirname(os.path.abspath(__file__)) + '/data/uhf/'
    creatingFolders(save_to)

    # setting state time
    state_start_time = 30
    state_time_interval = 40  # 180 #360 #20
    # creating a sequence of states
    number_of_states = 16
    number_of_nodes = 2
    # position x and y are the same
    reference_point = [2000, 5000]  # [2000, 5000] UHF [100, 250]#WIFI [24000,24000]#VHF [120,120] # [220,220]
    # defines the radius distance (10m, 100m,1000m...)
    magnitude = 200  # 200  # UHF 2000# VHF 10 # Wifi
    # number of points to interpolate
    n_interpolation = 10
    # type of trace
    trace_type = "_Shortest"  # "_Shortest" or ""
    gaps_type = "_Filled"  # "_Filled" or ""
    sequence_type = 'Trace_Pendulum'  # 'Trace_Pendulum' # 'Trace_Random' # 'Trace_Markov'
    file_description = 'UHF'  # WIFI
    reference_node = "_NtoN_"  # "" # node to base station ("") or node to node ("_NtoN_")

    datarate_rings = dict(
        [(5, "0.0," + str(2 * magnitude)),
         (4, str(2 * magnitude + 0.0001) + "," + str(4 * magnitude)),
         (3, str(4 * magnitude + 0.0001) + "," + str(6 * magnitude)),
         (2, str(6 * magnitude + 0.0001) + "," + str(8 * magnitude)),
         (1, str(8 * magnitude + 0.0001) + "," + str(10 * magnitude)),
         (0, str(11 * magnitude + 0.0001) + "," + str(13 * magnitude))])

    # if number_of_nodes == 1:
    # np.random.seed(356345)
    # np.random.seed(410)
    # np.random.seed(10) # good seed for Trace_Pendulum trace with 15 nodes
    np.random.seed(549)

    # creating a sequence of states based on probabilities
    if sequence_type == 'Trace_Pendulum':
        state_sequence = generatePendulumStates(number_of_states, [5, 4, 3, 2, 1, 0, 0, 0, 0])

    # creating a sequence of states based on probabilities
    if sequence_type == 'Trace_Random':
        state_sequence = generateRandomStates(number_of_states, [0, 1, 2, 3, 4, 5], [0.1, 0.2, 0.3, 0.1, 0.1, 0.2])

    if sequence_type == 'Trace_Markov':
        '''
        Uncomment the line of code if you want to change to a markov based sequence of 20 states.
        If you want to change the number of states you can do this in ever-changing/communication_scenario/config.py.
        Just change the parameters for the simple_mobility_config and run the file. This updates the config file.
        If you want to plot your Markov chain and the respective scenario just rund ever-changing_sequence as main before.
        This creates a plot of the scenario in the img folder.
        '''
        experiment, comm_scenario, state_sequence = ever_changing_sequence.create_sequence('markov_pattern_config')
        # Plot the transition matrices for an experiment
        print(experiment.plot_transition_matrices())
        print(state_sequence)

    # computing data rate and statistics based on the reference node (base station or the other node)

    trace_nodes = pd.DataFrame()
    for n in range(0, number_of_nodes):
        trace = creatingTraces(trace_type, gaps_type, state_sequence, state_time_interval, state_start_time,
                               reference_point, n, datarate_rings, n_interpolation)

        trace_nodes = pd.concat([trace_nodes, trace])

    # adding static node
    trace_nodes = add_static_node(trace_nodes, reference_point, number_of_nodes)

    # adding static node
    # trace_nodes = add_static_node(trace_nodes,[220,80],2)

    plot_states(trace_nodes, sequence_type + gaps_type + trace_type + '_NtoBS_' + file_description, save_to,
                'Kilometers')
    # plot_animated_states(trace_nodes,sequence_type+gaps_type+trace_type+file_description,save_to,'Kilometers')

    # saving the trace
    trace_nodes.to_csv(save_to + sequence_type + gaps_type + trace_type + '_NtoBS_' + file_description + '.csv',
                       index=False)

    # exporting trace to be analyzed in Bonn motion
    # with open(save_to+'node'+str(n)+"_"+gaps_type+trace_type+'_bm.dat', 'w') as filehandle:
    #    filehandle.writelines("%s " % place for place in trace_bonn_motion)
    # computing data rate and statistics based on the reference node (base station or the other node)

    if reference_node == '_NtoN_':
        df_grouped = trace_nodes.groupby(['node'])

        df_node1 = df_grouped.get_group(0).reset_index()
        df_node1.drop(['index'], axis='columns', inplace=True)
        df_node2 = df_grouped.get_group(1).reset_index()
        df_node2.drop(['index'], axis='columns', inplace=True)
        df_node3 = df_grouped.get_group(2).reset_index()
        df_node3.drop(['index'], axis='columns', inplace=True)

        for row in range(0, len(df_node1)):
            state_n2n = datarate_match(df_node1.loc[row, 'x'],
                             df_node1.loc[row, 'y'],
                             datarate_rings,
                             [df_node2.loc[row, 'x'],
                              df_node2.loc[row, 'y']])
            df_node1.loc[row,'state'] = state_n2n
            df_node2.loc[row, 'state'] = state_n2n
            # df_node2.loc[row, 'state'] = datarate_match(df_node2.loc[row, 'x'],
            #                                             df_node2.loc[row, 'y'],
            #                                             datarate_rings,
            #                                             [df_node1.loc[row, 'x'],
            #                                              df_node1.loc[row, 'y']])


        trace_nodes = pd.concat([df_node1, df_node2, df_node3])


        plot_states(trace_nodes, sequence_type + gaps_type + trace_type + reference_node + file_description, save_to,
                    'Kilometers')
        # plot_animated_states(trace_nodes,sequence_type+gaps_type+trace_type+file_description,save_to,'Kilometers')

        # saving the trace
        trace_nodes.to_csv(
            save_to + sequence_type + gaps_type + trace_type + reference_node + file_description + '.csv',
            index=False)

        # exporting trace to be analyzed in Bonn motion
        # with open(save_to+'node'+str(n)+"_"+gaps_type+trace_type+'_bm.dat', 'w') as filehandle:
        #    filehandle.writelines("%s " % place for place in trace_bonn_motion)
