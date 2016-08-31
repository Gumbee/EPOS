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
package experiments.log;

import agents.Agent;
import agents.fitnessFunction.costFunction.CostFunction;
import agents.plan.GlobalPlan;
import agents.plan.Plan;
import edu.uci.ics.jung.algorithms.layout.Layout;
import edu.uci.ics.jung.algorithms.layout.RadialTreeLayout;
import edu.uci.ics.jung.graph.DelegateForest;
import edu.uci.ics.jung.graph.Forest;
import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.util.Context;
import edu.uci.ics.jung.visualization.DefaultVisualizationModel;
import edu.uci.ics.jung.visualization.VisualizationModel;
import edu.uci.ics.jung.visualization.VisualizationViewer;
import edu.uci.ics.jung.visualization.control.DefaultModalGraphMouse;
import edu.uci.ics.jung.visualization.control.ModalGraphMouse;
import edu.uci.ics.jung.visualization.decorators.DirectionalEdgeArrowTransformer;
import edu.uci.ics.jung.visualization.decorators.EdgeShape;
import edu.uci.ics.jung.visualization.util.VertexShapeFactory;
import experiments.output.ImageFile;
import experiments.output.PngFile;
import experiments.output.SvgFile;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Menu;
import java.awt.MenuBar;
import java.awt.MenuItem;
import java.awt.Paint;
import java.awt.Shape;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.geom.AffineTransform;
import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.filechooser.FileFilter;
import org.apache.commons.collections15.Transformer;
import protopeer.Finger;
import protopeer.measurement.MeasurementLog;
import protopeer.network.NetworkAddress;

/**
 *
 * @author Peter
 */
public class GraphLogger extends AgentLogger {

    private final CostFunction costFunction;
    private final Map<Finger, Integer> selectedPlanIdxPerAgent = new HashMap<>();

    private final Dimension size = new Dimension(512, 512);
    private Forest<Node, Integer> graph;
    private int numIterations;
    private int curIteration;
    private Map<TreeNode, float[]> values;

    private final double vertexSize127 = 2;
    private final double vertexSize255 = 1;
    private final double vertexSize511 = 1;
    private final double vertexSize1023 = 1;
    private double vertexSize = vertexSize127;
    private VertexShapeFactory<Node> shapeFactory = new VertexShapeFactory<Node>();
    private AffineTransform shapeTransform = null;

    public GraphLogger(CostFunction costFunction) {
        this.costFunction = costFunction;
    }

    @Override
    public void init(int agentId) {
        selectedPlanIdxPerAgent.clear();
    }

    @Override
    public void initRoot(Plan costSignal) {
    }

    @Override
    public void log(MeasurementLog log, int epoch, Agent agent) {
        Plan costSignal = new GlobalPlan(agent);

        int prevIdx = selectedPlanIdxPerAgent.getOrDefault(agent.getPeer().getFinger(), -1);
        int idx = agent.getSelectedPlanIdx();
        selectedPlanIdxPerAgent.put(agent.getPeer().getFinger(), idx);

        TreeNode node = new TreeNode(agent.experimentId, agent.getPeer().getFinger(), agent.getChildren());
        double cost = costFunction.calcCost(agent.getSelectedPlan(), costSignal, idx, agent.getPossiblePlans().size(), idx != prevIdx);

        log.log(epoch, agent.getIteration(), node, cost);
    }

    @Override
    public void logRoot(MeasurementLog log, int epoch, Agent agent, Plan global) {
    }

