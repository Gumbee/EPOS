#!/usr/bin/env python
import numpy as np
from os import path as os_path
from os import makedirs as os_makedirs


def run(numAgents, numApplicants):
    options_applicants = 3
    options_price = 3
    sigma = 20

    if not os_path.exists('../datasets/airbnb/'):
        os_makedirs('../datasets/airbnb/')

    with open("../datasets/airbnb/agentData.info", "r") as data:
        for i in range(numAgents):
            data_line = data.readline()
            data_list = data_line.split(",")
            applicant_ids = np.random.randint(0, high=numApplicants, size=options_applicants)
            prices = []

            for e in range(options_price):
                price_delta = np.random.normal(float(data_list[2]), sigma, 1)
                prices.append(price_delta)

            with open("../datasets/airbnb/agent_" + str(i) + ".plans", "w+") as file:
                for j in applicant_ids:
                    applicant = np.zeros(numApplicants)
                    applicant[j] = 1.0
                    occupancy = np.zeros(numAgents)
                    occupancy[i] = np.random.randint(1, high=10)
                    for p in prices:
                        plan = str(0.0) + ":"
                        plan += ','.join(map(str, applicant)).replace('\n', '') + ","
                        price = np.zeros(numAgents)
                        price[i] = max(p/2, p)
                        plan += ','.join(map(str, price)).replace('\n', '') + ","
                        plan += ','.join(map(str, occupancy)).replace('\n', '') + "\n"
                        file.write(plan.replace(" ", ""))
