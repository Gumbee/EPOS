import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os

fileid = 0
numIterations = 40
agentid=0
num_plan_changes = 0
num_experiment = 0
plan_changes_list=[]	# amount of plant changes per agent
numAgents = 30
lambda_values = [0,10,20]

for fileid in lambda_values:
	df = pandas.read_csv('./lambda'+str(fileid)+'/selected-plans.csv')

	for agentid in range(numAgents):
		selected_plans = df['agent-'+str(agentid)].values
		num_plan_changes = 0

		for current_iteration in range(numIterations-1):
			if not (selected_plans[current_iteration+(num_experiment*numIterations)] == selected_plans[(current_iteration+1)+(num_experiment*numIterations)]):
				num_plan_changes += 1
			if current_iteration+1 is numIterations-1:
				break

		plan_changes_list.append(num_plan_changes)


# print(plan_changes_list)
# print(len(plan_changes_list))
# print(num_experiment)

plan_changes_0 = plan_changes_list[:30]			# plan changes for lambda = 0
plan_changes_10 = plan_changes_list[31:60]		# plan changes for lambda = 0.5
plan_changes_20 = plan_changes_list[61:90]		# plan changes for lambda = 1

agents = np.linspace(0, numAgents-1, numAgents)

trace1 = go.Bar(
	x=agents,
	y=plan_changes_0,
	name='\lambda =0')

trace2 = go.Bar(
	x=agents,
	y=plan_changes_10,
	name='\lambda =0.5')

trace3 = go.Bar(
	x=agents,
	y=plan_changes_20,
	name='\lambda =1')

data = [trace1,trace2,trace3]

layout = go.Layout(
	barmode='group',
	autosize=False,
    width=800,
    height=320,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='Agent',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        tickmode='linear',
        ticks='',
        dtick=2,
        range=[-1, len(agents)-1],
        autorange=False,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='Plan changes',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        autorange=True,
        showgrid=True,
        zeroline=False,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    )
	)

fig = go.Figure(data=data, layout=layout)
py.plot(fig)

if not os.path.exists('images'):
    os.mkdir('images')

pio.write_image(fig, 'images/plan_changes.svg')