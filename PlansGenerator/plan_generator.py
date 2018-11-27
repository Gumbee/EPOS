#!/usr/bin/env python
import numpy as np
from random import randint

no_agents = 400
no_applicants = 400

file = open("Plans/agentData.info","r")


for i in range(no_agents):
	data_line = file.readline()
	data_list = data_line.split(",")
	for j in range(no_applicants):
		applicant = np.zeros(no_applicants)
		applicant[j] = 1.0
		occupancy = np.zeros(no_agents)
		occupancy[i] = randint(1,10)
		price = np.zeros(no_agents)
		price[i] = float(data_list[2]) - 20
		plan1 = str(0.0) + ":" + np.array2string(applicant, separator=',')[1:-1] + "," + np.array2string(price, separator=',')[1:-1] + "," + np.array2string(occupancy, separator=',')[1:-1]+"\n"
		price[i] = data_list[2]
		plan2 = str(0.0) + ":" + np.array2string(applicant, separator=',')[1:-1] + "," + np.array2string(price, separator=',')[1:-1] + "," + np.array2string(occupancy, separator=',')[1:-1]+"\n"
		price[i] = float(data_list[2]) + 20
		plan3 = str(0.0) + ":" + np.array2string(applicant, separator=',')[1:-1] + "," + np.array2string(price, separator=',')[1:-1] + "," + np.array2string(occupancy, separator=',')[1:-1]+"\n"

	#price = str(float(data_list[2])-20) + "," + str(float(data_list[2])-10) + "," + data_list[2] + "," + str(float(data_list[2])+10) + "," + str(float(data_list[2])+20)
		if j == 0:
			plansfile = open("Plans/agent_" + str(i) + ".plan","+w")
		else:
			plansfile = open("Plans/agent_" + str(i) + ".plan","a")
	#plansfile.write(price)
		plansfile.write(plan1+plan2+plan3)


	#print (i)
	#print (data_line)