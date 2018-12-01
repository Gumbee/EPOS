import numpy as np

import plotly.graph_objs as go
import plotly.offline as py

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

    return density


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def run(numAgents, numApplicants):
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

        target = max(price-50, price/2, price-density)
        goal_price.append(target)
        occ_target = 10 / (density / 5)
        goal_occupancy.append(occ_target)
        sizes.append(occ_target)

    for i in range(numAgents):
        colors.append('red' if i == max_i else 'yellow')

    goal_matching = np.array(goal_matching)
    goal_price = np.array(goal_price)
    goal_occupancy = np.array(goal_occupancy)

    fileData = ""

    """
    trace1 = go.Scattermapbox(
        lon=longitudes[randomPermutation[:numAgents]],
        lat=latitudes[randomPermutation[:numAgents]],
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            colorscale='Viridis',
            showscale=False
        )
    )

    data = [trace1]

    layout = go.Layout(
        autosize=False,
        width=700,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#fff',
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=True,
            showline=False,
            ticks='',
            color='#ccc',
            showticklabels=True
        ),
        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=True,
            showline=False,
            ticks='',
            color='#ccc',
            showticklabels=True
        ),
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiZ3VtYmVlIiwiYSI6ImNqbmhtMjJ5YzBmYTkzcG55cDZlOXF0aGcifQ.zi-z-hT9ez-BtDU8LlicOA',
            bearing=0,
            center=dict(
                lat=np.average(latitudes[randomPermutation[:numAgents]]),
                lon=np.average(longitudes[randomPermutation[:numAgents]]),
                # lat=39.608532,
                # lon=2.892268,
            ),
            pitch=0,
            zoom=8.3,
            style='mapbox://styles/gumbee/cjnhnhix44mut2sqyffmx6tfn'
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig)
    """

    for i in range(numApplicants):
        fileData += str(goal_matching[i]).replace(" ", "") + ","

    for i in range(numAgents):
        fileData += str(goal_price[i]).replace(" ", "") + ","

    for i in range(numAgents - 1):
        fileData += str(goal_occupancy[i]).replace(" ", "") + ","

    fileData += str(goal_occupancy[numAgents - 1]).replace(" ", "")

    with open('../datasets/airbnb/goal.target', 'w+') as file:
        file.write(fileData)