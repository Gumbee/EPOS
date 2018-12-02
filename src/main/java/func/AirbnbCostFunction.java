package func;

import config.AirbnbConfiguration;
import config.Configuration;
import data.Vector;

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
        Vector matchingValue = GetVectorSection(value, 0, Configuration.numApplicants);
        Vector priceValue = GetVectorSection(value, Configuration.numApplicants, Configuration.numApplicants+Configuration.numAgents);
        Vector occupancyValue = GetVectorSection(value, Configuration.numApplicants+Configuration.numAgents, Configuration.numApplicants+Configuration.numAgents*2);

        Vector matchingGoal = GetVectorSection(goalSignal, 0, Configuration.numApplicants);
        Vector priceGoal = GetVectorSection(goalSignal, Configuration.numApplicants, Configuration.numApplicants+Configuration.numAgents);
        Vector occupancyGoal = GetVectorSection(goalSignal, Configuration.numApplicants+Configuration.numAgents, Configuration.numApplicants+Configuration.numAgents*2);

        return 20*calcCostRMSE(matchingValue, matchingGoal) + calcCostRMSE(priceValue, priceGoal) + 4*calcCostRMSE(occupancyValue, occupancyGoal);
    }

    @Override
    public Vector calcGradient(Vector value) {
        int numTotalDimensions = value.getNumDimensions();

        Vector matchingValue = GetVectorSection(value, 0, Configuration.numApplicants);
        Vector priceValue = GetVectorSection(value, Configuration.numApplicants, Configuration.numApplicants+Configuration.numAgents);
        Vector occupancyValue = GetVectorSection(value, Configuration.numApplicants+Configuration.numAgents, Configuration.numApplicants+Configuration.numAgents*2);

        Vector matchingGoal = GetVectorSection(goalSignal, 0, Configuration.numApplicants);
        Vector priceGoal = GetVectorSection(goalSignal, Configuration.numApplicants, Configuration.numApplicants+Configuration.numAgents);
        Vector occupancyGoal = GetVectorSection(goalSignal, Configuration.numApplicants+Configuration.numAgents, Configuration.numApplicants+Configuration.numAgents*2);

        Vector matchingGradient = ExtendVectorSection(calcGradientRMSE(matchingValue, matchingGoal), numTotalDimensions, 0);
        Vector priceGradient = ExtendVectorSection(calcGradientRMSE(priceValue, priceGoal), numTotalDimensions, Configuration.numApplicants);
        Vector occupancyGradient = ExtendVectorSection(calcGradientRMSE(occupancyValue, occupancyGoal), numTotalDimensions, Configuration.numApplicants+Configuration.numAgents);

        Vector totalGradient = matchingGradient.cloneThis();
        totalGradient.add(priceGradient);
        totalGradient.add(occupancyGradient);

        return totalGradient;
    }

    public double calcCostRMSE(Vector value, Vector goal) {
        double goalMean = goal.avg();
        double goalStd = goal.std();
        double otherMean = value.avg();
        double otherStd = value.std();

        Vector goalReplica = goal.cloneThis();
        goalReplica.subtract(goalMean);

        double multiplicativeFactor = otherStd / (goalStd + 1e-10);
        goalReplica.multiply(multiplicativeFactor);
        goalReplica.add(otherMean);
        return goalReplica.rootMeanSquareError(value);
    }

    public Vector calcGradientRMSE(Vector value, Vector goal) {
        double length = value.getNumDimensions();

        double inverse = 1 / calcCostRMSE(value, goal);
        Vector difference = value.cloneThis();
        difference.subtract(goal);

        difference.multiply(inverse * length);

        return difference;
    }

    private Vector GetVectorSection(Vector value, int start, int end){

        Vector returnVector = new Vector(end-start);

        for(int i=start;i<end;i++){
            returnVector.setValue(i-start, value.getValue(i));
        }

        return returnVector;
    }

    private Vector ExtendVectorSection(Vector value, int totalSize, int offset){

        Vector returnVector = new Vector(totalSize);

        for(int i=0;i<totalSize;i++){
            if(i >= offset && i < offset+value.getNumDimensions()) {
                returnVector.setValue(i, value.getValue(i-offset));
            }else{
                returnVector.setValue(i, 0);
            }
        }

        return returnVector;
    }
}
