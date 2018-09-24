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
package func;

import data.Plan;
import data.DataType;

/**
 * A function that assigns a cost value to any given data instance.
 * 
 * @author Peter
 * @param <V> the type of the data this cost function should handle
 */
public abstract class CostFunction<V extends DataType<V>> implements PlanCostFunction<V> {

    public abstract double calcCost(V value);

    @Override
    public final double calcCost(Plan<V> plan) {
        return calcCost(plan.getValue());
    }
}
