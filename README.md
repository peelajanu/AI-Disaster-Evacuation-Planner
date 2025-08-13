# AI-Based Disaster Evacuation Route Planner 🗺️


An intelligent and adaptable route planning tool that leverages real-world geospatial data and artificial intelligence algorithms to generate optimal evacuation paths during natural and human-made disasters. [cite_start]This project was developed as a submission for the Artificial Intelligence course (CSE 455 & CSE 455L) at SRM University-AP[cite: 3].

## ✨ Features

- [cite_start]**Dynamic Route Planning:** Utilizes classical pathfinding algorithms like **Dijkstra's**, **A* (A-Star)**, and **Breadth-First Search (BFS)** to compute the shortest and safest paths[cite: 21, 52, 53, 54].
- [cite_start]**Real-World Map Integration:** Automatically downloads real-world street network data from OpenStreetMap using the `OSMnx` library, modeling the road network as a complex graph[cite: 21, 48].
- [cite_start]**Dynamic Obstacle Simulation:** Users can interactively add obstacles on the map, and the algorithms will dynamically adjust route calculations to avoid these high-risk areas[cite: 22, 24].
- [cite_start]**Traffic Congestion Modeling:** The system can simulate traffic conditions, which inflates edge weights to represent congestion and helps in finding less crowded evacuation paths[cite: 22, 24].
- [cite_start]**Interactive GUI:** A user-friendly graphical interface built with `Tkinter` and `Matplotlib` allows users to select locations, input coordinates, visualize maps, and simulate emergency scenarios in real time[cite: 23, 50].
- [cite_start]**Scenario Management:** The ability to save and load emergency scenarios in JSON format enables pre-planning and testing of various disaster situations without recalculation[cite: 24, 151].

## ⚙️ Technologies Used

- **Python:** The core language for the application.
- [cite_start]**`NetworkX`:** A powerful Python package for the creation, manipulation, and study of complex networks, used to model the road network[cite: 46].
- [cite_start]**`OSMnx`:** A library to download and process real-world geospatial data from OpenStreetMap to create street network graphs[cite: 48].
- [cite_start]**`Tkinter` & `Matplotlib`:** Used together to create the interactive GUI for visualization and user interaction[cite: 23, 50].

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
    -   [cite_start]Enter a location (e.g., "Banjara Hills, Hyderabad, India") and click "Load Map" to download the street network[cite: 63, 114].
    -   [cite_start]Input the coordinates of your start and end points[cite: 64].
    -   [cite_start]Select your preferred algorithm (Dijkstra, A\*, or BFS)[cite: 65].
    -   [cite_start]Use the "Add Obstacle at Click" button to simulate blockages on the map[cite: 66, 108].
    -   [cite_start]Click "Find Route" to visualize the optimal evacuation path[cite: 110].

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🤝 Authors

-   [cite_start]SRI HASITHA - `GAP22110010075` [cite: 7]
-   [cite_start]VAISHNAVI K - `AP2211001010125` [cite: 7]
-   [cite_start]MOUNI SRIN - `AP22110010129` [cite: 8]
-   [cite_start]JAHNAVI P - `AP22110010382` [cite: 10]

---
**Note:** This project serves as a proof of concept and a foundational step for building smart, adaptive disaster evacuation solutions. [cite_start]Future work could include live data integration, mobile application development, and predictive modeling[cite: 158, 163].