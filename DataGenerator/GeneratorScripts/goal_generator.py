import numpy as np

from GeneratorScripts.agent_generator import get_data


max_i = 0
max_val = 0


def get_density(id, randomPermutation, latitudes, longitudes, numAgents):
    lat = latitudes[randomPermutation[id]]
    lon = longitudes[randomPermutation[id]]

    density = 0
    global max_val
    global max_i

    for j in range(numAgents):
        if id != j:
            otherLat = latitudes[randomPermutation[j]]
            otherLon = longitudes[randomPermutation[j]]

            norm = np.sqrt(np.square(lat - otherLat) + np.square(lon - otherLon))
            # print("We have a norm of: " + str(norm) + " which gives us " + str(gaussian(norm)))
            density += gaussian(norm, 0, 0.05)

    if density > max_val:
        max_val = density
        max_i = id

    density = density/numAgents*100

    return density


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def price_multiplier(density):
    if density <= 4:
        return (4-density)*6
    else:
        return (4-density)*3


def run(numAgents, numApplicants):
    print("Creating the goal signal based on density measurements...")

    randomPermutation, latitudes, longitudes, prices, _, _, _ = get_data()

    goal_matching = []
    goal_price = []
    goal_occupancy = []
    sizes = []
    colors = []

    for i in range(numApplicants):
        goal_matching.append(1)

    for i in range(numAgents):
        price = float(prices[randomPermutation[i]].replace(",", "").replace("$", ""))

        density = get_density(i, randomPermutation, latitudes, longitudes, numAgents)

        target = max(price-50, price/2, price-price_multiplier(density))
        target = min(price+50, price*3.0/2, target)
        goal_price.append(target)
        occ_target = min(10, 10/(density))
        occ_target = max(1, occ_target)
        goal_occupancy.append(occ_target)
        sizes.append(occ_target)

    for i in range(numAgents):
        colors.append('red' if i == max_i else 'yellow')

    goal_matching = np.array(goal_matching)
    goal_price = np.array(goal_price)
    goal_occupancy = np.array(goal_occupancy)

    fileData = ""

    for i in range(numApplicants):
        fileData += str(goal_matching[i]).replace(" ", "") + ","

    for i in range(numAgents):
        fileData += str(goal_price[i]).replace(" ", "") + ","

    for i in range(numAgents - 1):
        fileData += str(int(goal_occupancy[i])).replace(" ", "") + ","

    fileData += str(int(goal_occupancy[numAgents - 1])).replace(" ", "")

    with open('../datasets/airbnb/goal.target', 'w+') as file:
        file.write(fileData)
