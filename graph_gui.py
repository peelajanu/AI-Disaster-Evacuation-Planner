import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import messagebox, filedialog
from algorithms import shortest_path
from map_data import map_manager
from traffic_data import simulate_traffic

class EvacuationPlannerGUI:
    def __init__(self, master):
        self.master = master
        self.G = None
        self.route = None
        self.obstacle_mode = False
        self.fig = None
        self.ax = None
        self.cid = None
        
        self.setup_ui()
        self.load_map()
        
    def setup_ui(self):
        self.master.title("AI Disaster Evacuation Route Planner")
        
        # Map location frame
        loc_frame = tk.LabelFrame(self.master, text="Map Location")
        loc_frame.pack(pady=5, padx=10, fill="x")
        
        tk.Label(loc_frame, text="Location:").grid(row=0, column=0)
        self.entry_location = tk.Entry(loc_frame, width=30)
        self.entry_location.grid(row=0, column=1, padx=5)
        self.entry_location.insert(0, "Banjara Hills, Hyderabad, India")
        
        tk.Button(loc_frame, text="Load Map", command=self.load_map).grid(row=0, column=2)
        
        # Coordinates frame
        coord_frame = tk.LabelFrame(self.master, text="Route Planning")
        coord_frame.pack(pady=5, padx=10, fill="x")
        
        tk.Label(coord_frame, text="Start X").grid(row=0, column=0)
        tk.Label(coord_frame, text="Start Y").grid(row=1, column=0)
        tk.Label(coord_frame, text="End X").grid(row=2, column=0)
        tk.Label(coord_frame, text="End Y").grid(row=3, column=0)
        
        self.entry_x1 = tk.Entry(coord_frame)
        self.entry_y1 = tk.Entry(coord_frame)
        self.entry_x2 = tk.Entry(coord_frame)
        self.entry_y2 = tk.Entry(coord_frame)
        
        self.entry_x1.grid(row=0, column=1)
        self.entry_y1.grid(row=1, column=1)
        self.entry_x2.grid(row=2, column=1)
        self.entry_y2.grid(row=3, column=1)
        
        # Algorithm selection
        tk.Label(coord_frame, text="Algorithm").grid(row=4, column=0)
        self.algo_var = tk.StringVar(value="dijkstra")
        tk.OptionMenu(coord_frame, self.algo_var, "dijkstra", "astar", "bfs").grid(row=4, column=1)
        
        # Buttons
        tk.Button(coord_frame, text="Find Route", command=self.calculate_route).grid(row=5, columnspan=2, pady=5)
        
        # Obstacle management frame
        obs_frame = tk.LabelFrame(self.master, text="Obstacle Management")
        obs_frame.pack(pady=5, padx=10, fill="x")
        
        tk.Label(obs_frame, text="Obstacle Severity (1-5)").grid(row=0, column=0)
        self.entry_severity = tk.Entry(obs_frame)
        self.entry_severity.grid(row=0, column=1)
        self.entry_severity.insert(0, "2.0")
        
        tk.Button(obs_frame, text="Add Obstacle at Click", command=self.toggle_obstacle_mode).grid(row=1, columnspan=2)
        tk.Button(obs_frame, text="Clear All Obstacles", command=self.clear_obstacles).grid(row=2, columnspan=2)
        
        # Scenario management
        scenario_frame = tk.LabelFrame(self.master, text="Scenario Management")
        scenario_frame.pack(pady=5, padx=10, fill="x")
        
        tk.Button(scenario_frame, text="Save Scenario", command=self.save_scenario).grid(row=0, column=0, padx=5)
        tk.Button(scenario_frame, text="Load Scenario", command=self.load_scenario).grid(row=0, column=1, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        tk.Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(fill="x")
        
    def load_map(self):
        location = self.entry_location.get()
        try:
            self.G = map_manager.load_real_world_map(location)
            self.status_var.set(f"Map loaded: {location}")
            self.draw_map()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {e}")
            self.status_var.set("Error loading map")
            
    def draw_map(self, route=None):
        if self.G is None:
            return
            
        plt.close('all')  # Close previous figures
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        
        # Get positions from node data
        pos = {node: (data['x'], data['y']) for node, data in self.G.nodes(data=True)}
        
        # Draw base graph
        nx.draw(self.G, pos, ax=self.ax, node_size=20, edge_color='gray', alpha=0.7)
        
        # Draw obstacles
        if map_manager.obstacles:
            nx.draw_networkx_nodes(self.G, pos, nodelist=list(map_manager.obstacles.keys()), 
                                 node_color='black', node_size=50, ax=self.ax)
        
        # Draw route if exists
        if route:
            path_edges = list(zip(route, route[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, 
                                  edge_color='red', width=2, ax=self.ax)
            nx.draw_networkx_nodes(self.G, pos, nodelist=route, 
                                 node_color='red', node_size=30, ax=self.ax)
            
            # Highlight start and end
            nx.draw_networkx_nodes(self.G, pos, nodelist=[route[0]], 
                                 node_color='green', node_size=100, ax=self.ax)
            nx.draw_networkx_nodes(self.G, pos, nodelist=[route[-1]], 
                                 node_color='orange', node_size=100, ax=self.ax)
        
        # Add legend
        handles = []
        if route:
            handles.append(plt.Line2D([0], [0], color='red', lw=2, label='Route'))
            handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Start'))
            handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, label='End'))
        if map_manager.obstacles:
            handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='Obstacle'))
        
        if handles:
            self.ax.legend(handles=handles, loc='upper right')
        
        plt.title("Disaster Evacuation Route Planner")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True)
        
        # Connect click event
        if self.cid:
            self.fig.canvas.mpl_disconnect(self.cid)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_map_click)
        
        plt.tight_layout()
        plt.show()
        
    def toggle_obstacle_mode(self):
        """Toggle obstacle mode on/off"""
        self.obstacle_mode = not self.obstacle_mode
        if self.obstacle_mode:
            self.status_var.set("Click on map to add ONE obstacle (click outside to cancel)")
        else:
            self.status_var.set("Ready")
        
    def on_map_click(self, event):
        if not self.obstacle_mode:
            return
            
        # Find nearest node to click
        click_x, click_y = event.xdata, event.ydata
        if click_x is None or click_y is None:  # Clicked outside axes
            self.toggle_obstacle_mode()  # Cancel mode
            return
            
        min_dist = float('inf')
        nearest = None
        for node, data in self.G.nodes(data=True):
            node_x, node_y = data['x'], data['y']
            dist = ((node_x - click_x) ** 2 + (node_y - click_y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                nearest = node
                
        if nearest:
            try:
                severity = float(self.entry_severity.get())
                if severity < 1 or severity > 5:
                    messagebox.showwarning("Warning", "Severity should be between 1 and 5")
                    return
                    
                map_manager.add_obstacle(nearest, severity)
                self.status_var.set(f"Added obstacle at node {nearest} with severity {severity}")
                self.draw_map(self.route)
            except ValueError:
                messagebox.showerror("Error", "Invalid severity value")
        
        # Always exit obstacle mode after one click
        self.toggle_obstacle_mode()
        
    def clear_obstacles(self):
        map_manager.clear_obstacles()
        self.status_var.set("All obstacles cleared")
        self.draw_map(self.route)
        
    def calculate_route(self):
        try:
            x1 = float(self.entry_x1.get())
            y1 = float(self.entry_y1.get())
            x2 = float(self.entry_x2.get())
            y2 = float(self.entry_y2.get())
            algo = self.algo_var.get()
            
            src_node = self.find_nearest_node(x1, y1)
            dst_node = self.find_nearest_node(x2, y2)
            
            if src_node == dst_node:
                messagebox.showinfo("Info", "Start and End locations are the same.")
                return
                
            self.route = shortest_path(self.G, src_node, dst_node, algo)
            
            if self.route:
                self.status_var.set(f"Route found with {len(self.route)} nodes using {algo}")
                self.draw_map(self.route)
            else:
                messagebox.showerror("Error", "No route found between the selected coordinates.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric coordinates.")
            
    def find_nearest_node(self, x, y):
        min_dist = float('inf')
        nearest = None
        for node, data in self.G.nodes(data=True):
            node_x, node_y = data['x'], data['y']
            dist = ((node_x - x) ** 2 + (node_y - y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                nearest = node
        return nearest
        
    def save_scenario(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", 
                                               filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                map_manager.save_scenario(filename)
                self.status_var.set(f"Scenario saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save scenario: {e}")
                
    def load_scenario(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                self.G = map_manager.load_scenario(filename)
                self.status_var.set(f"Scenario loaded from {filename}")
                self.draw_map()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load scenario: {e}")

def draw_route(graph, route=None):
    """Standalone function to draw route (for command-line use)"""
    plt.figure(figsize=(12, 8))
    pos = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}
    
    # Draw base graph
    nx.draw(graph, pos, node_size=20, edge_color='gray', alpha=0.7)
    
    # Draw route if provided
    if route:
        path_edges = list(zip(route, route[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, 
                              edge_color='red', width=2)
        nx.draw_networkx_nodes(graph, pos, nodelist=route,
                             node_color='red', node_size=30)
        
        # Highlight start and end
        nx.draw_networkx_nodes(graph, pos, nodelist=[route[0]],
                             node_color='green', node_size=100)
        nx.draw_networkx_nodes(graph, pos, nodelist=[route[-1]],
                             node_color='orange', node_size=100)
    
    plt.title("Evacuation Route")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

def find_nearest_node(graph, x, y):
    """Standalone nearest node finder"""
    min_dist = float('inf')
    nearest = None
    for node, data in graph.nodes(data=True):
        node_x, node_y = data['x'], data['y']
        dist = ((node_x - x) ** 2 + (node_y - y) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            nearest = node
    return nearest

def run_gui():
    """Run the full GUI application"""
    root = tk.Tk()
    app = EvacuationPlannerGUI(root)
    root.mainloop()