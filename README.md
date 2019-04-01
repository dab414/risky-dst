# Dissertation Experiments
This repository contains the source code for my dissertation experiments to be run on MTurk.  

*These experiments are still under development (3/31/2019)*  

## Pilot Data  

* [Pilot Data Summary](http://davebraun.org/dissertation/experiments/pilots/scripts/dissertationPilot_1-23.html)

## Experiment 1

The experiment is hosted at https://davebraun.org/dissertation/experiments/exp1  

Experiment 1 is broken down into five phases:  

* [Practice Cued Task Switching](exp1/pracCued/index.html)  
* [Practice Deck Selections](exp1/pracDecks/index.html)  
* [Point Calibration](exp1/calibration/index.html)  
* [Two-option choice](exp1/twoChoice/index.html)  
* [Three-option choice](exp1/threeChoice/index.html)  

The supplementary JavaScript functions for the experiment are separated into two files based on whether they will generalize across all three experiments:  

* [JavaScript specific to Exp 1](exp1/js/exp1Functions.js)  
* [JavaScript for all three exps](globalJs/globalFunctions.js)  

Data processing scripts:  

* Convert subject JSON files to aggregate CSV files: [`dataProcessing.py`](exp1/dataProcessing/dataProcessing.py)