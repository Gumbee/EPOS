import subprocess
import numpy as np


def set_settings(numAgents, numApplicants, lambdaValue, applicantOptions, priceOptions):
    new_lines = ""

    with open('conf/epos.properties', 'r') as file:
        lines = file.readlines()

        for line in lines:
            spaceless_line = line.replace(" ", "")
            if "#" in spaceless_line:
                new_lines += line.replace("\n", "")
            elif "numAgents=" in spaceless_line:
                new_lines += "numAgents=" + str(numAgents)
            elif "numApplicants=" in spaceless_line:
                new_lines += "numApplicants=" + str(numApplicants)
            elif "weightsString=" in spaceless_line:
                new_lines += "weightsString=" + '"0.0,' + str(lambdaValue) + '"'
            elif "applicantOptions=" in spaceless_line:
                new_lines += "applicantOptions=" + str(applicantOptions)
            elif "priceOptions=" in spaceless_line:
                new_lines += "priceOptions=" + str(priceOptions)
            else:
                new_lines += spaceless_line.replace("\n", "")
            new_lines += "\n"

    with open('conf/epos.properties', 'w') as file:
        file.write(new_lines)


print("start")
#lambdaValues = np.linspace(0, 1, 21)
lambdaValues = [0]
applicantOptions = [40]
priceOptions = [5]

for lambdaVal in lambdaValues:
    for applicantOption in applicantOptions:
        for priceOption in priceOptions:
            set_settings(100, 100, lambdaVal, applicantOption, priceOption)
            subprocess.call("sh ./run_airbnb_optimization.sh", shell=True)

print("end")
