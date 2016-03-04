/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package experiments;


import agents.EPOSAgent;
import agents.energyPlan.Plan;
import agents.fitnessFunction.FitnessFunction;
import agents.fitnessFunction.MinProductSumFitnessFunction;
import dsutil.generic.RankPriority;
import dsutil.generic.state.ArithmeticListState;
import dsutil.generic.state.ArithmeticState;
import dsutil.protopeer.services.topology.trees.DescriptorType;
import dsutil.protopeer.services.topology.trees.TreeProvider;
import dsutil.protopeer.services.topology.trees.TreeType;
import java.io.File;
import java.io.FileFilter;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.NoSuchElementException;
import java.util.Scanner;
import org.joda.time.DateTime;
import protopeer.Experiment;
import protopeer.Peer;
import protopeer.PeerFactory;
import protopeer.SimulatedExperiment;
import protopeer.servers.bootstrap.SimplePeerIdentifierGenerator;
import protopeer.util.quantities.Time;
import tree.centralized.client.TreeClient;
import tree.centralized.server.TreeServer;

/**
 *
 * @author Evangelos
 */
public class EPOS_PNW extends SimulatedExperiment{
    
    private final static String expSeqNum="01";
    private static String experimentID="Experiment "+expSeqNum+"/";
    
    //Simulation Parameters
    private final static int runDuration=25;
    private final static int N=496;
    
    // Tree building
    private static final RankPriority priority=RankPriority.HIGH_RANK;
    private static final DescriptorType descriptor=DescriptorType.RANK;
    private static final TreeType type=TreeType.SORTED_HtL;
    private final static int[] v=new int[]{4};
    // EPOS Agent
    private static int treeInstances=1;
    private static String plansLocation="input-data";
    private static String planConfigurations="8.5";
    private static String TISLocation="input-data/TISs/TIS-GENERATION-FAILURE.txt";
    static File dir = new File(plansLocation+"/"+planConfigurations);  
    private static String treeStamp="2BR"; //1. average k-ary tree, 2. Balanced or random k-ary tree, 3. random positioning or nodes 
    private static File[] agentMeterIDs = dir.listFiles(new FileFilter() {  
        public boolean accept(File pathname) {  
            return pathname.isDirectory();  
        }  
    });
    private static DateTime aggregationPhase=DateTime.parse("2014-07-23");
    private static String plansFormat=".plans";
    private static FitnessFunction fitnessFunction=new MinProductSumFitnessFunction();
    private static int planSize=144;
    private static DateTime historicAggregationPhase=DateTime.parse("0001-01-01");
    private static Plan patternEnergyPlan;
    private static int historySize=5;
    
    public static void main(String[] args) {
        for(int i=0;i<treeInstances;i++){
            treeStamp="3BR"+i;
            System.out.println("Experiment "+expSeqNum+"\n");
            Experiment.initEnvironment();
            final EPOS_PNW test = new EPOS_PNW();
            test.init();
            experimentID="Experiment "+i+"/";
            final File folder = new File("peersLog/"+experimentID);
            clearExperimentFile(folder);
            folder.mkdir();
//            patternEnergyPlan=getPatternPlan(planSize);
            patternEnergyPlan=loadTIS(TISLocation);
            PeerFactory peerFactory=new PeerFactory() {
                public Peer createPeer(int peerIndex, Experiment experiment) {
                    Peer newPeer = new Peer(peerIndex);
                    if (peerIndex == 0) {
                       newPeer.addPeerlet(new TreeServer(N, priority, descriptor, type));
                    }
                    newPeer.addPeerlet(new TreeClient(Experiment.getSingleton().getAddressToBindTo(0), new SimplePeerIdentifierGenerator(), peerIndex, 4)); //v[(int)(Math.random()*v.length)]
                    newPeer.addPeerlet(new TreeProvider());
                    newPeer.addPeerlet(new EPOSAgent(experimentID, plansLocation, planConfigurations, treeStamp, agentMeterIDs[peerIndex].getName(), plansFormat, fitnessFunction, planSize, aggregationPhase, historicAggregationPhase, patternEnergyPlan, historySize)); 
                    return newPeer;
                }
            };
            test.initPeers(0,N,peerFactory);
            test.startPeers(0,N);
            //run the simulation
            test.runSimulation(Time.inSeconds(runDuration));
        }
        
    }
    
    public final static Plan loadTIS(String TISLocation){
        Plan patternEnergyPlan= new Plan();
        File file = new File(TISLocation);
        try {
            Scanner sc = new Scanner(file);
            while (sc.hasNextLine()) {
                patternEnergyPlan.addArithmeticState(new ArithmeticState(sc.nextDouble()));
            }
            sc.close();
        } 
        catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        catch(NoSuchElementException e){
            e.printStackTrace();
        }
        return patternEnergyPlan;
    }
    
    
    public final static ArithmeticListState getPatternPlan(int planSize){
        ArithmeticListState patternEnergyPlan=new ArithmeticListState(new ArrayList());
        for(int i=0;i<planSize;i++){
            if((i>=40 && i<=59)){
                patternEnergyPlan.addArithmeticState(new ArithmeticState(-0.035));
            }
            else{
                patternEnergyPlan.addArithmeticState(new ArithmeticState(0.0137));
            }
            
        }
        return patternEnergyPlan;
    }
    
    public final static void clearExperimentFile(File experiment){
        File[] files = experiment.listFiles();
        if(files!=null) { //some JVMs return null for empty dirs
            for(File f: files) {
                if(f.isDirectory()) {
                    clearExperimentFile(f);
                } else {
                    f.delete();
                }
            }
        }
        experiment.delete();
    }
}
