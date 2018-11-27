package util;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Locale;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

import config.AirbnbConfiguration.*;

/**
 * Implments the pool of agents that are optimized by I-EPOS
 * at a given time
 * 
 * @author: maxbortone
 */
public class AgentPool {

    public static AgentPool agentPool = new AgentPool();

    private String agentDatasetDir;

    // the agent pool containing our agent information
    private ArrayList<AgentData> pool;
    // define a debugSeed so we can get rid of the randomness while debugging
    private int debugSeed = 52812;

    /**
     * Generates a new random agent pool of the given size
     *
     * @param size: the amount of agents we should generate
     */
    public void generateAgentPool(int size){
        // parse agent data file and populate pool
        File file = new File(agentDatasetDir + File.separator + "adentData.info");
        try (Scanner scanner = new Scanner(file)) {
            scanner.useLocale(Locale.ENGLISH);

            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                AgentData agentData = parseAgent(line);
                pool.add(agentData);
            }
        } catch (FileNotFoundException ex) {
            Logger.getLogger(AgentPool.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Get agent with a given index from the pool
     *
     * @param index: integer value representing the index of the agent
     * @return the agent data
     */
    public AgentData getAgent(int index){
        AgentData agentData = agentPool.pool.get(index);
        return agentData;
    }

    /**
     * Parse the agent data from the agent's data file of the form:
     * <code>
     *      "latitude,longitude,optimalPrice,optimalOccupancy,optimalType,[type1Rank,...,typeNRank];
     *       ...
     *       latitude,longitude,optimalPrice,optimalOccupancy,optimalType,[type1Rank,...,typeNRank];"
     * </code> 
     *
     * @param agentStr the string representation of the agent data
     * @return the agent data represented by the given string
     */
    private AgentData parseAgent(String agentStr) {
        AgentData agentData = new AgentData();
        Scanner scanner = new Scanner(agentStr);
        scanner.useLocale(Locale.US);
        scanner.useDelimiter(",");

        agentData.latitude = scanner.nextDouble();
        agentData.longitude = scanner.nextDouble();
        agentData.optimalPrice = scanner.nextDouble();
        agentData.optimalOccupancy = scanner.nextInt();
        agentData.optimalType = scanner.nextDouble();
        for (int i=0; i<ApplicantType.values().length; ++i) {
            double rank = scanner.nextDouble();
            agentData.typeRanking.add(rank);
        }

        return agentData;
    }
}
