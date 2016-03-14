/*
 * Copyright (C) 2016 Evangelos Pournaras
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */
package agents.fitnessFunction;

import agents.Agent;
import agents.energyPlan.AggregatePlan;
import agents.energyPlan.Plan;
import agents.AgentPlans;
import java.util.List;

/**
 * minimize variance (submodular/convex compared to std deviation)
 * @author Peter
 */
public class IterativeMinVariance1 extends FitnessFunction {

    @Override
    public double getRobustness(Plan plan, Plan costSignal, AgentPlans historic) {
        return plan.variance();
    }

    @Override
    public int select(Agent agent, Plan aggregatePlan, List<Plan> combinationalPlans, Plan pattern) {
        double minVariance = Double.MAX_VALUE;
        int selected = -1;

        for (int i = 0; i < combinationalPlans.size(); i++) {
            Plan combinationalPlan = combinationalPlans.get(i);
            Plan testAggregatePlan = new AggregatePlan(agent);
            testAggregatePlan.add(aggregatePlan);
            testAggregatePlan.add(combinationalPlan);

            double variance = testAggregatePlan.variance();
            if (variance < minVariance) {
                minVariance = variance;
                selected = i;
            }
        }

        return selected;
    }

    @Override
    public int select(Agent agent, Plan childAggregatePlan, List<Plan> combinationalPlans, Plan pattern, AgentPlans historic, AgentPlans previous) {
        Plan modifiedChildAggregatePlan = new AggregatePlan(agent);
        if(previous != null) {
            modifiedChildAggregatePlan.set(previous.globalPlan);
            modifiedChildAggregatePlan.subtract(previous.aggregatePlan);
            modifiedChildAggregatePlan.multiply(0.001);
            modifiedChildAggregatePlan.add(childAggregatePlan);
        } else {
            modifiedChildAggregatePlan.set(childAggregatePlan);
        }
        return select(agent, modifiedChildAggregatePlan, combinationalPlans, pattern);
    }

}