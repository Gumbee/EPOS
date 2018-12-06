#!/usr/bin/env python
import statistics
import math

#numAgents = 10

def get_num_agents():
    with open('./conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "numAgents=" in line:
                return int(line.replace("numAgents=", ""))

def get_num_applicants():
    with open('./conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "numApplicants=" in line:
                return int(line.replace("numApplicants=", ""))

def get_options_applicants():
    with open('./conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "applicantOptions=" in line:
                return int(line.replace("applicantOptions=", ""))


def get_options_price():
    with open('./conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "priceOptions=" in line:
                return int(line.replace("priceOptions=", ""))


def computeRMSE(goal,response):

    goal_avg = sum(goal)/len(goal)
    goal_std = statistics.stdev(goal)
    response_avg = sum(response)/len(response)
    response_std = statistics.stdev(response)

    magic_factor = response_std/(goal_std+1e-10)
    goal = [x-y for x,y in zip(goal,[goal_avg]*len(goal))]#(goal - ([goal_avg]*len(goal)))
    goal = [magic_factor*x for x in goal]
    goal = [sum(pair) for pair in zip(goal,[response_avg]*len(goal))]#goal + ([response_avg]*len(goal))

    errors = [x-y for x,y in zip(response,goal)]
    errors_square = [e**2 for e in errors]
    RMSE = math.sqrt(sum(errors_square)/len(errors_square))

    return RMSE

def get_plans(agent_id):
    # code which reads all possible plans of agent_id and saves all plans in a list and returns that list
    # the plan is just a list of values
    plan = []
    # the list of plans is a list of lists(plans)
    list_of_plans = []
    with open("./datasets/airbnb/agent_" + str(agent_id) + ".plans", "r") as data:
        print("Reading plans for " + str(agent_id) +" agent...")
        numPlans = Applicants_options*Price_options
        for plan_id in range(numPlans):
            plan = data.readline().replace('\n','')[4:]    # Eliminates score and line break characters
            plan = list(map(float,plan.split(",")))         # converts huge string into list of strings into list of floats (plan as a list of values) 
            #plan = str(plan).replace('\\n', '')
            list_of_plans.append(plan)
    
    return list_of_plans


def evaluate_cost_of_plan_combination(selected_plans,goal):
    # evaluate the global cost if the agents have selected the provided plans
    acc_response = [0.0]*(numApplicants+numAgents+numAgents)
    for agent_id in range(numAgents):
        chosen_plan_idx = selected_plans[agent_id]
        plan_list_current_agent = agent_plans[agent_id]
        chosen_plan=plan_list_current_agent[chosen_plan_idx]
        acc_response = [sum(pair) for pair in zip(acc_response,chosen_plan)]
    #Computes RMSE from acc_response and target signal
    matching_response = acc_response[:numApplicants]
    price_response = acc_response[numApplicants:numApplicants*2]
    occupancy_response = acc_response[numApplicants*2:]

    # with open("./datasets/airbnb/goal.target", "r") as targetfile:
    #     print("Reading target file: " + str(targetfile.name))
    #     goal = targetfile.readline().replace('\n','')
    #     goal = list(map(float,goal.split(",")))             # list containing goal signal

    matching_goal = goal[:numApplicants]
    price_goal = goal[numApplicants:numApplicants*2]
    occupancy_goal = goal[numApplicants*2:]

    print('Evaluating...')

    globalcost = 20*computeRMSE(matching_goal,matching_response) + computeRMSE(price_goal,price_response) + 4*computeRMSE(occupancy_goal,occupancy_response)
    

    return globalcost

#---------------------------------CONFIGURATION FOR PARAMETERS------------------
numApplicants=get_num_applicants()       
numAgents=get_num_agents()
Applicants_options = get_options_applicants()
Price_options = get_options_price()
#--------------------------------------------------------------------------------

print('Executing Brute Force approach with: ' + str(numApplicants) + ' Applicants, ' + str(numAgents) + ' Agents, ' + str(Applicants_options) + ' Applicant options, ' + str(Price_options) + ' Price options...')

# contains the list of plans of every agent
agent_plans = []
# a list of indices which tell us which plan every agent currently has selected
current_selected_plan = []
# a list of indices which tell us which combination of plans is currently the best
current_best_combination = []

# save all plans
for agent_id in range(numAgents):
    agent_plans.append(get_plans(agent_id))
    # every agent starts with the first plan selected
    current_selected_plan.append(0)
    # the current best combination of plans is if every agent selects the first one (since we haven't explored more combinations yet)
    current_best_combination.append(0)

has_reached_end = False
# start with a ridiculous cost
current_cost = 1000000000000

costs_list = []

# READ TARGET SIGNAL (ONCE) FOR RMSE COMPUTATION
with open("./datasets/airbnb/goal.target", "r") as targetfile:
        print("Reading target file: " + str(targetfile.name))
        goal = targetfile.readline().replace('\n','')
        goal = list(map(float,goal.split(",")))             # list containing goal signal

cost = evaluate_cost_of_plan_combination(current_selected_plan,goal)         # EVALUATES THE FIRST PLAN FOR ALL AGENTS WHICH IS NOT CONSIDERED IN THE LOOP BELOW
costs_list.append(cost)
if current_cost > cost:
    current_cost = cost
    current_best_combination = current_selected_plan.copy()

loop_count = 1  # Plan 0 (first plan combination is actually evaluated outside the while loop)

while not has_reached_end:

    print('Testing plan combination: ' + str(loop_count))

    for agent_id in range(numAgents-1, -1, -1):
        # if we have selected the last plan, we need to go back to the first plan and the next agent has to go one plan up
        if current_selected_plan[agent_id] == len(agent_plans[agent_id])-1:
            # if we have to reset the first agent, we have reached the end
            if agent_id == 0:
                has_reached_end = True
            current_selected_plan[agent_id] = 0
        else:
            current_selected_plan[agent_id] = current_selected_plan[agent_id]+1
            break

    # evaluate the global cost if the agents have selected the plans which are referenced in the current_selected_plan list
    cost = evaluate_cost_of_plan_combination(current_selected_plan,goal)
    costs_list.append(cost)
    #print(costs_list)

    if current_cost > cost:
        current_cost = cost
        current_best_combination = current_selected_plan.copy()

    loop_count +=1

with open("./datasets/airbnb/brute_force.costs", "w+") as destination:
    destination.write(str(costs_list))

print("The best combination of plans results in a cost of " + str(current_cost))