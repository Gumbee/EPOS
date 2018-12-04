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
            'lat': float(fields[0]),
            'lon': float(fields[1]),
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
lat = []
lon = []
for agent in agents:
    local_cost.append(localcost(plans[agent], agent_data[agent]))
    lat.append(agent_data[agent]['lat'])
    lon.append(agent_data[agent]['lon'])
local_cost = np.array(local_cost)
lat = np.array(lat)
lon = np.array(lon)
# print(local_cost.mean())

# Plot
trace = dict(
    type = 'scattergeo',
    lat = lat,
    lon = lon,
    marker=dict(
        #color = local_cost,
        #colorscale='Viridis',
        opacity=0.6,
        size = np.round(local_cost),
        line = dict(
            color = 'rgb(231, 99, 250)',
            width = 1.5
          ),
        showscale=False
    )
)
data = [trace]
layout = dict(
    title = 'Local cost distribution',
    geo = dict(
        scope='europe',
        showland = True,
        landcolor = "rgb(0, 0, 0)",
        subunitcolor = "rgb(217, 217, 217)",
        countrycolor = "rgb(217, 217, 217)",
        countrywidth = 0.5,
        subunitwidth = 0.5,
        lonaxis = dict(
            showgrid = True,
            gridwidth = 0.5,
            range= [ lon.min(), lon.max() ],
            dtick = 5
        ),
        lataxis = dict (
            showgrid = True,
            gridwidth = 0.5,
            range= [ lat.min(), lat.max() ],
            dtick = 5
        )
    ),
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, auto_open=False)

if not os.path.exists('images'):
    os.mkdir('images')

pio.write_image(fig, 'images/fig8-2.svg')