# AI-Based Disaster Evacuation Route Planner 🗺️


An intelligent and adaptable route planning tool that leverages real-world geospatial data and artificial intelligence algorithms to generate optimal evacuation paths during natural and human-made disasters.
## ✨ Features

**Dynamic Route Planning:** Utilizes classical pathfinding algorithms like **Dijkstra's**, **A* (A-Star)**, and **Breadth-First Search (BFS)** to compute the shortest and safest paths
**Real-World Map Integration:** Automatically downloads real-world street network data from OpenStreetMap using the `OSMnx` library, modeling the road network as a complex graph.
**Dynamic Obstacle Simulation:** Users can interactively add obstacles on the map, and the algorithms will dynamically adjust route calculations to avoid these high-risk areas.
**Traffic Congestion Modeling:** The system can simulate traffic conditions, which inflates edge weights to represent congestion and helps in finding less crowded evacuation paths.
**Interactive GUI:** A user-friendly graphical interface built with `Tkinter` and `Matplotlib` allows users to select locations, input coordinates, visualize maps, and simulate emergency scenarios in real time
**Scenario Management:** The ability to save and load emergency scenarios in JSON format enables pre-planning and testing of various disaster situations without recalculation.

## ⚙️ Technologies Used

- **Python:** The core language for the application.
**`NetworkX`:** A powerful Python package for the creation, manipulation, and study of complex networks, used to model the road network.
**`OSMnx`:** A library to download and process real-world geospatial data from OpenStreetMap to create street network graphs.
**`Tkinter` & `Matplotlib`:** Used together to create the interactive GUI for visualization and user interaction.

## 🚀 Getting Started

### Prerequisites

You need Python 3.x installed. The project dependencies are listed in the `requirements.txt` file.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/ai-disaster-evacuation-planner.git](https://github.com/YOUR_USERNAME/ai-disaster-evacuation-planner.git)
    cd ai-disaster-evacuation-planner
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  **Run the application:**
    ```bash
    python start_gui.py
    ```
2.  **Using the GUI:**
    -   Enter a location (e.g., "Banjara Hills, Hyderabad, India") and click "Load Map" to download the street network.
    -   Input the coordinates of your start and end points.
    -   Select your preferred algorithm (Dijkstra, A\*, or BFS).
    -   Use the "Add Obstacle at Click" button to simulate blockages on the map.
    -   Click "Find Route" to visualize the optimal evacuation path.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🤝 Authors

-   Peela Tulasi Jahnavi

---
**Note:** This project serves as a proof of concept and a foundational step for building smart, adaptive disaster evacuation solutions.Future work could include live data integration, mobile application development, and predictive modeling.
