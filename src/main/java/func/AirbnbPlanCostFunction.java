package func;

import java.util.Date;

import config.Configuration;
import data.Plan;
import data.Vector;
import config.AirbnbConfiguration;
import config.AirbnbLocalParameters;
import util.AgentPool;
import util.ApplicantPool;
import util.AgentData;

/**
 * Implments the local cost function
 * 
 * @author: maxbortone
 */
public class AirbnbPlanCostFunction implements PlanCostFunction<Vector> {

    private int id;

    /**
     * Calculate the local cost function for a given plan
     * 
     * @param plan: vector representation of the plan
     * @return local cost associated with the plan
     */
    @Override
    public double calcCost(Plan<Vector> plan) {
        this.id = plan.getAgentId();
        Vector planData = plan.getValue().cloneThis();
        int agentId = plan.getAgentId();
        AgentData agentData = AgentPool.agentPool.getAgent(agentId); 
        double priceCost = calcPriceCost(planData, agentData, agentId);
        double occupancyCost = calcOccupancyCost(planData, agentData, agentId);
        double typeCost = calcTypeCost(planData, agentData, agentId);
        double planCost = AirbnbLocalParameters.priceFactor*priceCost + AirbnbLocalParameters.occupancyFactor*occupancyCost
                         + AirbnbLocalParameters.typeFactor*typeCost;
        return planCost;
    }

    public String getLabel() {
        return "Airbnb-Local";
    }

    /**
     * Calculate the local cost due to the price resource
     * of the plan
     * 
     * @param plan: vector representation of the plan
     * @param data: agent data containing optimal values
     * @param id: id of the agent
     * @return local cost associated with the plan due to price resource
     */
    private double calcPriceCost(Vector plan, AgentData data, int id) {
        double diff = plan.getValue(Configuration.numApplicants+id)-data.optimalPrice;
        double priceCost = Math.sqrt(Math.pow(diff, 2.0));
        return priceCost;
    }

    /**
     * Calculate the local cost due to the occupancy resource
     * of the plan
     * 
     * @param plan: vector representation of the plan
     * @param data: agent data containing optimal values
     * @param id: id of the agent
     * @return local cost associated with the plan due to occupancy resource
     */
    private double calcOccupancyCost(Vector plan, AgentData data, int id) {
        int offset = Configuration.numApplicants+Configuration.numAgents;
        double diff = plan.getValue(offset+id)-data.optimalOccupancy;
        double occupancyCost = Math.sqrt(Math.pow(diff, 2.0));
        return occupancyCost;
    }

    /**
     * Calculate the local cost due to the type resource
     * of the plan
     * 
     * @param plan: vector representation of the plan
     * @param data: agent data containing optimal values
     * @param id: id of the agent
     * @return local cost associated with the plan due to type resource
     */
    private double calcTypeCost(Vector plan, AgentData data, int id) {
        double diff = getApplicantRank(plan, data)-data.optimalType;
        double typeCost = Math.sqrt(Math.pow(diff, 2.0));
        return typeCost;
    }

    /**
     * Get the rank associated with the applicant
     * selcted by the plan
     * 
     * @param plan: vector representation of the plan
     * @param data: agent data containing optimal values
     * @return rank of the applicant
     */
    private double getApplicantRank(Vector plan, AgentData data) {
        int applicantId = 0;

        while (applicantId < plan.getNumDimensions() && Math.abs(plan.getValue(applicantId)-0.0) < 1E-7) {
            ++applicantId;
        }

        if(applicantId == plan.getNumDimensions()){
            return 0;
        }

        int typeId = ApplicantPool.getTypeId(applicantId);
        double rank = data.typeRanking.get(typeId);
        return rank;
    }
}