    @Override
    public void print(MeasurementLog log) {
        int numAgents = log.getTagsOfType(TreeNode.class).size();
        if (numAgents <= 127) {
            vertexSize = vertexSize127;
        } else if (numAgents <= 255) {
            vertexSize = vertexSize255;
        } else if (numAgents <= 511) {
            vertexSize = vertexSize511;
        } else if (numAgents <= 1023) {
            vertexSize = vertexSize1023;
        } else {
            vertexSize = vertexSize1023;
        }
        shapeTransform = AffineTransform.getScaleInstance(vertexSize, vertexSize);

        graph = new DelegateForest<>();
        numIterations = log.getMaxEpochNumber();

        Map<NetworkAddress, Node> idx2Node = new HashMap<>();
        values = new HashMap<>();

        float[] minValues = new float[numIterations];
        float[] maxValues = new float[numIterations];
        for(int i = 0; i < numIterations; i++) {
            minValues[i] = 1;
        }
        for (Object agentObj : log.getTagsOfType(TreeNode.class)) {
            TreeNode agent = (TreeNode) agentObj;
            if (agent.expId != 0) {
                continue;
            }

            Node node = new Node();
            node.agent = agent;

            idx2Node.put(agent.id.getNetworkAddress(), node);
            graph.addVertex(node);

            float[] agentValues = new float[numIterations];
            for (int i = 0; i < numIterations; i++) {
                double localError = log.getAggregate(i, agent).getAverage();
                if (Double.isNaN(localError)) {
                    numIterations = i;
                    break;
                }
                agentValues[i] = 1.0f - (float) localError;
                minValues[i] = Math.min(minValues[i],agentValues[i]);
                maxValues[i] = Math.max(maxValues[i],agentValues[i]);
            }

            values.put(agent, agentValues);
        }
        for (Map.Entry<TreeNode, float[]> entry : values.entrySet()) {
            float[] agentValues = entry.getValue();
            for (int i = 0; i < numIterations; i++) {
                agentValues[i] = (agentValues[i]-minValues[i]+0.00001f) / (maxValues[i]-minValues[i]+0.00001f);
            }
        }

        int edge = 0;
        for (Node node : graph.getVertices()) {
            for (Finger f : node.agent.children) {
                Node child = idx2Node.get(f.getNetworkAddress());
                graph.addEdge(edge++, node, child);
            }
        }

        showGraph();
    }

    private VisualizationViewer<Node, Integer> visualize(VisualizationModel<Node, Integer> model) {
        VisualizationViewer<Node, Integer> viewer = new VisualizationViewer<>(model);
        viewer.setPreferredSize(new Dimension(size.width, size.height + 26));
        viewer.setBackground(Color.white);
        viewer.getRenderContext().setEdgeShapeTransformer(getEdgeShapeTransformer());
        viewer.getRenderContext().setEdgeArrowTransformer(getEdgeArrowTransformer());
        viewer.getRenderContext().setVertexFillPaintTransformer(getVertexFillPaintTransformer());
        viewer.getRenderContext().setVertexShapeTransformer(getVertexShapeTransformer());
        //viewer.getRenderContext().getMultiLayerTransformer().getTransformer(Layer.LAYOUT).(, vertexSize, pd);
        viewer.setGraphMouse(getGraphMouse());
        return viewer;
    }

    private void initIteration(int iteration) {
        for (Node n : graph.getVertices()) {
            n.val = values.get(n.agent)[iteration];
        }
    }

    private <V, E> Layout<V, E> getLayout(Forest<V, E> graph) {
        Layout<V, E> layout = new RadialTreeLayout<>(graph);
        layout.setSize(size);
        return layout;
    }

    private <V, E> Transformer<Context<Graph<V, E>, E>, Shape> getEdgeShapeTransformer() {
        return new EdgeShape.Line();
    }

    private <V, E> Transformer<Context<Graph<V, E>, E>, Shape> getEdgeArrowTransformer() {
        return new DirectionalEdgeArrowTransformer<>(0, 0, 0);
    }

    private Transformer<Node, Paint> getVertexFillPaintTransformer() {
        return (Node vertex) -> {
            return new Color(vertex.val, vertex.val, vertex.val);
        };
    }

    private Transformer<Node, Shape> getVertexShapeTransformer() {
        return (Node vertex) -> {
            Shape shape = shapeFactory.getEllipse(vertex);
            shape = shapeTransform.createTransformedShape(shape);
            return shape;
        };
    }

    private VisualizationViewer.GraphMouse getGraphMouse() {
        DefaultModalGraphMouse graphMouse = new DefaultModalGraphMouse();
        graphMouse.setMode(ModalGraphMouse.Mode.TRANSFORMING);
        return graphMouse;
    }

