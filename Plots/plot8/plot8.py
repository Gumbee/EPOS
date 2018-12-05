import os
import numpy as np
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio

def localcost(plan, agent, stacked=False):
    price_cost = np.sqrt((plan['price']-agent['optimalPrice'])**2)
    occupancy_cost = np.sqrt((plan['occupancy']-agent['optimalOccupancy'])**2)
    type_cost = np.sqrt((agent['rank'+str(plan['type'])]-agent['rank'+str(agent['optimalType'])])**2)
    if stacked:
        return [price_cost, occupancy_cost, type_cost]
    return price_cost+occupancy_cost+type_cost

# Import selected plans as Pands DataFrame
df = pd.read_csv('./data/output/selected-plans.csv')

# Get agent ids
agents = df.columns[2:]
num_agents = agents.shape[0]

# Get plan ids selected during last iteration
plan_ids = df.tail(n=1)

# Get number of applicants from configuration file
with open('./data/output/used_conf.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if "numApplicants = " in line:
            num_applicants = int(line.replace("numApplicants = ", ""))

# Import plans selected by I-EPOS
plans = {}
applicant_pool = pd.read_csv('./data/plans/applicant_pool.csv', header=None, names=['group_size', 'type'])
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
local_cost = []
for agent in agents:
    local_cost.append(localcost(plans[agent], agent_data[agent]))
# local_cost = np.array(local_cost)
# print(local_cost.mean())

# Plot
trace = go.Bar(
    x = np.arange(num_agents),
    y = local_cost,
    marker=dict(
        colorscale='Viridis',
        opacity=1,
        showscale=False
    )
)
data = [trace]
layout = go.Layout(
    title='Local Cost of Selected Plan',
    autosize=False,
    width=800,
    height=450,
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
        title='Local Cost',
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

pio.write_image(fig, 'images/fig8.svg')

# Compute local costs
local_cost = []
for agent in agents:
    local_cost.append(localcost(plans[agent], agent_data[agent], stacked=True))
local_cost = np.array(local_cost)
# print(local_cost.mean())

# Plot
trace_price = go.Bar(
    x = np.arange(num_agents),
    y = local_cost[:,0],
    name = 'Price',
    marker=dict(
        colorscale='Viridis',
        opacity=1,
        showscale=False
    )
)
trace_occupancy = go.Bar(
    x = np.arange(num_agents),
    y = local_cost[:,1],
    name = 'Occupancy',
    marker=dict(
        colorscale='Viridis',
        opacity=1,
        showscale=False
    )
)
trace_type = go.Bar(
    x = np.arange(num_agents),
    y = local_cost[:,2],
    name = 'Type',
    marker=dict(
        colorscale='Viridis',
        opacity=1,
        showscale=False
    )
)
data = [trace_price, trace_occupancy, trace_type]
layout = go.Layout(
    title='Local Cost of Selected Plan',
    barmode='stack',
    autosize=False,
    width=800,
    height=450,
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
        title='Local Cost',
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

pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/fig8-1.svg')