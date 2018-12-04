import os
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio

def missmatch(plan, agent):
    return np.abs(agent['rank'+str(plan['type'])]-agent['rank'+str(agent['optimalType'])])

# Import selected plans as Pands DataFrame
df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/output/selected-plans.csv')

# Get agent ids
agents = df.columns[2:]
num_agents = agents.shape[0]

# Get plan ids selected during last iteration
plan_ids = df.tail(n=1)

# Get number of applicants from configuration file
with open(os.path.dirname(os.path.abspath(__file__)) + '/data/output/used_conf.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if "numApplicants = " in line:
            num_applicants = int(line.replace("numApplicants = ", ""))

# Import plans selected by I-EPOS
plans = {}
applicant_pool = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/plans/applicant_pool.csv', header=None, names=['group_size', 'type'])
applicant_types = {
    'SINGLE': 0,
    'COUPLE': 1,
    'FAMILY': 2,
    'GROUP': 3,
    'BUSINESS': 4
}
for (i, agent) in enumerate(agents):
    filename = agent.replace('-', '_')+'.plans'
    with open(os.path.join('./data/plans', filename), 'r+') as file:
        lines = file.readlines()
        idx = plan_ids[agent].values[0]
        fields = np.array(lines[idx][4:].split(','), dtype=np.float32)
        applicant_id = np.where(fields[:num_applicants] == 1.0)[0][0]
        plans[agent] = {
            'price': fields[num_applicants+i],
            'occupancy': fields[num_applicants+num_agents+i],
            'type': applicant_types[applicant_pool.iloc[applicant_id]['type']]
        }

# Import agent data
agent_data = {}
with open('./data/plans/agentData.info', 'r+') as data:
    lines = data.readlines()
    for (i, line) in enumerate(lines):
        fields = line.split(',')
        agent_data[agents[i]] = {
            'optimalPrice': float(fields[2]),
            'optimalOccupancy': int(fields[3]),
            'optimalType': int(fields[4]),
            'rank0': float(fields[5]),
            'rank1': float(fields[6]),
            'rank2': float(fields[7]),
            'rank3': float(fields[8]),
            'rank4': float(fields[9])
        }

# Compute local costs
type_missmatch = []
for agent in agents:
    type_missmatch.append(missmatch(plans[agent], agent_data[agent]))
# local_cost = np.array(local_cost)
# print(local_cost.mean())

# Plot
trace = go.Bar(
    x = np.arange(num_agents),
    y = type_missmatch,
    marker=dict(
        colorscale='Viridis',
        opacity=0.6,
        line = dict(
            color = 'rgb(231, 99, 250)',
            width = 1.5
          ),
        showscale=False
    )
)
data = [trace]
layout = go.Layout(
    autosize=False,
    width=700,
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='Agent',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        ticks='',
        autorange=True,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='Type Missmatch',
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

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/fig10.svg')

