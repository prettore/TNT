import configparser

config = configparser.ConfigParser()

'''
For new experiments you can create a new config by using 

    config['NAME_OF_NEW_CONFIGURATION'] = {
        "parameter 1": value 1,
        .
        .
        .
        "parameter n": value n,
    }
and save the config to the config.ini configuration file by setting CONFIG_NAME to the configuration name. 
'''

config['default_config'] = {
        "config_name" : "default_config",
        "transition_matrix_names" : "B1,B1_2,B2,B3,B4,B5_round1,B5_round2,B6",
        "transition_matrix_file_path": "transition_matrices.csv",
        "pendulum_pattern": "9.6 kbps,4.8 kbps,2.4 kbps,1.2 kbps,0.6 kbps,0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps",
        "scenario" : "B1,pendulum,B3,B4,pendulum,B6,B5_round1,B5_round2,B1_2",
        "state_values": "0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps,9.6 kbps",
        "initial_datarate" : "0.6 kbps",
        "number_steps": "100,100,100,100,100,100,100,100",
        "multiple": "10"

    }

'''
Example configuration to update a previous experiment and continue with a new set of transition matrices defined as new
experiment. 
'''

config['simple_experiment'] = {
        "config_name": "simple_experiment",
        "transition_matrix_names": "B1,B1_2,B2,B3,B4,B5_round1,B5_round2,B6",
        "transition_matrix_file_path": "transition_matrices.csv",
        "pendulum_pattern": "9.6 kbps,4.8 kbps,2.4 kbps,1.2 kbps,0.6 kbps,0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps",
        "scenario": "B1,B1_2,B2,B3,B4,B5_round1,B5_round2,B6",
        "state_values": "0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps,9.6 kbps",
        "initial_datarate": "0.6 kbps",
        "number_steps": "100,100,100,100,100,100,100,100",
        "multiple": "10"
}

'''
Create the Escher Pattern as an optimum policy resulting from a MDP.
'''

config['escher_mdp_config'] = {
        "config_name" : "default_config",
        "transition_matrix_names" : "B1,B2,B3,B4,B5,B6",
        "transition_matrix_file_path": "inputs/metamorphosis_patterns.csv",
        "pendulum_pattern": "9.6 kbps,4.8 kbps,2.4 kbps,1.2 kbps,0.6 kbps,0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps",
        "scenario" : "B1,B2,B3,B4,B5,B6",
        "state_values": "0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps,9.6 kbps",
        "initial_datarate" : "0.0 kbps",
        "number_steps": "100,100,100,100,100,100,100,100",
        "multiple": "10"

    }

'''
Create simple mobility config.
'''
config['markov_pattern_config'] = {
        "config_name" : "markov_pattern_config",
        "transition_matrix_names" : "Limited",
        "transition_matrix_file_path": "ever_changing_sparse/communication_scenario/inputs/simple_mobility_pattern.csv",
        "pendulum_pattern": "9.6 kbps,4.8 kbps,2.4 kbps,1.2 kbps,0.6 kbps,0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps",
        "scenario" : "Limited",
        "state_values": "0.0 kbps,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps,9.6 kbps",
        "initial_datarate" : "1.2 kbps",
        "number_steps": "30",
        "multiple": "10"
    }

if __name__ == "__main__":

    CONFIG_FILE_NAME = 'config'
    CONFIG_NAME = 'markov_pattern_config'

    with open('configs/'+CONFIG_FILE_NAME+'.ini', 'w') as configfile:
        config.write(configfile)

    for key in config[CONFIG_NAME]:
        print(config[CONFIG_NAME][key])


