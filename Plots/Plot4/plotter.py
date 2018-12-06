
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os

numExperiments = 21
final_costs = []
lambda_list = []
final_deviations = []

for fileid in range(numExperiments):
    df = pandas.read_csv('./lambda'+str(fileid)+'/global-cost.csv')
    costs = df['Mean'].values
    deviation = df['Stdev'].values

    final_costs.append(costs[-1])
    final_deviations.append(deviation[-1])


    df1 = pandas.read_csv('./lambda'+str(fileid)+'/weights-alpha-beta.csv')
    lambdas = df1['Local cost weight'].values
    lambda_list.append(lambdas[-1])


trace = go.Scatter(
    x = lambda_list,
    y = final_costs,
    mode='lines+markers',
    error_y =dict(
        type='data',
        array= final_deviations,
        visible=True
        ),
    marker=dict(
        size=1,
        colorscale='Viridis',
        color='rgb(50,70,130)',
        opacity=1,
        line = dict(
            color = 'rgb(50,70,130)',
            width = 4
          ),
        showscale=False
    )
)


data = [trace]

layout = go.Layout(
    autosize=False,
    width=800,
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='Greediness (\lambda)',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        tickmode='linear',
        ticks='',
        dtick=0.1,
        range=[-0.02, 1.02],
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
        zeroline=False,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    )
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='latex')

if not os.path.exists('images'):
    os.mkdir('images')

pio.write_image(fig, 'images/GCvsLAMBDA.svg')