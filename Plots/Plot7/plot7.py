import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os


def get_directories():
    return os.listdir(os.path.dirname(os.path.abspath(__file__)) + '/data/')


def extract_agents(lines):
    for line in lines:
        spaceLessLine = line.replace(" ", "")
        if "numAgents=" in spaceLessLine:
            return spaceLessLine.replace("numAgents=", "")


def extract_applicants(lines):
    for line in lines:
        spaceLessLine = line.replace(" ", "")
        if "numApplicants=" in spaceLessLine:
            return spaceLessLine.replace("numApplicants=", "")


def get_num_conflicts(responses):
    collisions = 0

    for response in responses:
        if response > 1:
            collisions += np.square(response-1)

    return collisions

values = []

for directory in get_directories():
    if directory.startswith('.'):
        continue

    lines = []

    with open(os.path.dirname(os.path.abspath(__file__)) + '/data/' + directory + '/used_conf.txt') as file:
        lines = file.readlines()

    num_agents = extract_agents(lines)
    num_applicants = extract_applicants(lines)

    df = pandas.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/' + directory + '/global-response.csv')
    response = df.iloc[40]
    response = response.values[2:int(num_applicants)]

    num_conflicts = get_num_conflicts(response[:int(num_applicants)])

    value = (float(num_agents)/float(num_applicants), np.sqrt(num_conflicts/int(num_applicants)))
    values.append(value)


values.sort(key=lambda x: x[0])

trace = go.Scatter(
    x=list(map(lambda x: x[0], values)),
    y=list(map(lambda x: x[1], values)),
    mode='lines+markers',
    marker=dict(
        size=1,
        colorscale='Viridis',
        opacity=1,
        line=dict(
            width=3
        ),
        showscale=False
    )
)

traces = [trace]

layout = go.Layout(
    autosize=False,
    width=700,
    height=230,
    margin=dict(
        t=25,
        b=40
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='\#agents per applicant',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#555'
        ),
        type='linear',
        ticks='',
        dtick=0.5,
        range=[-0.1, 10],
        autorange=False,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='\\sqrt{avg\\text{ of }collision^2}',
        titlefont=dict(
            family='Arial',
            size=10,
            color='#555'
        ),
        range=[0,10],
        dtick=2,
        autorange=False,
        showgrid=True,
        zeroline=True,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    )
)

fig = go.Figure(data=traces, layout=layout)
py.plot(fig)

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/plot7.svg')
