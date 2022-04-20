try:
    import communication_scenario.Experiment as exp
    import communication_scenario.CommunicationScenario as com
    import pickle as pickle
except:
    raise

def main():
    # Define an experiment and save it to pickle file
    experiment = exp.Experiment('default_config')
    print(experiment.dict)
    experiment.save_experiment('experiments/test_experiment')

    # Plot the transition matrices for an experiment
    print(experiment.plot_transition_matrices())

    # Create a new communication scenario from an experiment
    comm_scenario = com.CommunicationScenario(experiment)

    # Run the experiment and init the sequence of ever-changing data rates from the experiment
    ever_changing_data_rates = comm_scenario.init_communication_scenario()
    print(ever_changing_data_rates)
    print(len(ever_changing_data_rates))

    # Plot the communication scenario in 100 states per plot in 2 rows each of dim=10
    comm_scenario.plot_communication_scenario('test_scenario')

    # Update communication scenario using a new experiment
    experiment3 = exp.Experiment('simple_experiment')
    print(experiment3.dict)
    comm_scenario.update_communication_scenario(experiment3)
    print(len(comm_scenario.sequence))

if __name__ == "__main__":
    main()


