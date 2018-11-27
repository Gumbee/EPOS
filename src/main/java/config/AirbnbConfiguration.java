package config;

import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 * @author: Gumbee
 */
public class AirbnbConfiguration {

    public static Date currentDate = new GregorianCalendar(2018, Calendar.NOVEMBER, 27).getTime();
    public static int numApplicants = 400;
    public static int numAgents = 400;

    public enum ApplicantType {
        SINGLE, COUPLE, FAMILY, GROUP, BUSINESS
    }

}
