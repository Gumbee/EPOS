import os
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio

def get_matching_conflicts(response):
    conflicts = response[response>1]
    C = 0
    for c in conflicts:
        C += c//2
    return C

# Import global response as Pands DataFrame
df_cooperative = pd.read_csv('./data/output/cooperative/global-response.csv')
df_greedy = pd.read_csv('./data/output/baseline/global-response.csv')

# Get number of applicants from configuration
with open('./data/output/cooperative/used_conf.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if "numApplicants = " in line:
            num_applicants = int(line.replace("numApplicants = ", ""))
        if "numAgents = " in line:
            num_agents = int(line.replace("numAgents = ", ""))

# Select applicant dimensions from global response
cols = ['dim-'+str(i) for i in range(num_applicants)]
applicants_cooperative = df_cooperative.loc[num_agents,cols]
applicants_greedy = df_greedy.loc[num_agents,cols]

conflicts_cooperative = get_matching_conflicts(applicants_cooperative)
conflicts_greedy = get_matching_conflicts(applicants_greedy)

# Plot
trace = go.Bar(
    x = ['Cooperative', 'Greedy'],
    y = [conflicts_cooperative/num_agents, conflicts_greedy/num_agents],
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

if not os.path.exists('images'):
    os.mkdir('images')

pio.write_image(fig, 'images/fig14.svg')