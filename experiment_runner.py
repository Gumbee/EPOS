import subprocess

def set_settings(numAgents, numApplicants, lambdaValue, applicantOptions):
    with open('conf/epos.properties', 'r+') as file:
        lines = file.readlines()
        new_lines = ""

        for line in lines:
            if "numAgents=" in line:
                new_lines += "numAgents=" + str(numAgents)
            elif "numApplicants=" in line:
                new_lines += "numApplicants=" + str(numApplicants)
            elif "weightsString=" in line:
                new_lines += "weightsString=" + '"0.0,"' + str(lambdaValue)
            elif "applicantOptions=" in line:
                new_lines += "applicantOptions=" + str(applicantOptions)
            else:
                new_lines += line.replace("\n", "")

            new_lines += "\n"

        file.seek(0)
        file.truncate()
        file.write(new_lines)


print("start")
lambdaValues = [0.0, 0.2, 0.5, 1.0]
applicantOptions = [7, 30]

for lambdaVal in lambdaValues:
    for applicantOption in applicantOptions:
        set_settings(200, 200, lambdaVal, applicantOption)
        subprocess.call("sh ./run_airbnb_optimization.sh", shell=True)

print("end")