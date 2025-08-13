import osmnx as ox
import os
import networkx as nx
import random
from typing import Optional, Dict, Tuple, List

class MapManager:
    def __init__(self):
        self.obstacles = {}
        self.original_graph = None
        self.current_graph = None
        
    def load_real_world_map(self, location: str, distance: int = 2000) -> nx.MultiGraph:
        """Load real-world map from OpenStreetMap"""
        try:
            print(f"🌍 Downloading map for {location} (radius: {distance}m)")
            self.original_graph = ox.graph_from_address(location, dist=distance, network_type='drive')
            self.current_graph = self.original_graph.copy()
            
            # Ensure all edges have weight attributes
            for u, v, k, data in self.current_graph.edges(keys=True, data=True):
                if 'length' not in data:
                    data['length'] = 1.0  # fallback
                data['weight'] = data['length']  # initial weight = length
                
            return self.current_graph
        except Exception as e:
            print(f"Error loading map: {e}")
            return self.get_fallback_graph()
            
    def get_fallback_graph(self) -> nx.MultiGraph:
        """Fallback to a complete graph with 10 nodes"""
        print("⚠️ Using fallback graph")
        G = nx.MultiGraph()
        
        # Add 10 nodes with random positions
        for i in range(1, 11):
            G.add_node(i, x=random.uniform(0, 10), y=random.uniform(0, 10))
        
        # Add edges between all nodes with random weights
        for u in G.nodes():
            for v in G.nodes():
                if u != v:
                    G.add_edge(u, v, weight=round(random.uniform(1.0, 5.0), 2))
        
        self.original_graph = G.copy()
        self.current_graph = G
        return G
        
    def add_obstacle(self, node_id: int, severity: float = 2.0):
        """Add obstacle by marking node and significantly increasing edge weights"""
        if node_id not in self.current_graph:
            raise ValueError(f"Node {node_id} not in graph")
            
        # Mark node as obstacle
        self.current_graph.nodes[node_id]['obstacle'] = True
        self.obstacles[node_id] = severity
        
        # Dramatically increase weight of all edges connected to this node
        for neighbor in nx.neighbors(self.current_graph, node_id):
            for k in self.current_graph[node_id][neighbor]:
                original_weight = self.original_graph[node_id][neighbor][k].get('weight', 1.0)
                # Large multiplier to ensure avoidance
                self.current_graph[node_id][neighbor][k]['weight'] = original_weight * 100 * severity
                
    def clear_obstacles(self):
        """Reset all obstacles and restore original weights"""
        self.current_graph = self.original_graph.copy()
        self.obstacles = {}
        print("All obstacles cleared - weights restored to original values")
        
    def save_scenario(self, filename: str):
        """Save current scenario (graph + obstacles)"""
        data = {
            'graph': nx.node_link_data(self.original_graph),
            'obstacles': self.obstacles
        }
        import json
        with open(filename, 'w') as f:
            json.dump(data, f)
        print(f"Scenario saved to {filename}")
            
    def load_scenario(self, filename: str) -> nx.MultiGraph:
        """Load saved scenario and reapply obstacles"""
        import json
        with open(filename) as f:
            data = json.load(f)
            
        self.original_graph = nx.node_link_graph(data['graph'])
        self.obstacles = data.get('obstacles', {})
        self.current_graph = self.original_graph.copy()
        
        # Reapply obstacles with their original severity
        for node_id, severity in self.obstacles.items():
            self.add_obstacle(node_id, severity)
            
        print(f"Scenario loaded from {filename} with {len(self.obstacles)} obstacles")
        return self.current_graph

# Singleton instance for easy access
map_manager = MapManager()

def get_graph(location: Optional[str] = None) -> nx.MultiGraph:
    """Get graph for location or fallback graph if no location specified"""
    if location:
        return map_manager.load_real_world_map(location)
    return map_manager.get_fallback_graph()