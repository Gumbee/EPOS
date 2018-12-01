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


### TODO - Plots
1. Global cost / Local cost plot (x-axis:iterations)
2. Global response vs target signal plot
3. Global cost vs lambda value (x-axis: lambda)
3. Local cost vs lambda value (x-axis: lambda)
4. Global cost reduction (x-axis: season)
5. Global cost reduction (x-axis: #plans)
6. Local cost of selected plans (x-axis: agents, bar graph)
7. Number of conflicts (in matching) (x-axis: season)
8. Profit/Loss (x-axis: agent)
9. Plan selection index (x-axis: lambda)
10. Brute force vs EPOS