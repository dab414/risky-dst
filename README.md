# Dissertation Experiments
This repository contains the source code for my dissertation experiments to be run on MTurk.  


## Pilot Data  

* [Pilot Data Summary](http://davebraun.org/dissertation/experiments/production/pilots/scripts/dissertationPilot_1-23.html)

## Experiment 1

The experiment is hosted at: https://davebraun.org/dissertation/experiments/production/exp1  

Experiment 1 is broken down into two phases, the code for which can be found below:  

* [Practice Cued Task Switching](exp1/pracCued/index.html)  
* [Demand Selection Task](exp1/dst/index.html)  

The supplementary JavaScript functions for the experiment are separated into two files based on whether they will generalize across all three experiments:  

* [JavaScript specific to Exp 1](exp1/js/exp1Functions.js)  
* [JavaScript for all three exps](globalJs/globalFunctions.js)  

Data processing scripts:  

* Convert subject JSON files to aggregate CSV files: [`dataProcessing.py`](exp1/dataProcessing/dataProcessing.py)

## Experiment 2

The experiment is hosted at: https://davebraun.org/dissertation/experiments/production/exp2

Experiment 2 is broken down into three general phases, the code for which can be found below:  

* [Practice Cued Task Switching](exp2/pracCued/index.html)  
* [Demand Selection Task](exp2/dst/index.html)  
* [Rapid Fire Demand Selection Task](exp2/rapidFire/index.html)

The JavaScript specific to this experiment is [here](exp2/js/exp2Functions.js)

## Experiment 3

The experiment is hosted at: https://davebraun.org/dissertation/experiments/production/exp3

Experiment 3 is broken down into three general phases, the code for which can be found below:  

* [Practice Cued Task Switching](exp3/pracCued/index.html)  
* [Demand Selection Task](exp3/dst/index.html)  
* [Rapid Fire Demand Selection Task](exp3/rapidFire/index.html)

The JavaScript specific to this experiment is [here](exp3/js/exp3Functions.js)