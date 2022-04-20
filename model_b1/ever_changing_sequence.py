##################################################
## creating states sequence using Markov chain
##################################################
## Author: Johannes and Paulo H. L. Rettore
## Status: close
## Date: 20/09/2020
##################################################

try:
    import sys
    sys.path.append('../ever_changing_sparse/')

    # import communication_scenario.Experiment as exp
    # import communication_scenario.CommunicationScenario as com
    # import communication_scenario.utils as ut
    import model_b1.ever_changing_sparse.communication_scenario.Experiment as exp
    import model_b1.ever_changing_sparse.communication_scenario.CommunicationScenario as com
    import model_b1.ever_changing_sparse.communication_scenario.utils as ut

except:
    raise


def create_sequence(config_name):
    # Define an experiment and save it to pickle file
    experiment = exp.Experiment(config_name)

    # Create a new communication scenario from an experiment
    comm_scenario = com.CommunicationScenario(experiment)

    # Run the experiment and init the sequence of ever-changing data rates from the experiment
    ever_changing_data_rates = comm_scenario.init_communication_scenario()

    return experiment, comm_scenario, ut.get_int_sequence(ever_changing_data_rates)


if __name__ == "__main__":
    # Create ever-changing sequence of data rates
    experiment, comm_scenario, ever_changing_data_rates = create_sequence('markov_pattern_config')

    # Print the setup for the experiment
    print(experiment.dict)

    # Plot the transition matrices for an experiment
    print(experiment.plot_transition_matrices())

    # Run the experiment and init the sequence of ever-changing data rates from the experiment
    print(comm_scenario.sequence)
    print(len(ever_changing_data_rates))
    comm_scenario.plot_communication_scenario('simple_mobility_scenario',number_of_states=20)


