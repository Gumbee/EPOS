#!/usr/bin/env python
import numpy as np
from os import path as os_path
from os import makedirs as os_makedirs
from GeneratorScripts.agent_generator import get_data


def run(numAgents, numApplicants, options_applicants, options_price):
    sigma = 20

    randomPermutation, _, _, _, accomodates, _, _ = get_data()

    if not os_path.exists('../datasets/airbnb/'):
        os_makedirs('../datasets/airbnb/')

    with open("../datasets/airbnb/agentData.info", "r") as data:
        print("Creating the plans for the agents...")
        applicantOccupancies = []

        for i in range(numApplicants):
            applicantOccupancies.append(np.random.randint(1, high=11))

        for i in range(numAgents):
            data_line = data.readline()
            data_list = data_line.split(",")

            applicant_ids = []

            for k in range(options_applicants):
                random_applicant = np.random.randint(0, high=numApplicants, size=1)

                while False or applicantOccupancies[random_applicant[0]] > int(accomodates[randomPermutation[i]]):
                    random_applicant = np.random.randint(0, high=numApplicants, size=1)

                applicant_ids.append(random_applicant)

            prices = []

            for e in range(options_price):
                price_delta = np.random.normal(float(data_list[2]), sigma, 1)
                price_delta = max(price_delta, float(data_list[2])/2)
                price_delta = min(price_delta, float(data_list[2])*3.0/2)
                prices.append(price_delta)

            with open("../datasets/airbnb/agent_" + str(i) + ".plans", "w+") as file:
                for p in prices:
                    for j in applicant_ids:
                        applicant = np.zeros(numApplicants)
                        applicant[j] = 1.0
                        occupancy = np.zeros(numAgents)
                        occupancy[i] = applicantOccupancies[j[0]]
                        plan = str(0.0) + ":"
                        plan += ','.join(map(str, applicant)).replace('\n', '') + ","
                        price = np.zeros(numAgents)
                        price[i] = p
                        plan += ','.join(map(str, price)).replace('\n', '') + ","
                        plan += ','.join(map(str, occupancy)).replace('\n', '') + "\n"
                        file.write(plan.replace(" ", ""))

                print("Plans for Agent " + str(i) + " sucessfully generated.")
