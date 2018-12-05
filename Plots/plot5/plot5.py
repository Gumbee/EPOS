import os
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio

# Import average final local cost form all datasets
# and log beta value used for the optimization
paths = [name for name in os.listdir('./data') if os.path.isdir(os.path.join('./data', name))]
beta = []
localcost = []
stddev = []
for path in paths:
    with open(os.path.join('./data', path, 'used_conf.txt'), 'r+') as conf:
        lines = conf.readlines()
        for line in lines:
            if 'beta' in line:
                beta.append(float(line.replace("beta = ", "")))

    with open(os.path.join('./data', path, 'local-cost.csv'), 'r+') as file:
        lines = file.readlines()
        fields = lines[-1].split(',')
        localcost.append(fields[1])
        stddev.append(fields[2])

# Sort data points
perm = np.argsort(beta)
beta = np.array(beta)[perm]
localcost = np.array(localcost)[perm]
stddev = np.array(stddev)[perm]

# Plot the local cost as a function of beta
trace = go.Scatter(
    x = beta,
    y = localcost,
    error_y=dict(
        type='data',
        array=stddev,
        visible=True
    ),
    mode = 'lines+markers',
    marker=dict(
        size=1,
        colorscale='Viridis',
        opacity=1,
        line = dict(
            color = 'rgb(231, 99, 250)',
            width = 0
          ),
        showscale=False
    )
)
data = [trace]
layout = go.Layout(
    autosize=False,
    width=700,
    height=300,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='\\lambda',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        tickmode='linear',
        ticks='',
        dtick=0.1,
        range=[-0.05, 1.05],
        autorange=False,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='Average Local Cost',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        dtick=2,
        autorange=False,
        range=[5,17],
        showgrid=True,
        zeroline=True,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, auto_open=False)

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/fig5.svg')