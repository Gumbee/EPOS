import numpy as np
import pandas as pd
from os import path as os_path
from os import makedirs as os_makedirs

# to run this script, get the data from InsideAirbnb and put it in the Data folder (file is called listing.csv)
#
# Link:
# http://insideairbnb.com/get-the-data.html

def get_data():
    # get the data frame
    df = pd.read_csv('Data/listings.csv')

    seedValue = 22

    np.random.seed(seedValue)

    randomPermutation = np.random.permutation(len(df['latitude'].values))

    # get latitude and logitude values
    latitudes = df['latitude'].values
    longitudes = df['longitude'].values

    # get the prices
    prices = df['price'].values

    # get the max occupancies
    accomodates = df['accommodates'].values

    # generate the preferred types
    optimalTypesArray = []
    optimalTypesIndices = []

    for i in range(len(randomPermutation)):
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

    optimalTypes = np.array(optimalTypesArray)
    optimalTypesIndices = np.array(optimalTypesIndices)

    return randomPermutation, latitudes, longitudes, prices, accomodates, optimalTypes, optimalTypesIndices


def run(numAgents, numApplicants):
    print("Creating agents from the InsideAirbnb dataset...")

    np.set_printoptions(suppress=True)

    fileData = ""

    randomPermutation, latitudes, longitudes, prices, accomodates, optimalTypes, optimalTypesIndices = get_data()

    for i in range(numAgents):
        line = str(latitudes[randomPermutation[i]]) + "," + str(longitudes[randomPermutation[i]]) + "," + str(prices[randomPermutation[i]][1:]) + "," + str(accomodates[randomPermutation[i]]) + "," + str(optimalTypesIndices[randomPermutation[i]]) + "," + ','.join(map(str, optimalTypes[randomPermutation[i]])) + "\n"
        fileData += line.replace(" ", "")

    if not os_path.exists('../datasets/airbnb/'):
        os_makedirs('../datasets/airbnb/')

    with open('../datasets/airbnb/agentData.info', 'w+') as file:
        file.write(fileData)

