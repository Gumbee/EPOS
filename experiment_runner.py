import subprocess
import numpy as np

def set_settings(numAgents, numApplicants, lambdaValue, applicantOptions):
    with open('conf/epos.properties', 'r+') as file:
        lines = file.readlines()
        new_lines = ""

        for line in lines:
            spaceless_line = line.replace(" ", "")
            if "#" in spaceless_line:
                new_lines += line.replace("\n", "")
            if "numAgents=" in spaceless_line:
                new_lines += "numAgents=" + str(numAgents)
            elif "numApplicants=" in spaceless_line:
                new_lines += "numApplicants=" + str(numApplicants)
            elif "weightsString=" in spaceless_line:
                new_lines += "weightsString=" + '"0.0,"' + str(lambdaValue)
            elif "applicantOptions=" in spaceless_line:
                new_lines += "applicantOptions=" + str(applicantOptions)
            else:
                new_lines += spaceless_line.replace("\n", "")

            new_lines += "\n"

        file.seek(0)
        file.truncate()
        file.write(new_lines)


print("start")
lambdaValues = np.linspace(0, 1, 20)
applicantOptions = [10]

for lambdaVal in lambdaValues:
    for applicantOption in applicantOptions:
        set_settings(100, 100, lambdaVal, applicantOption)
        subprocess.call("sh ./run_airbnb_optimization.sh", shell=True)

print("end")