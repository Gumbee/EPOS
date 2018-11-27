package func;

import config.AirbnbConfiguration;
import config.Configuration;
import data.Vector;
import util.ApplicantPool;

/**
 * @author: Gumbee
 */
public class AirbnbCostFunction implements CostFunction<Vector>, HasGoal {

    // reference to the applicant pool so we can get data about the applicant by his/her id
    @Override
    public String getLabel() {
        return "Airbnb Global Cost Function";
    }

    /**
     * This method calculates the goal signal based on which the cost finction is calculated.
     */
    @Override
    public void populateGoalSignal() {
        RMSECostFunction.goalSignal = Configuration.goalSignalSupplier.get();
        RMSECostFunction.goalMean = RMSECostFunction.goalSignal.avg();
        RMSECostFunction.goalStd = RMSECostFunction.goalSignal.std();
    }

    @Override
    public double calcCost(Vector value) {
        Vector goalSignal = RMSECostFunction.goalSignal.cloneThis();
        return rootMeanSquareError(value, goalSignal).sum();
    }

    /**
     * Returns the cost of the matching, the price and the occupancy of our model.
     *
     * @param a the accumulated global response
     * @param b the goal signal
     * @return the cost
     */
    private AirbnbCostResult rootMeanSquareError(Vector a, Vector b) {
        double[] vectorX = a.getValues();
        double[] vectorY = b.getValues();

        int numApplicants = AirbnbConfiguration.numApplicants;
        int numAgents = AirbnbConfiguration.numAgents;

        AirbnbCostResult result = new AirbnbCostResult();

        for (int i = 0; i < numApplicants; i++) {
            result.matchingCost += Math.pow(vectorX[i] - vectorY[i], 2);
        }

        for (int i = numApplicants; i < numApplicants+numAgents; i++) {
            result.priceCost += Math.pow(vectorX[i] - vectorY[i], 2);
        }

        for (int i = numApplicants+numAgents; i < numApplicants+numAgents*2; i++) {
            result.occupancyCost += Math.pow(vectorX[i] - vectorY[i], 2);
        }

        result.matchingCost = result.matchingCost / numApplicants;
        result.priceCost = result.priceCost / numAgents;
        result.occupancyCost = result.occupancyCost / numAgents;

        result.matchingCost = Math.sqrt(result.matchingCost);
        result.priceCost = Math.sqrt(result.priceCost);
        result.occupancyCost = Math.sqrt(result.occupancyCost);

        return result;
    }

    /**
     * A class which combines the different costs of our AirbnbCostFunction into one data package
     */
    private class AirbnbCostResult {
        public double matchingCost;
        public double priceCost;
        public double occupancyCost;

        public double sum(){
            return matchingCost;
        }
    }
}
