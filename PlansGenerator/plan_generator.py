#!/usr/bin/env python
import numpy as np
import itertools

no_agents = 400
no_applicants = 400

file = open("../AgentGenerator/Generator/Data/agentData.info", "r")

options_applicants = 3
options_price = 3
price_delta = 20

for i in range(no_agents):
    data_line = file.readline()
    data_list = data_line.split(",")
    applicant_ids = np.random.randint(0, high=no_applicants, size=options_applicants)
    prices = np.array([float(data_list[2]) - price_delta, float(data_list[2]), float(data_list[2]) + price_delta])
    plansfile = open("../datasets/airbnb/agent_" + str(i) + ".plans", "w")
    for j in applicant_ids:
        applicant = np.zeros(no_applicants)
        applicant[j] = 1.0
        occupancy = np.zeros(no_agents)
        occupancy[i] = np.random.randint(1, high=10)
        for p in prices:
            plan = str(0.0) + ":"
            plan += np.array2string(applicant, separator=',')[1:-1].replace('\n', '')
            price = np.zeros(no_agents)
            price[i] = p
            plan += "," + np.array2string(price, separator=',')[1:-1].replace('\n', '')
            plan += np.array2string(occupancy, separator=',')[1:-1].replace('\n', '') + "\n"
            plansfile.write(plan.replace(" ", ""))
            print("-----")
            print(applicant.shape)
            print(price.shape)
            print(occupancy.shape)
    plansfile.close()