    public void showGraph() {
        JFrame frame = new JFrame("IEPOS");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        curIteration = 0;
        initIteration(curIteration);
        frame.setTitle("IEPOS - iteration " + (curIteration + 1));
        VisualizationModel<Node, Integer> model = new DefaultVisualizationModel(getLayout(graph));
        VisualizationViewer<Node, Integer> viewer = visualize(model);

        KeyListener keyListener = new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
                boolean refresh = false;

                if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
                    if (curIteration < numIterations - 1) {
                        curIteration++;
                        refresh = true;
                    }
                } else if (e.getKeyCode() == KeyEvent.VK_LEFT) {
                    if (curIteration > 0) {
                        curIteration--;
                        refresh = true;
                    }
                }
                frame.setTitle("IEPOS - iteration " + (curIteration + 1));

                if (refresh) {
                    initIteration(curIteration);
                    model.setGraphLayout(model.getGraphLayout());
                    //model.setGraphLayout(getLayout((Forest<Node, Integer>) tree));
                    viewer.invalidate();
                    viewer.validate();
                }
            }
        };

        viewer.addKeyListener(keyListener);
        frame.getContentPane().add(viewer);
        frame.pack();
        frame.setVisible(true);

        frame.setMenuBar(new MenuBar());
        Menu menu = new Menu("File");
        MenuItem saveas = new MenuItem("Save As...");
        saveas.addActionListener((ActionEvent e) -> {
            JFileChooser fileChooser = new JFileChooser();
            fileChooser.addChoosableFileFilter(new FileFilter() {
                @Override
                public boolean accept(File f) {
                    return f.getName().endsWith(".png");
                }

                @Override
                public String getDescription() {
                    return ".png files";
                }
            });
            fileChooser.addChoosableFileFilter(new FileFilter() {
                @Override
                public boolean accept(File f) {
                    return f.getName().endsWith(".svg");
                }

                @Override
                public String getDescription() {
                    return ".svg files";
                }
            });
            int returnVal = fileChooser.showSaveDialog(frame);
            if (returnVal == JFileChooser.APPROVE_OPTION) {
                File file = fileChooser.getSelectedFile();

                ImageFile img = null;
                if (file.getName().endsWith(".png")) {
                    img = new PngFile(file, viewer.getWidth(), viewer.getHeight());
                } else if (file.getName().endsWith(".svg")) {
                    img = new SvgFile(file, viewer.getWidth(), viewer.getHeight());
                }

                viewer.setDoubleBuffered(false);
                viewer.getRootPane().paintComponents(img.createGraphics());
                viewer.setDoubleBuffered(true);

                img.write();
            }
        });
        menu.add(saveas);
        frame.getMenuBar().add(menu);
    }

    private static class Node {

        public TreeNode agent;
        public float val;

        @Override
        public int hashCode() {
            int hash = 3;
            return hash;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (obj == null) {
                return false;
            }
            if (getClass() != obj.getClass()) {
                return false;
            }
            final Node other = (Node) obj;
            if (!Objects.equals(this.agent, other.agent)) {
                return false;
            }
            return true;
        }

    }

    private class TreeNode {

        public final int expId;
        public final Finger id;
        public final List<Finger> children;

        public TreeNode(int expId, Finger id, List<Finger> children) {
            this.expId = expId;
            this.id = id;
            this.children = children;
        }

        @Override
        public int hashCode() {
            int hash = 7;
            hash = 97 * hash + this.expId;
            hash = 97 * hash + Objects.hashCode(this.id);
            return hash;
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) {
                return true;
            }
            if (obj == null) {
                return false;
            }
            if (getClass() != obj.getClass()) {
                return false;
            }
            final TreeNode other = (TreeNode) obj;
            if (this.expId != other.expId) {
                return false;
            }
            if (!Objects.equals(this.id, other.id)) {
                return false;
            }
            if (!Objects.equals(this.children, other.children)) {
                return false;
            }
            return true;
        }
    }
}
