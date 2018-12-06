
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os

df = pandas.read_csv('./airbnb_costs/global-cost.csv')

g_costs = df['Mean'].values
iterations_2 = []

with open("./datasets/airbnb/brute_force.costs", "r") as file:
    costs = file.readline().replace('\n','')
    costs = costs.replace('[','')
    costs = costs.replace(']','')
    costs = list(map(float,costs.split(",")))

costs.sort(reverse=True)        #Brute force cost
iterations = np.linspace(0, len(costs)-1, len(costs))

for i in g_costs:
    for j in costs:
        if abs(i-j) <0.05:
            print('i= ' +str(i) +'   j= '+str(j))
            iterations_2.append(iterations[costs.index(j)])
            break

#print(iterations_2)

trace1 = go.Scatter(
    x = iterations,
    y = costs,
    name='Brute Force',
    mode='lines',
    marker=dict(
        size=1,
        colorscale='Viridis',
        color='rgb(200,50,70)',
        opacity=1,
        line = dict(
            color = 'rgb(200,50,70)',
            width = 4
          ),
        showscale=False
    )
)

trace2 = go.Scatter(
    x = iterations_2,
    y = g_costs,
    name='I-EPOS',
    mode='markers',
    marker=dict(
        symbol='x-open',
        size=1,
        colorscale='Viridis',
        color='rgb(0,0,0)',
        opacity=1,
        line = dict(
            color = 'rgb(0,0,0)',
            width = 6
          ),
        showscale=False
    )
)


data = [trace1, trace2]

layout = go.Layout(
    autosize=False,
    width=800,
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='Solution',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        tickmode='linear',
        ticks='',
        dtick=1000,
        range=[-400, 8000],#len(costs)],
        autorange=False,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='Global Cost',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        autorange=True,
        showgrid=True,
        zeroline=True,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    )
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig)

if not os.path.exists('images'):
    os.mkdir('images')

pio.write_image(fig, 'images/BFvsEPOS2.svg')