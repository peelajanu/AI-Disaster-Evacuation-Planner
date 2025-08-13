import random

def simulate_traffic(graph):
    print("Simulating traffic conditions...")

    for u, v, k, data in graph.edges(keys=True, data=True):
        # Simulate traffic factor between 1.0 and 3.0
        traffic_factor = random.uniform(1.0, 3.0)
        original_weight = data.get('weight', 1.0)
        new_weight = original_weight * traffic_factor
        data['weight'] = new_weight
        print(f"Edge ({u}, {v}, {k}): weight changed from {original_weight:.2f} to {new_weight:.2f}")

    return graph
