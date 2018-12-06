#!/usr/bin/env python
import statistics
import math
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import pandas
import plotly.io as pio
import os

#numAgents = 10

def get_num_agents():
    with open('.conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "numAgents=" in line:
                return int(line.replace("numAgents=", ""))

def get_num_applicants():
    with open('./conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "numApplicants=" in line:
                return int(line.replace("numApplicants=", ""))

def get_options_applicants():
    with open('./conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "applicantOptions=" in line:
                return int(line.replace("applicantOptions=", ""))


def get_options_price():
    with open('./conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "priceOptions=" in line:
                return int(line.replace("priceOptions=", ""))

def get_plans(agent_id):
    # code which reads all possible plans of agent_id and saves all plans in a list and returns that list
    # the plan is just a list of values
    plan = []
    # the list of plans is a list of lists(plans)
    list_of_plans = []
    with open("./airbnb_small/airbnb/agent_" + str(agent_id) + ".plans", "r") as data:
        print("Reading plans for " + str(agent_id) +" agent...")
        numPlans = Applicants_options*Price_options
        for plan_id in range(numPlans):
            plan = data.readline().replace('\n','')[4:]    # Eliminates score and line break characters
            plan = list(map(float,plan.split(",")))         # converts huge string into list of strings into list of floats (plan as a list of values) 
            #plan = str(plan).replace('\\n', '')
            list_of_plans.append(plan)
    
    return list_of_plans


numApplicants=get_num_applicants()       
numAgents=get_num_agents()
Applicants_options =get_options_applicants()
Price_options =get_options_price()

occupancies=[]
prices=[]

for agent_id in range(numAgents):
    current_list_of_plans = get_plans(agent_id)
    for plan_id in range(Applicants_options):
    #for plan_id in range(len(current_list_of_plans)):   #looking at each plan for the current agent
        current_plan=current_list_of_plans[plan_id]
        #price_part = current_plan[numApplicants:numApplicants+numAgents]
        occupancy_part = current_plan[numApplicants+numAgents:]
        occupancies.append(occupancy_part[next((i for i, x in enumerate(occupancy_part) if x),None)])
        #for i in range(len(occupancy_part)):

    for plan_id in range(Price_options):
        current_plan=current_list_of_plans[plan_id*Applicants_options]
        price_part = current_plan[numApplicants:numApplicants+numAgents]
        prices.append(price_part[next((i for i, x in enumerate(price_part) if x),None)])

#print(occupancies)
#print(prices)



new_list_occupancy=[]
no_times_occupancy=[]

for i in occupancies:
    if not (i in new_list_occupancy):
        no_times_occupancy.append(occupancies.count(i))
        new_list_occupancy.append(i)

new_list_prices=[]
no_times_prices=[]

for i in prices:
    if not (i in new_list_prices):
        no_times_prices.append(prices.count(i))
        new_list_prices.append(i)


# trace1 = go.Bar(
#     x=new_list_occupancy,
#     y=no_times_occupancy,
#     width=[0.5]*len(new_list_occupancy),
#     name='\lambda =0')


# data = [trace1]

# layout = go.Layout(
#     barmode='group',
#     autosize=False,
#     width=800,
#     height=320,
#     paper_bgcolor='rgba(0,0,0,0)',
#     plot_bgcolor='#fff',
#     xaxis=dict(
#         title='Occupancies',
#         titlefont=dict(
#             family='Arial',
#             size=14,
#             color='#666'
#         ),
#         tickmode='linear',
#         ticks='',
#         dtick=1,
#         range=[0,max(new_list_occupancy)+0.5],
#         autorange=False,
#         showgrid=True,
#         zeroline=False,
#         showline=False,
#         color='#888',
#         showticklabels=True
#     ),
#     yaxis=dict(
#         title='Count',
#         titlefont=dict(
#             family='Arial',
#             size=14,
#             color='#666'
#         ),
#         range=[0,max(no_times_occupancy)+1],
#         autorange=False,
#         showgrid=True,
#         zeroline=False,
#         showline=False,
#         ticks='',
#         color='#888',
#         showticklabels=True
#     )
#     )

# fig = go.Figure(data=data, layout=layout)
# py.plot(fig)

# if not os.path.exists('images'):
#     os.mkdir('images')

# pio.write_image(fig, 'images/histogram.svg')




trace2 = go.Bar(
    x=new_list_prices,
    y=no_times_prices,
    width=[5]*len(new_list_prices),
    name='\lambda =0')


data2 = [trace2]

layout2 = go.Layout(
    barmode='group',
    autosize=False,
    width=800,
    height=320,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#fff',
    xaxis=dict(
        title='Prices',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        tickmode='linear',
        ticks='',
        dtick=100,
        range=[min(new_list_prices)-5,max(new_list_prices)+5],
        autorange=False,
        showgrid=True,
        zeroline=False,
        showline=False,
        color='#888',
        showticklabels=True
    ),
    yaxis=dict(
        title='Count',
        titlefont=dict(
            family='Arial',
            size=14,
            color='#666'
        ),
        range=[0,max(no_times_prices)+0.5],
        autorange=False,
        showgrid=True,
        zeroline=False,
        showline=False,
        ticks='',
        color='#888',
        showticklabels=True
    )
    )

fig2 = go.Figure(data=data2, layout=layout2)
py.plot(fig2)

if not os.path.exists('images'):
    os.mkdir('images')

pio.write_image(fig2, 'images/histogram2.svg')

