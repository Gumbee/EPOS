# EPOS - Economic Planning and Optimized Selections

### Getting started
To run this project do the following:
1. Make sure you have `pandas` and `numpy` installed (if not, run `pip3 install numpy pandas`)
2. Run the bash script `run_airbnb_optimization.sh` by running `sh ./run_airbnb_optimization.sh`

### TODO
1. explain changes to model from first assignment
   1. changes in the plan
   2. changes in global cost function
   3. how we generate goal signals
2. generate datasets for different scenarios
3. describe each dataset in a short REAME file (see EPOS examples)
4. illustrate datasets for each scenario:
   1. plot price distribution
   2. plot occupancy distribution
   3. plot local cost of plans for each agent
5. system-level evaluation:
   1. determine global cost baseline using plans with the agent's optimal values and with current state goal signals
   2. plot global cost reduction for each scenario by repeating the optimization for different positioning of the agents
   3. plot local cost of selected plans for each scenario
6. optimality analysis:
   1. implement a brute-force approach for small number of agents and plans
   2. compare brute-force and I-EPOS solutions for each scenario (see p.27 of [1])
7. socio-technical evaluation:
   1. define a grid of &lambda; values
   2. run optimization for each of them
   3. plot global and local costs, selected plans, etc...

