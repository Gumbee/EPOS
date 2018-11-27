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
        applicant = np.ones(no_applicants)*7
        applicant[j] = 1.0
        occupancy = np.ones(no_agents)*3
        occupancy[i] = np.random.randint(1, high=10)
        for p in prices:
            plan = str(0.0) + ":"
            plan += ','.join(map(str, applicant)).replace('\n', '') + ","
            price = np.ones(no_agents)*5
            price[i] = p
            plan += ','.join(map(str, price)).replace('\n', '') + ","
            plan += ','.join(map(str, occupancy)).replace('\n', '') + "\n"
            plansfile.write(plan.replace(" ", ""))
            print("-----")
            print(applicant.shape)
            print(price.shape)
            print(occupancy.shape)
    plansfile.close()
