# Import libraries

try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    import networkx as nx
    import pandas as pd
    import random
except ImportError:
    raise


class CommunicationScenario:

    def __init__(self, experiment):
        """
        Init method for the class to set parameters from config file used to generate the communicaiton
        scenario.
        :param config_file_name: Name of the config file that is used for the experiment
        """
        # Initialize variables for the communication scenario

        self.experiments = [experiment]
        self.experiment_id = 0
        self.nxn_dim_plot = int(experiment._multiple)
        self.initial_data_rate = experiment._initial_data_rate
        self.sequence_transition_matrices = experiment._communication_changes
        self.markov_chains = experiment._markov_chains
        self.pendulum_pattern = experiment._pendulum_pattern
        self._state_values = experiment._state_values
        self._state_numbers = self.__map_kbps_to_numbers(self._state_values)
        self.sequence = []

    def change_pendulum_pattern(self, pendulum_pattern):
        """
        Change the pendulum pattern.
        :param pendulum_pattern: New pendulum pattern
        """
        self.pendulum_pattern = pendulum_pattern

    def add_new_experiment(self, experiment):
        """
        Add a new experiment to the list of experiments
        :param experiment: experiment to add to list of experiments
        """
        self.experiments.append(experiment)

    def set_experiment_id(self, new_id):
        """
        Set the experiment id to new_id to change the actual experiment.
        :param id: new experiment id
        """
        self.experiment_id = new_id

    def update_parameters(self,experiment,experiment_id=None):
        """
        Update CommunicationScenario parameters, if the scenario is updated with a new experiment.
        :param experiment: New experiment
        """
        self.add_new_experiment(experiment)

        if experiment_id is None:
            experiment_id = len(self.experiments)-1
        self.set_experiment_id(experiment_id)

        if len(self.sequence) > 0:
            self.initial_data_rate = self.sequence[-1]
        else:
            self.initial_data_rate = experiment._initial_data_rate

        self.sequence_transition_matrices = experiment._communication_changes
        self.markov_chains = experiment._markov_chains

    def __map_kbps_to_numbers(self,state_values):
        """
        Map kbps data rates to state numbers.
        :param states: list of possible states
        :return: list of state numbers
        """
        numbers = []
        counter = 0
        for state in state_values:
            if state == '0.0 kbps':
                numbers.append(0)
            elif state == '0.6 kbps':
                numbers.append(1)
            elif state == '1.2 kbps':
                numbers.append(2)
            elif state == '2.4 kbps':
                numbers.append(3)
            elif state == '4.8 kbps':
                numbers.append(4)
            elif state == '9.6 kbps':
                numbers.append(5)
            counter = counter + 1
        return numbers

    def create_sequence(self, markov_chain_name, markov_chain, sequence_length, initial_state=None):
        """
        Create a sequence of states from a markov_chain using the initial_state,
        which is in ('0.0 kbps','0.6 kbps','1.2 kbps','2.4 kbps','4.8 kbps' or '9.6 kbps')
        :param markov_chain_name: Name of the markov chain/ transition matrix
        :param markov_chain: MarkovChain(initial_matrix)
        :param sequence_length: int
        :param initial_state: '0.0 kbps','0.6 kbps','1.2 kbps','2.4 kbps','4.8 kbps' or '9.6 kbps'
        :return: sequence as List that holds sequence_length number of steps following the markov_chain
                from initial_state
        """
        experiment = self.experiments[self.experiment_id].dict
        scenario = experiment[markov_chain_name]
        markov_chain = scenario[0]
        if initial_state is None:
            return markov_chain.simulate(ts_length=scenario[1])
        else:
            return markov_chain.simulate(ts_length=scenario[1], init=initial_state)

    def create_pendulum(self, sequence_length, initial_data_rate, experiment=None):
        """
           Create pendulum pattern
           :param sequence_length: length of the sequence following the pendulum
           :param pattern: pattern for the pendulum
           :param initial_data_rate: State/datarate for the start of the pattern
           :return: sequence of states following the pendulum pattern
           """
        sequence_of_states = []
        if experiment is None:
            experiment = self.experiments[self.experiment_id]
        count = experiment._pendulum_pattern.index(initial_data_rate)
        for i in range(1, sequence_length - 1):
            if count == len(experiment._pendulum_pattern):
                count = 0
            sequence_of_states.append(experiment._pendulum_pattern[count])
            count = count + 1
            # restart the pattern for the pendulum
        return sequence_of_states

    def change_communication_scenario(self,next_pattern_name, next_pattern,
                                      sequence_length, experiment=None,communication_scenario=None, initial_data_rate=None):
        """
           Change an existing communication scenario defined by sequence_of states
           :param initial_data_rate: initial data rate for the new scenario
           :param sequence_length: number of states that the comm. scenario should
           :param communication_scenario: The communication scenario
           :param next_pattern_name: Name of the next transition pattern (MC or pendulum)
           :param sequence_length: sequence of the corresponding communication scenario
           :param next_pattern: transition matrix that defines the probabilities for
                  changing the communication scenario
           :return: new communication scenario as list of ever-changing data rates
            defined by sequence_of_states following the new transition matrix next_transition_matrix
           """
        if experiment is None:
            experiment = self.experiments[self.experiment_id]
        if communication_scenario is None:
            communication_scenario = []
            if initial_data_rate is None:
                initial_data_rate = random.choice(self._state_values)
        else:
            if initial_data_rate is None:
                initial_data_rate = communication_scenario[-1]
        if 'pendulum' in next_pattern_name:
            return communication_scenario + self.create_pendulum(sequence_length, initial_data_rate)
        else:
            return communication_scenario + \
                   self.create_sequence(markov_chain_name=next_pattern_name, markov_chain=next_pattern,
                                        sequence_length=sequence_length, initial_state=initial_data_rate).tolist()

    def init_communication_scenario(self, experiment=None, experiment_id=None):
        """
        :param experiment: Experiment that is the basis for creating a new communication scenario.
        Only use this method if you want to create an initial scenario based on an experiment.
        To change a scenario we refer to the change_communication_scenario method.
        :return: Communication scenario as list of ever-changing data rates defined by experiment.
        """
        # If parameter is None set to default from instance
        if experiment_id is None:
            experiment_id = self.experiment_id
        if experiment is None:
            experiment = self.experiments[experiment_id].dict

        # Set initial data rate and init communication scenario as new empty scenario
        initial_data_rate = experiment['initial_data_rate']
        communication_scenario = []

        # Create scenario from set of pattern defined by the patterns of the experiment
        for pattern in experiment:
            if pattern != 'initial_data_rate':
                if len(communication_scenario) == 0:
                    init = initial_data_rate
                else:
                    init = communication_scenario[-1]
                print('Changed transition to: ' + pattern)

                communication_scenario = self \
                    .change_communication_scenario(
                    next_pattern_name=pattern,
                    communication_scenario=communication_scenario,
                    next_pattern=experiment[pattern][0],
                    sequence_length=experiment[pattern][1], initial_data_rate=init)
                print('Length of the communication scenario: ' + str(len(communication_scenario)))
                print(
                    '----------------------------------------------------------------------------------------------------'
                    '------------------------')
        self.sequence = communication_scenario
        return self.sequence

    def update_communication_scenario(self, experiment, experiment_id=None,communication_scenario=None):
        """
        Update/Extend an existing communication_scenario from an experiment.
        :param communication_scenario: Existing communication scenario represented as list of ever-changing data rates
        :param experiment: New experiment object from Experiment.py class
        :return: Updated/Extended communication scenario after running experiment
        """

        self.update_parameters(experiment,experiment_id)
        print(self.experiment_id)
        print(experiment.dict)

        if communication_scenario is None:
            communication_scenario = self.sequence

        for pattern in experiment.dict:
            if pattern != 'initial_data_rate':
                print('Changed transition matrix to: ' + pattern)

                if len(communication_scenario) == 0:
                    init = experiment['initial_data_rate']
                else:
                    init = communication_scenario[-1]

                communication_scenario = self \
                    .change_communication_scenario(
                    next_pattern_name=pattern,
                    communication_scenario=communication_scenario,
                    next_pattern=experiment.dict[pattern][0],
                    sequence_length=experiment.dict[pattern][1], initial_data_rate=init)
                print('Length of the communication scenario: ' + str(len(communication_scenario)))
                print(
                    '---------------------------------------------------------------------------------------------------- '
                    '------------------------')
        self.sequence = communication_scenario
        return communication_scenario

    def run_set_of_experiment(self):
        """
        Run a set of experiments defined by CommunicationScenario.experiments.
        :return: sequence of ever-changing data rates
        """
        for experiment in self.experiments:
            self.update_communication_scenario(self.sequence,experiment)
            self.experiment_id = self.experiments.index(experiment)
        return self.sequence

    def __get_color_map(self,states):
        """
        Get the colors from given color map for the states.
        :param states: sequence of states from 0,...,5 representing the 6 possible data rates
        :return: color_map for the states of the respective sub-scenario
        """
        states = self.__map_kbps_to_numbers(states)
        color_map = []
        cm = plt.get_cmap('RdYlGn')
        norm = Normalize(vmin=0, vmax=5)

        for state in states:
            color_map.append(cm(norm(state)))
        return color_map

    def __create_subgraph(self,states, start):
        """
        Create networkx subgraph for the states defined by states and from the starting point start.
        :param states: sequence of states from 0,...,5 representing the 6 possible data rates
        :param start: start state for the current subgraph
        :return:
        """
        subrapgh = nx.Graph()
        nodes = range(start, start + len(states))
        color_map = self.__get_color_map(states[0:len(states)])
        state_labels = self.__map_kbps_to_numbers(states)
        subrapgh.add_nodes_from(nodes)

        # Initialize parameters for networkx subgraph
        pos = {}
        labels = {}
        edge_labels = {}
        edges = []
        counter = 0

        for node in nodes:
            pos[nodes[counter]] = (counter, 0)
            labels[nodes[counter]] = state_labels[counter]
            if counter < len(nodes) - 1:
                edges.append((nodes[counter], nodes[counter] + 1))
                if state_labels[counter + 1] == state_labels[counter]:
                    edge_labels[(nodes[counter], nodes[counter] + 1)] = '='
                elif state_labels[counter + 1] > state_labels[counter]:
                    edge_labels[(nodes[counter], nodes[counter] + 1)] = '+'
                else:
                    edge_labels[(nodes[counter], nodes[counter] + 1)] = '-'
            counter = counter + 1

        # G.add_edges_from(edges)

        return subrapgh, pos, labels, edge_labels, edges

    def create_plot(self,file_name,states,figsize=(10,5)):
        """
        Create plot for a set of states
        :param figsize: size of the plt.figure
        :param states: sequence of states from 0,...,5 representing the 6 possible data rates
        :param file_name: Destination path for the plot .png file
        """

        # Set number of subplots
        number_subplots = int(len(states) / self.nxn_dim_plot)
        print()
        fig = plt.figure(figsize=figsize)

        for i in range(1, number_subplots+1):
            fig.add_subplot(int(number_subplots / 2), 2, i)
            subgraph, pos, labels, edge_labels, edges = self.__create_subgraph(states=states[(i - 1) * self.nxn_dim_plot:i * self.nxn_dim_plot],
                                                                        start=(i - 1) * self.nxn_dim_plot)
            color_map = self.__get_color_map(states=states[(i - 1) * self.nxn_dim_plot:i * self.nxn_dim_plot])
            nx.draw(subgraph, pos, node_color=color_map, with_labels=False, k=0.5)
            nx.draw_networkx_labels(subgraph, pos, labels)
            nx.draw_networkx_edges(subgraph, pos, edges, alpha=0.00001)
            nx.draw_networkx_edge_labels(subgraph, pos, edge_labels)

        fig.tight_layout()
        fig.savefig('img/'+file_name+'.png')
        plt.axis('off')
        plt.show()

    def plot_communication_scenario(self,file_name,number_of_states=100):
        """
        Plot a communication scenario
        :param file_name: Prefix for the plot file names
        :param number_of_states: number of states per plot
        """
        # Map sequence of ever-changing data rates to state numbers
        states = self.sequence
        print(states)
        number_plots = int(len(states) /number_of_states)
        print(number_plots)
        for plot_id in range(0,number_plots):
            self.create_plot(file_name+str(plot_id),states[(plot_id)*number_of_states:(plot_id+1)*number_of_states])
            print('Hello')





