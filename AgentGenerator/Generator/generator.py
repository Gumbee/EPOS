import numpy as np
import pandas as pd

import random

# to run this script, get the data from InsideAirbnb and put it in the Data folder (file is called listing.csv)
#
# Link:
# http://insideairbnb.com/get-the-data.html

numAgents = 100

np.random.seed(120)
randomPermutation = np.random.permutation(numAgents)

# get the data frame
df = pd.read_csv('Data/listings.csv')

# get latitude and logitude values
latitudes = df['latitude'].values[randomPermutation[:numAgents]]
longitudes = df['longitude'].values[randomPermutation[:numAgents]]

# get the prices
prices = df['price'].values[randomPermutation[:numAgents]]

# get the max occupancies
accomodates = df['accommodates'].values[randomPermutation[:numAgents]]

# generate the preferred types
optimalTypesArray = []
optimalTypesIndices = []

for i in range(len(latitudes)):
    percentages = []

    totalPercentage = 1.0

    for j in range(4):
        # generate a random preference of this type (j)
        randomPercentage = np.random.uniform(0, totalPercentage)
        # add this preference
        percentages.append(randomPercentage)
        # subtract the random preference from the total so we never exceed 1
        totalPercentage -= randomPercentage

    # the last type gets the remaining percentage as preference
    percentages.append(totalPercentage)
    np.random.shuffle(percentages)

    maxPercentage = -1
    maxIndex = -1

    for j in range(5):
        if percentages[j] > maxPercentage:
            maxPercentage = percentages[j]
            maxIndex = j

    optimalTypesArray.append(percentages)
    optimalTypesIndices.append(maxIndex)

optimalTypes = np.array(optimalTypesArray)[randomPermutation[:numAgents]]
optimalTypesIndices = np.array(optimalTypesIndices)[randomPermutation[:numAgents]]

np.set_printoptions(suppress=True)

print(accomodates.shape)
print(optimalTypes.shape)

fileData = ""

for i in range(numAgents):
    line = str(latitudes[i]) + "," + str(longitudes[i]) + "," + str(prices[i][1:]) + "," + str(accomodates[i]) + "," + str(optimalTypesIndices[i]) + "," + np.array2string(optimalTypes[i], separator=',') + "\n"
    fileData += line.replace(" ", "")

with open('Data/agentData.info', 'w+') as file:
    file.write(fileData)
