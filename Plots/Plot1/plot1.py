import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os

df = pandas.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/lambdaZero/global-cost.csv')
iterations = df['Iteration'].values
costs = df['Mean'].values

trace = go.Scatter(
    x = iterations,
    y = costs,
    mode='lines+markers',
    marker=dict(
        size=1,
        colorscale='Viridis',
        opacity=1,
        line = dict(
            color = 'rgb(10, 10, 10)',
            width = 0
          ),
        showscale=False
    ),
    name='With cooperation'
)

df = pandas.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/lambdaOne/global-cost.csv')
iterations = df['Iteration'].values
costs = df['Mean'].values

traceBase = go.Scatter(
    x = iterations,
    y = costs,
    mode='lines+markers',
    marker=dict(
        size=1,
        colorscale='Viridis',
        opacity=1,
        line = dict(
            color = 'rgb(10, 10, 10)',
            width = 0
          ),
        showscale=False
    ),
    name='Without cooperation'
)


data = [trace, traceBase]

layout = go.Layout(
    autosize=False,
    width=700,
    height=150,
    margin=dict(
        t=25,
        b=40
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='iteration',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#555'
        ),
        tickmode='linear',
        ticks='',
        dtick=2,
        range=[-1, 39],
        autorange=False,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='global cost',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#555'
        ),
        range=[15, 70],
        autorange=False,
        showgrid=True,
        zeroline=True,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    ),
    legend=dict(
        y=0.5
    )
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig)

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/plot1.svg')