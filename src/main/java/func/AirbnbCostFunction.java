package func;

import data.Vector;
import util.ApplicantPool;

/**
 * @author: Gumbee
 */
public class AirbnbCostFunction implements CostFunction<Vector> {

    // reference to the applicant pool so we can get data about the applicant by his/her id
    @Override
    public String getLabel() {
        return "Airbnb Global Cost Function";
    }

    @Override
    public double calcCost(Vector planData) {
        double price = planData.getValue(0);

        return 0;
    }
}
