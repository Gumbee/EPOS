import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os


def extract_agent(i, lines):
    return lines[i].split(',')


size = 200

values = []

df = pandas.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/greedy/global-response.csv')
response = df.iloc[40]
response = response.values[2:]

with open(os.path.dirname(os.path.abspath(__file__)) + '/data/agentData.info') as file:
    lines = file.readlines()

for i in range(size):
    agent = extract_agent(i, lines)

    value = (float(agent[0]), float(agent[1]), response[size + size + i])
    values.append(value)

values.sort(key=lambda x: x[0])

latitudes = list(map(lambda x: x[0], values))
longitudes = list(map(lambda x: x[1], values))
sizes = list(map(lambda x: x[2], values))

trace = go.Scattermapbox(
    lon=longitudes,
    lat=latitudes,
    mode='markers',
    marker=dict(
        opacity=1,
        size=sizes,
        color='#f1c40f',
        colorscale='Viridis',
        showscale=False
    )
)

traces = [trace]

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
    xaxis=dict(
        title='#agents per applicant',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#555'
        ),
        type='linear',
        ticks='',
        dtick=0.5,
        range=[0, 2],
        autorange=True,
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
        dtick=3,
        autorange=True,
        showgrid=True,
        zeroline=True,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    ),
    mapbox=dict(
        accesstoken='key',
        bearing=0,
        center=dict(
            lat=np.average(latitudes)-0.02,
            lon=np.average(longitudes)-0.1,
        ),
        pitch=0,
        zoom=8.3,
        style='style'
    )
)
fig = go.Figure(data=traces, layout=layout)
py.plot(fig)

if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/images'):
    os.mkdir(os.path.dirname(os.path.abspath(__file__)) + '/images')

pio.orca.config.mapbox_access_token = 'key'
pio.orca.config.save()
pio.write_image(fig, os.path.dirname(os.path.abspath(__file__)) + '/images/plot12b.svg')
