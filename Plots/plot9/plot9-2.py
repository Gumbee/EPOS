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
df = pd.read_csv('./data/output/cooperative/selected-plans.csv')
df_baseline = pd.read_csv('./data/output/baseline/selected-plans.csv')

# Get agent ids
agents = df.columns[2:]
num_agents = agents.shape[0]

# Get plan ids selected during last iteration
plan_ids = df.tail(n=1)
plan_ids_baseline = df_baseline.tail(n=1)

# Get number of applicants from configuration file
with open('./data/output/cooperative/used_conf.txt', 'r') as file:
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

# Repeat for baseline plans
plans_baseline = {}
for (i, agent) in enumerate(agents):
    filename = agent.replace('-', '_')+'.plans'
    with open(os.path.join('./data/plans', filename), 'r+') as file:
        lines = file.readlines()
        idx = plan_ids_baseline[agent].values[0]
        fields = np.array(lines[idx][4:].split(','), dtype=np.float32)
        applicant_id = np.where(fields[:num_applicants] == 1.0)[0][0]
        plans_baseline[agent] = {
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
local_cost_baseline = []
lat = []
lon = []
occupancy = []
occupancy_baseline = []
for agent in agents:
    local_cost.append(localcost(plans[agent], agent_data[agent]))
    local_cost_baseline.append(localcost(plans_baseline[agent], agent_data[agent]))
    lat.append(agent_data[agent]['lat'])
    lon.append(agent_data[agent]['lon'])
    occupancy.append(plans[agent]['occupancy'])
    occupancy_baseline.append(plans_baseline[agent]['occupancy'])
local_cost = np.array(local_cost)
local_cost_baseline = np.array(local_cost_baseline)
lat = np.array(lat)
lon = np.array(lon)
occupancy = np.array(occupancy)
occupancy_baseline = np.array(occupancy_baseline)

# Plot
trace = go.Scattermapbox(
    lon=lon,
    lat=lat,
    mode='markers',
    marker=dict(
        opacity=1,
        size=2*(occupancy*np.sqrt(2)),
        color='#f1c40f',
        colorscale='Viridis',
        showscale=False
    )
)
data = [trace]

layout = go.Layout(
    autosize=False,
    width=550,
    height=420,
    margin=dict(
        t=0,
        b=0,
        l=0,
        r=0
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    mapbox=dict(
        accesstoken='pk.eyJ1IjoiZ3VtYmVlIiwiYSI6ImNqbmhtMjJ5YzBmYTkzcG55cDZlOXF0aGcifQ.zi-z-hT9ez-BtDU8LlicOA',
        bearing=0,
        center=dict(
            lat=np.average(lat)-0.02,
            lon=np.average(lon)-0.1,
        ),
        pitch=0,
        zoom=8.3,
        style='mapbox://styles/gumbee/cjnhnhix44mut2sqyffmx6tfn'
    )
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, auto_open=False)

if not os.path.exists('images'):
    os.mkdir('images')

pio.orca.config.mapbox_access_token = 'pk.eyJ1IjoiZ3VtYmVlIiwiYSI6ImNqbmhtMjJ5YzBmYTkzcG55cDZlOXF0aGcifQ.zi-z-hT9ez-BtDU8LlicOA'
pio.orca.config.save()
pio.write_image(fig, 'images/fig9-2-0.2.svg')

trace = go.Scattermapbox(
    lon=lon,
    lat=lat,
    mode='markers',
    marker=dict(
        opacity=1,
        size=2*(occupancy_baseline*np.sqrt(2)),
        color='#f1c40f',
        colorscale='Viridis',
        showscale=False,
        colorbar=dict(
            thickness=10,
            titleside='right',
            ticks='outside',
            ticklen=3,
            dtick=2
        )
    )
)
data = [trace]

layout = go.Layout(
    autosize=False,
    width=550,
    height=420,
    margin=dict(
        t=0,
        b=0,
        l=0,
        r=0
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    mapbox=dict(
        accesstoken=your_key_here,
        bearing=0,
        center=dict(
            lat=np.average(lat)-0.02,
            lon=np.average(lon)-0.1,
        ),
        pitch=0,
        zoom=8.3,
        style='mapbox://styles/gumbee/cjnhnhix44mut2sqyffmx6tfn'
    )
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, auto_open=False)

if not os.path.exists('images'):
    os.mkdir('images')

pio.orca.config.mapbox_access_token = your_key_here
pio.orca.config.save()
pio.write_image(fig, 'images/fig9-2-1.svg')