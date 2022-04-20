from model_b1.datarate_to_trace import creatingFolders

try:
    import configparser
    import math
    import matplotlib.pyplot as plt
    import networkx as nx
    from graphviz import Digraph
    import pandas as pd
    import json
    import pickle as pickle
    from pprint import pprint
    import quantecon as qe
    import random
    import re
    import os
except ImportError:
    raise

class Experiment:


    def __init__(self,config_name=None):
        """
        Init method for the class to set parameters from config file used to generate the communicaiton
        scenario.
        :param config_file_name: Name of the config file that is used for the experiment
        """
        self._transition_matrix_names = []
        self._transition_matrix_file_path = ''
        self._communication_changes = []
        self._state_values = []
        self._initial_data_rate = ''
        self._number_steps = 0

        self._initial_transition_matrices = []
        self._markov_chains = {}
        self.dict = {}
        self._pendulum_pattern = []

        # Initialize the config from the config file
        if config_name is not None:
            self.__set_config(config_name)
            self.__set_parameters(config_name)
        pass

    def __set_config(self,config_name):
        # Initialize the config from the config file
        self.__config = configparser.ConfigParser()
        self.__config.read('ever_changing_sparse/communication_scenario/configs/config.ini')
        self.__config_name = config_name

    def __set_parameters(self,config_name):
        # Read variables from config file and set parameters that describe the experiment
        self._transition_matrix_names = self.__config[config_name]['transition_matrix_names'].split(",")
        self._transition_matrix_file_path = self.__config[config_name]['transition_matrix_file_path']
        self._communication_changes = self.__config[config_name]['scenario'].split(",")
        self._state_values = tuple(self.__config[config_name]['state_values'].split(","))
        if self.__config[config_name]['initial_datarate'] == 'rand':
            self._initial_data_rate = random.choice(self._state_values)
        else:
            self._initial_data_rate = self.__config[config_name]['initial_datarate']
        self._number_steps = self.__config[config_name]['number_steps'].split(",")

        # Load initial transition matrices create markov chains from the matrices and define the experiment
        self._initial_transition_matrices = self.__load_initial_matrices()
        self._markov_chains = self.__create_markov_chains()
        self.dict = self.create_experiment_dict()

        # Set pendulum pattern
        self._pendulum_pattern = self.__set_pendulum()

        # Set multiple for plotting

        self._multiple = self.__config[config_name]['multiple']

    def __set_pendulum(self):
        """
        Set the pendulum pattern for the experiment to default or as defined in config.
        """
        if self.__config[self.__config_name]['pendulum_pattern'] == None:
            return ['9.6 kbps','4.8 kbps','2.4 kbps','1.2 kbps','0.6 kbps','0.0 kbps','0.6 kbps',
                                     '1.2 kbps','2.4 kbps','4.8 kbps']
        else:
            return self.__config[self.__config_name]['pendulum_pattern'].split(",")

    def __load_initial_matrices(self):
        """
        Load the initial matrices from csv file transition_matrix_file_path.csv
        :return: list of matrices
        """
        #dir_path = os.path.dirname(os.path.realpath(__file__))

        matrices = []
        with open(self._transition_matrix_file_path, 'r') as file:
            content = file.read()
        # gets each matrix based on the pattern [[ ]]
        matrices_string = re.findall("\[([\d\s.\n\]\[]+)\]", content)
        # loops over each matrix
        for matrix_string in matrices_string:
            # parses each row of the matrix
            matrix_rows = re.findall("\[([\d\s.\n\]]+)\]", matrix_string)
            # gets all the numbers for each row of the matrix and remakes the matrix as a list of floats
            matrices.append([list(map(float, re.findall("\d+\.\d+", row))) for row in matrix_rows])

        return matrices

    def __create_markov_chains(self):
        """
        Create quantecon Markov chains from initial_transition_matrices using the state_values
        :return: dictionary of markov chains with names for the transition matrices
        """
        chains = {}
        count = 0
        for matrix in self._initial_transition_matrices:
            chains[self._transition_matrix_names[count]] = qe.MarkovChain(matrix,state_values=self._state_values)
            count = count +1
        return chains

    def compute_stationary_distributions(self,markov_chains):
        """
        Compute the stationary distributions for a set of markov chains
        :param markov_chains: List(MarkovChain)
        :return: stationary_distributions: List()
        """
        stationary_distributions = []
        for chain in markov_chains:
            stationary_distributions.append(stationary_distributions)
        return stationary_distributions

    @staticmethod
    def __get_markov_edges(p_df):
        """
            Convert a transition_matrix to pandas dataframe
            :return: edges of the graph representation of the MC
            """
        edges = {}
        for col in p_df.columns:
            for idx in p_df.index:
                edges[(idx,col)] = p_df.loc[idx,col]
        return edges

    def __convert_matrix_pd(self,transition_matrix):
        """
        Convert a transition_matrix to pandas dataframe
        :param transition_matrix: Transition matrix
        :return: pandas dataframe representation of a transition matrix
        """
        p_df = pd.DataFrame(columns=self._state_values, index=self._state_values)
        for i in range(len(transition_matrix)):
            p_df.loc[self._state_values[i]] = transition_matrix[i]
        return p_df


    def plot_chain(self,transition_matrix) :
        """
        Plot a graph representation of the transition matrix of a markov_chain
        :param transition_matrix: Transition matrix
        """
        p_df = self.__convert_matrix_pd(transition_matrix)
        edges_wts = self.__get_markov_edges(p_df)

        fig, ax = plt.subplots()

        print("Plot Markov Chain using the following representation: ")
        pprint(edges_wts)

        state_color = ['#CC0000', '#FFE66C', '#EBD367', '#D0B100', '#2B8C48', '#005E25']

        # create graph object
        G = nx.MultiDiGraph(overlap=False)

        # nodes correspond to states
        G.add_nodes_from(self._state_values)
        print(f'Nodes:\n{G.nodes()}\n')

        # edges represent transition probabilities
        for k, v in edges_wts.items():
            tmp_origin, tmp_destination = k[0], k[1]
            G.add_edge(tmp_origin, tmp_destination, weight=round(v,ndigits=3), label=round(v,ndigits=3))
        print(f'Edges:')
        pprint(G.edges(data=True))


        pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='circo', root="0.0 kbps")
        pos['0.0 kbps'] = [40.946, 148.48]
        pos['0.6 kbps'] = [114.42, 275.75]
        pos['1.2 kbps'] = [261.38, 275.75]
        pos['2.4 kbps'] = [334.86, 148.48]
        pos['4.8 kbps'] = [261.38, 21.211]
        pos['9.6 kbps'] = [114.42, 21.211]

        labels = {}
        for node in G.nodes():
            # set the node name as the key and the label as its value
            if 'kbps' in node:
                labels[node] = node.replace('kbps','')
        # Now add labels to the nodes
        nx.draw_networkx_labels(G, pos, labels, font_size=20, font_color='black',font_weight='bold')


        # #nx.draw_networkx(G, pos, node_color=(range(6)), node_size=3200, cmap=plt.get_cmap('RdYlGn'),
        # #                 k=5 / math.sqrt(G.order()))
        nx.draw_networkx(G, pos, node_color=state_color, with_labels=False, node_size=3200)


        # create edge labels for jupyter plot but is not necessary
        edge_labels = {(n1, n2): d['label'] for n1, n2, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, font_size=16, edge_labels=edge_labels,
                                     alpha=.5, label_pos=0.73)
        dot = nx.drawing.nx_pydot.write_dot(G, 'model_B.dot')
        plt.show()



        ax.axis('off')
        fig.tight_layout()
        creatingFolders("ever_changing_sparse/communication_scenario/img/")
        fig.savefig("ever_changing_sparse/communication_scenario/img/" + self.__config_name.replace("_config",".pdf") , bbox_inches='tight', dpi=300)

    def plot_transition_matrices(self,transition_matrices=None):
        """
        Plot transition matrices.
        :param transition_matrices:
        """
        # If parameter is None set to default from instance
        if transition_matrices is None:
            transition_matrices = self._initial_transition_matrices

        for matrix in transition_matrices:
            self.plot_chain(matrix)

    def create_experiment_dict(self):
        """
        Creates dictionary for the experiment.
        :return: experiment description as dictionary holding the markov chains sorted by the communication_changes
        order with the respective markov_chain and the number of steps that the experiment should follow the transitions
        defined by markov_chain
        """
        experiment = {}
        experiment['initial_data_rate'] = self._initial_data_rate
        counter = 0
        for transition in self._communication_changes:
            if transition == 'pendulum':
                experiment[transition] = (self._pendulum_pattern,int(self._number_steps[counter]))
            else:
                experiment[transition] = (self._markov_chains[transition],int(self._number_steps[counter]))
        return experiment

    def save_experiment(self,file_name):
        """
        Save the experiment to pickle file for later usage.
        :param file_name: name of the destination .p pickle file without .p
        """
        with open(file_name+'.p', 'wb') as fp:
            pickle.dump(self, fp, protocol=pickle.HIGHEST_PROTOCOL)


