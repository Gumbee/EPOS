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


numAgents = get_num_agents()
numApplicants = get_num_applicants()

AgentGenerator.run(numAgents, numApplicants)
GoalGenerator.run(numAgents, numApplicants)
PlanGenerator.run(numAgents, numApplicants)
