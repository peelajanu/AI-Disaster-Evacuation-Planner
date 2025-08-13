import networkx as nx

def dijkstra_path(graph, source, target):
    try:
        # Use modified weights that account for obstacles
        modified_weights = {(u, v, k): data.get('weight', 1.0) * 
                          (10 if graph.nodes[u].get('obstacle') or graph.nodes[v].get('obstacle') else 1)
                          for u, v, k, data in graph.edges(keys=True, data=True)}
        
        path = nx.shortest_path(graph, source, target, weight=lambda u, v, d: modified_weights[(u, v, d.get('key', 0))])
        length = nx.shortest_path_length(graph, source, target, weight=lambda u, v, d: modified_weights[(u, v, d.get('key', 0))])
        return path, length
    except nx.NetworkXNoPath:
        print("No path found using Dijkstra.")
        return None, None

def astar_path(graph, source, target):
    try:
        # Heuristic function that ignores obstacles for estimation
        def heuristic(u, v):
            if 'x' in graph.nodes[u] and 'y' in graph.nodes[u] and 'x' in graph.nodes[v] and 'y' in graph.nodes[v]:
                return ((graph.nodes[u]['x'] - graph.nodes[v]['x'])**2 + 
                        (graph.nodes[u]['y'] - graph.nodes[v]['y'])**2)**0.5
            return 0
            
        # Use modified weights
        modified_weights = {(u, v, k): data.get('weight', 1.0) * 
                          (10 if graph.nodes[u].get('obstacle') or graph.nodes[v].get('obstacle') else 1)
                          for u, v, k, data in graph.edges(keys=True, data=True)}
        
        path = nx.astar_path(graph, source, target, 
                            weight=lambda u, v, d: modified_weights[(u, v, d.get('key', 0))],
                            heuristic=heuristic)
        length = nx.astar_path_length(graph, source, target, 
                                    weight=lambda u, v, d: modified_weights[(u, v, d.get('key', 0))],
                                    heuristic=heuristic)
        return path, length
    except nx.NetworkXNoPath:
        print("No path found using A*.")
        return None, None

def shortest_path(graph, source, target, algo='dijkstra'):
    if algo == 'dijkstra':
        return dijkstra_path(graph, source, target)[0]
    elif algo == 'astar':
        return astar_path(graph, source, target)[0]
    elif algo == 'bfs':
        return nx.shortest_path(graph, source, target, method='bfs')
    else:
        raise ValueError("Unsupported algorithm")