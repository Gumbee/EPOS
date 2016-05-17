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
package experiments.parameters;

/**
 *
 * @author Peter
 */
public class PosIntParam implements Param<Integer> {

    @Override
    public boolean isValid(String param) {
        try {
            Integer.parseUnsignedInt(param);
            return true;
        } catch(NumberFormatException e) {
            return false;
        }
    }

    @Override
    public String validDescription() {
        return "any positive integer";
    }

    @Override
    public Integer get(String param) {
        return Integer.parseUnsignedInt(param);
    }
    
}