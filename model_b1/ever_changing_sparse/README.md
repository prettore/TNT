<<<<<<< HEAD
#Ever-changing commmunication scenarios for tactical networks
=======
# :arrows_counterclockwise: Ever-changing commmunication scenarios for tactical networks :arrows_counterclockwise:
>>>>>>> master
This is an initial approach to create ever-changing communication scenarios for tactical networks. 
In this case the term "ever-chaning" is related to the data rate of our VHF radios, which support 5 possible 
data rates. All the experiments created with this framework consist of communication scenarios defined by ever-changing 
data rates between 0.0 kbps (disconnected) ,0.6 kbps,1.2 kbps,2.4 kbps,4.8 kbps and 9.6 kbps. 

:space_invader: :space_invader: :space_invader: :space_invader:

<<<<<<< HEAD
## Requirements
=======
## :wrench: Requirements :wrench:
>>>>>>> master

`python 3.6 or higher`
`networkx`
`pandas`
`quanteco`
`POT` For installation we refer to: ["POT Source"](https://pythonot.github.io/index.html ("Python optimal transport"))

<<<<<<< HEAD
## Usage
=======
## :memo: Usage :memo:
>>>>>>> master

1. Change the `config.py` by adding a new configuration for your experiment. The parameters are as follows: 
    - `transition_matrix_names:` Comma seperated string holding the names for the transition matrix of the 
    respective markov chains.
    - `transition_matrix_file_path:`File path to the `.csv` matrix file 
    - `pendulum_pattern:` Definition of the pendulum pattern through all possible data rates, if needed in 
    the scenario.
    - `scenario:` Comma seperated string defining the order of the transition matrices in the communication 
    scenario
    - `state_values:` Comma seperated string of possible data rates of the radios. 
    - `initial_datarate:` Initial data rate for the experiment, that is used as initial state for the first 
    Markov chain. 
    - `number_steps:` The number of steps that the experiments follow the respective transition matrix in 
    `scenario`.
    - `multiple:` a string representation of an integer, which defines the rows and columns of the output plot.
                  Not recommended to be greater than 10. Otherwise also set the size of the plt figures, s.t.
                  they can handle `multiple`.
    Then run `config.py` as main function to update the `config.ini` file regarding to your experiment
    configuration.

2. Create a new experiment using the Experiment.py class. An example can be seen in main.py. 
    - Use `experiment = exp.Experiment('CONFIG_NAME')` to create a new experiment, where `CONFIG_NAME` is the name of the
    configuration that you want to use from `config/config.ini`.
    - `experiment.dict` gives you the dictionary representation of the experiment. You can print it with
    `print(experiment.dict)`
    - Use `experiment.plot_transition_matrices()` to plot the Markov chains represented by the `transition_matrices` 
    from the `CONFIG_NAME.ini`. 
    
    An example output can look like this: 
    
    ![Example Markov Chain](communication_scenario/img/example_markov_chain.png)
    
   - You can save your experiment to a pickle file using `Experiment.save_model(FILE_NAME)`, where `FILE_NAME`is the name 
   of the destination `.p` pickle file (without `.p`)
   
 3. Once you created an experiment you can use the experiment to create a new instance of
 a communication scenario and run the experiment:
    - Use `comm_scenario = CommunicationScenario.CommunicationScenario(EXPERIMENT)`,where `EXPERIMENT`is an
    instance of the `Experiment.py` class. 
    - Then you can use `comm_scenario.init_communication_scenario()` to run the experiment. The sequence of
    ever-changing data rates can be get directly from the return value of the method or from 
    `comm_scenario.sequence`.
    - To plot the scenario use `comm_scenario.plot_communication_scenario('test_scenario')`. 
    This creates a set of `.png` files in the `img/` directory. Each file holds a plot of 
    100 states in 2 rows each of dimension 10x10. 
    
    An example output can look like this: 
    
    Ever-changing datarates         |    Ever-changing datarates 
    :-------------------------:|:-------------------------:
    States 1-100             |  States 100-200 
    ![Test scenario plot 1](communication_scenario/img/test_scenario1.png)  |  ![Test scenario plot 2](communication_scenario/img/test_scenario2.png)
    States 200-300             |  States 300-400 
    ![Test scenario plot 3](communication_scenario/img/test_scenario3.png)  |  ![Test scenario plot 4](communication_scenario/img/test_scenario4.png)
    States 400-500             |  States 500-600 
    ![Test scenario plot 3](communication_scenario/img/test_scenario3.png)  |  ![Test scenario plot 4](communication_scenario/img/test_scenario4.png)
    
    - You can also update a communication scenario using `CommunicationScenario.update_communication_scenario(EXPERIMENT)`,
    where `EXPERIMENT` is an instance of the `Experiments.py` class. It should be noted that you can always access
    previous experiments by accessing the list of experiments `CommunicationScenario.experiments` of the `CommunicationScenario`
    instance. You can also set the `CommunicationScenario` parameters to the respective experiment by using 
    `CommunicationScenario.update_paramerters(EXPERIMENT)`. But this is always important if you are running back in time. 
    If you update forward in time parameters are set automatically to the actual `EXPERIMENT` instance.
    
 4. If you want to use the ever-changing communication scenario from the laboratory you can use the `RaspiConnector()` 
    class to create a new connection to the Raspberry Pi in the laboratory. Once you initiated the connection you can use 
    the `disrupt_radio()` method to handle disruptions from the scenario. 