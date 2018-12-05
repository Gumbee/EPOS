import os
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio


def get_matching_conflicts(response):
    conflicts = response[response>0]
    return 1.0*len(conflicts)/len(response)

# Import global response as Pands DataFrame
df_cooperative = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '//data/output/cooperative/global-response.csv')
df_greedy = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '//data/output/baseline/global-response.csv')

# Get number of applicants from configuration
with open(os.path.dirname(os.path.abspath(__file__)) + '/data/output/cooperative/used_conf.txt', 'r') as file:

    lines = file.readlines()
    for line in lines:
        if "numApplicants = " in line:
            num_applicants = int(line.replace("numApplicants = ", ""))
        if "numAgents = " in line:
            num_agents = int(line.replace("numAgents = ", ""))

# Select applicant dimensions from global response
applicants_cooperative = df_cooperative.iloc[40]
applicants_cooperative = applicants_cooperative.values[2:]
applicants_cooperative = applicants_cooperative[:num_applicants]
applicants_greedy = df_greedy.iloc[40]
applicants_greedy = applicants_greedy.values[2:]
applicants_greedy = applicants_greedy[:num_applicants]


conflicts_cooperative = get_matching_conflicts(applicants_cooperative)
conflicts_greedy = get_matching_conflicts(applicants_greedy)

# Plot
trace = go.Bar(
    x=['Cooperative', 'Greedy'],
    y = [1-conflicts_cooperative, 1-conflicts_greedy],
    marker=dict(
        colorscale='Viridis',
        opacity=1,
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
        ticks='',
        autorange=True,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='Conflict probability',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        dtick=0.1,
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
py.plot(fig, auto_open=False)

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/plot14.svg')