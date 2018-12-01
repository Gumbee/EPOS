import GeneratorScripts.agent_generator as AgentGenerator
import GeneratorScripts.plan_generator as PlanGenerator
import GeneratorScripts.goal_generator as GoalGenerator


def get_num_agents():
    with open('../conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "numAgents=" in line:
                return int(line.replace("numAgents=", ""))


def get_num_applicants():
    with open('../conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "numApplicants=" in line:
                return int(line.replace("numApplicants=", ""))


def get_options_applicants():
    with open('../conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "applicantOptions=" in line:
                return int(line.replace("applicantOptions=", ""))


def get_options_price():
    with open('../conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "priceOptions=" in line:
                return int(line.replace("priceOptions=", ""))


numAgents = get_num_agents()
numApplicants = get_num_applicants()
options_applicants = get_options_applicants()
options_price = get_options_price()

AgentGenerator.run(numAgents, numApplicants)
GoalGenerator.run(numAgents, numApplicants)
PlanGenerator.run(numAgents, numApplicants, options_applicants, options_price)
