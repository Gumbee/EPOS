import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os


def get_directories():
    return os.listdir(os.path.dirname(os.path.abspath(__file__)) + '/data/')


def extract_applicant_options(lines):
    for line in lines:
        spaceLessLine = line.replace(" ", "")
        if "applicantOptions=" in spaceLessLine:
            return spaceLessLine.replace("applicantOptions=", "")


def extract_price_options(lines):
    for line in lines:
        spaceLessLine = line.replace(" ", "")
        if "priceOptions=" in spaceLessLine:
            return spaceLessLine.replace("priceOptions=", "")


values = []

for directory in get_directories():
    if directory.startswith('.'):
        continue

    df = pandas.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/' + directory + '/global-cost.csv')
    iterations = df['Iteration'].values
    costs = df['Mean'].values

    lines = []

    with open(os.path.dirname(os.path.abspath(__file__)) + '/data/' + directory + '/used_conf.txt') as file:
        lines = file.readlines()

    value = (int(extract_applicant_options(lines))*int(extract_price_options(lines)), costs[39])
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
            width=0
        ),
        showscale=False
    )
)

traces = [trace]

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
        title='\# of plans per agent',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#555'
        ),
        ticks='',
        dtick=30,
        range=[-1, 400],
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
        range=[17, 62],
        autorange=False,
        showgrid=True,
        zeroline=True,
        showline=False,
        ticks='',
        color='#555',
        showticklabels=True
    )
)

fig = go.Figure(data=traces, layout=layout)
py.plot(fig)

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/plot2.svg')
