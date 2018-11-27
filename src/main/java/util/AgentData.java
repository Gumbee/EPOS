import java.util.ArrayList;

/**
 * @author: maxbortone
 */
public class AgentData {
    // The coordinates of the agent
    public double latitude;
    public double longitude;
    // Optimal price decided by the agent
    public double optimalPrice;
    // Maximal allowed occupancy decided by the agent
    public int optimalOccupancy;
    // Preferred applicant type decided by the agent
    public double optimalType;
    // Ranking of applicant type decided by the agent
    public ArrayList<Double> typeRanking;
}