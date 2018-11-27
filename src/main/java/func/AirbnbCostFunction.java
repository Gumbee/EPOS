package func;

import config.AirbnbConfiguration;
import config.Configuration;
import data.Vector;
import util.ApplicantPool;

import java.util.logging.Level;

/**
 * @author: Gumbee
 */
public class AirbnbCostFunction implements DifferentiableCostFunction<Vector>, HasGoal {

    public static Vector goalSignal = null;

    // reference to the applicant pool so we can get data about the applicant by his/her id
    @Override
    public String getLabel() {
        return "Airbnb-Global";
    }

    /**
     * This method calculates the goal signal based on which the cost finction is calculated.
     */
    @Override
    public void populateGoalSignal() {
        AirbnbCostFunction.goalSignal = Configuration.goalSignalSupplier.get();
    }

    @Override
    public double calcCost(Vector value) {
        Vector goalSignal = AirbnbCostFunction.goalSignal.cloneThis();
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

    @Override
    public Vector calcGradient(Vector value) {
        AirbnbCostResult result = rootMeanSquareError(value, goalSignal.cloneThis());

        double length = AirbnbConfiguration.numApplicants;
        double inverse = 1 / result.matchingCost;
        Vector differenceMatching = value.cloneThis();
        ZeroOutVector(differenceMatching, 0, AirbnbConfiguration.numApplicants);
        differenceMatching.subtract(ZeroOutVector(AirbnbCostFunction.goalSignal.cloneThis(), 0, AirbnbConfiguration.numApplicants));
        differenceMatching.multiply(inverse * length);


        length = AirbnbConfiguration.numAgents;
        inverse = 1 / result.priceCost;
        Vector differencePrice = value.cloneThis();
        ZeroOutVector(differencePrice, AirbnbConfiguration.numApplicants, AirbnbConfiguration.numApplicants+AirbnbConfiguration.numAgents);
        differencePrice.subtract(ZeroOutVector(AirbnbCostFunction.goalSignal.cloneThis(), AirbnbConfiguration.numApplicants, AirbnbConfiguration.numApplicants+AirbnbConfiguration.numAgents));
        differencePrice.multiply(inverse * length);


        length = AirbnbConfiguration.numAgents;
        inverse = 1 / result.occupancyCost;
        Vector differenceOccupancy = value.cloneThis();
        ZeroOutVector(differenceOccupancy, AirbnbConfiguration.numApplicants+AirbnbConfiguration.numAgents, AirbnbConfiguration.numApplicants+AirbnbConfiguration.numAgents*2);
        differenceOccupancy.subtract(ZeroOutVector(AirbnbCostFunction.goalSignal.cloneThis(), AirbnbConfiguration.numApplicants+AirbnbConfiguration.numAgents, AirbnbConfiguration.numApplicants+AirbnbConfiguration.numAgents*2));
        differenceOccupancy.multiply(inverse * length);

        differenceMatching.add(differencePrice);
        differenceMatching.add(differenceOccupancy);
        return differenceMatching;
    }

    public Vector ZeroOutVector(Vector value, int start, int end){

        for(int i=0;i<value.getNumDimensions();i++){
            if(i < start || i >= end){
                value.setValue(i, 0);
            }
        }

        return value;
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
