package util;

import java.util.ArrayList;
import java.util.Random;
import data.Vector;
import config.AirbnbConfiguration.ApplicantType;

/**
 * @author: Gumbee
 */
public class ApplicantPool {

    private static class ApplicantData {
        // unique identifier (on EPOS simulation granularity)
        public int id;
        // the amount of people which belong to this applicant (one applicant can represent a group of people)
        public int groupSize;
        // the tourist type of this applicant
        public ApplicantType type;
    }

    // the applicant pool containing our applicant information
    private static ArrayList<ApplicantData> pool;
    // define a debugSeed so we can get rid of the randomness while debugging
    private static int debugSeed = 52812;

    /**
     * Generates a new random applicant pool of the given size
     *
     * @param size: the amount of applicants we should generate
     */
    public static void generateApplicantPool(int size){
        // create a new pool
        pool = new ArrayList<>();
        // create a RNG with a given seed so we can easily debug if something goes wrong
        Random random = new Random(debugSeed);

        // generate N new applicants
        for(int i=0;i<size;i++){
            ApplicantData applicant = new ApplicantData();
            // set the id
            applicant.id = i;
            // generate a group size which is uniform between 0 and 9
            applicant.groupSize = random.nextInt(10);
            // generate a random applicant type
            int randomTypeIndex = random.nextInt(ApplicantType.values().length);
            applicant.type = ApplicantType.values()[randomTypeIndex];
            // add the generated applicant to the pool
            pool.add(applicant);
        }
    }

    /**
     * Returns a vector which has 0 in all entries except the entry which corresponds to the applicant's type
     *
     * @param applicantId the applicant's id
     * @return a vector of 0s and one 1
     */
    public static Vector getTypeSimilarity(int applicantId){
        // get the applicant from the pool
        ApplicantData applicant = pool.get(applicantId);
        // create the vector of type similarities
        Vector similarities = new Vector(ApplicantType.values().length);

        for (ApplicantType applicantType : ApplicantType.values()) {
            // make sure we only set a 1 at the position which corresponds to the applicant's type
            similarities.add(applicantType == applicant.type ? 1f : 0f);
        }

        return similarities;
    }

    /**
     * Returns the group size of the given applicant
     *
     * @param applicantId the applicant's id
     * @return the size of the group
     */
    public static int getGroupSize(int applicantId){
        // get the applicant from the pool
        ApplicantData applicant = pool.get(applicantId);

        return applicant.groupSize;
    }

    /**
     * Returns the type id of the given applicant
     *
     * @param applicantId the applicant's id
     * @return the id of the type
     */
    public static int getTypeId(int applicantId){
        // get the applicant from the pool
        ApplicantData applicant = pool.get(applicantId);

        int typeId = 0;
        for (ApplicantType applicantType : ApplicantType.values()) {
            if (applicantType != applicant.type) {
                ++typeId;
            } else {
                break;
            }
        }
        return typeId;
    }
}
