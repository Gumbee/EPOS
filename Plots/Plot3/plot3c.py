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


def extract_num_agents(lines):
    for line in lines:
        spaceLessLine = line.replace(" ", "")
        if "numAgents=" in spaceLessLine:
            return spaceLessLine.replace("numAgents=", "")


def extract_num_applicants(lines):
    for line in lines:
        spaceLessLine = line.replace(" ", "")
        if "numApplicants=" in spaceLessLine:
            return spaceLessLine.replace("numApplicants=", "")


def extract_goal_signal():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/data/goal.target') as file:
        line = file.readline()

        splitLine = line.split(',')
        result = np.array(splitLine).astype(float)
        return result


traces = []

target = extract_goal_signal()

for directory in get_directories():
    if directory.startswith('.') or "goal.target" in directory:
        continue

    df = pandas.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/' + directory + '/global-response.csv')
    response = df.iloc[40]
    response = response.values[2:]

    ef = pandas.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/' + directory + '/weights-alpha-beta.csv')
    weights = ef['Local cost weight'].values

    with open(os.path.dirname(os.path.abspath(__file__)) + '/data/' + directory + '/used_conf.txt') as file:
        lines = file.readlines()

    numAgents = int(extract_num_agents(lines))
    numApplicants = int(extract_num_applicants(lines))

    if not weights[0] in [0, 1]:
        continue

    rangeStart = numApplicants+numAgents
    rangeEnd = numApplicants+numAgents*2

    trace = go.Bar(
        x=np.arange(rangeEnd-rangeStart),
        y=np.abs(np.subtract(response[rangeStart:rangeEnd], target[rangeStart:rangeEnd])),
        name='\lambda=' + str(weights[0])
    )

    value = (weights[0], trace)
    traces.append(value)

layout = go.Layout(
    autosize=False,
    width=700,
    height=150,
    margin=dict(
        t=25,
        b=40
    ),
    barmode='group',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='agent',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#555'
        ),
        tickmode='linear',
        ticks='',
        dtick=2,
        range=[-1, 100],
        autorange=True,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='\| target - response \|',
        titlefont=dict(
            family='Arial',
            size=10,
            color='#555'
        ),
        autorange=True,
        showgrid=True,
        zeroline=True,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    ),
    title='Occupancy Global Response',
    titlefont=dict(
        family='Arial',
        size=14,
        color='#555'
    ),
)

traces.sort(key=lambda x: x[0])

fig = go.Figure(data=list(map(lambda x: x[1], traces)), layout=layout)
py.plot(fig)

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/plot3c.svg')
