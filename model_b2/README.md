
# Transforming mobility pattern into sequences of data rates: 

Model MB2 (Γ, C, nref ) transforms mobility patterns into network states and is used to change the
radio modulation or cause link disconnections during the experiment. It should be noted that TNT is designed to work with
any tool that implements mobility models and exports a trace
file, such as MobiSim and BonnMotion. For simplicity, this investigation focuses on the usage of BonnMotion due
to its flexibility and the wide variety of different models like
Random Waypoint (RWP), Random Walk (RW), Probabilistic
Random Walk (PRW), Gauss-Markov (GM), Manhattan Grid
(MG), and Disaster Area (DA) that it supports. Thus, TNT
defines the mobility scenario and the corresponding parameters
using BonnMotion, parses the resulting trace file Γ and uses the
mobility trace to define the communication area C with respect
to reference node nref , as discussed before. Then TNT uses the
resulting set of communication areas A0, . . . , A|S|−1 to match
each position to with a data rate representing the tactical radio
modulation. In this sense, Model B2 reuses the methods defined by
Model B1 , namely Modeling the communication area, Matching
data rates, and Trace features extraction. For more details, 
please read the referred article.


## Getting Started

Execute the script [trace_to_datarate](trace_to_datarate.py) to create mobility traces from stochastic models. 

```shell
python trace_to_datarate.py
```

_**Note:** Additional important information for the usage of this project can be found in the comments of the python scripts.
We strongly recommend looking into the code of those files before using them._
