# Traffic Flow Optimizer

### Description

**Traffic Flow Optimizer** is a Python-based framework designed to automate the **optimization of urban traffic flow**. The system integrates three major components:

* **Perception** – Detects and tracks vehicles from video data.
* **Flow Prediction** – Computes real-time traffic flow metrics and predicts future trends using machine learning models.
* **Flow Optimization** – Determines optimal traffic signal timings to minimize congestion and improve throughput.

A visual overview of the data and process pipeline illustrates how these components interact.

### Repository Structure
```
.
├── dataset
├── optimization
│   ├── linear-program/
│   └── mdp/
├── perception
│   ├── model/
│   ├── results/
│   └── src
│       ├── utils/ 
│       └── main.py
├── prediction
│   ├── results
│   │   ├── analysis/ 
│   │   └── dataframe/ 
│   └── src
│       ├── lstm/ 
│       ├── random_forest/
│       ├── utils/ 
│       └── main.py
├── utils/
├── README.md
└── requirements.txt
```
Further details about each functional module are described below.

### Functional Overview

#### 1. Perception
The perception part handles the following tasks: 
* Trains **YOLOv8** model for vehicle detection.
* Tracks detected objects using **DeepSort**.
* Iterates through `.mp4` videos in `dataset/vid` (local only, not committed).
* Exports frame-by-frame detection and tracking results to `perception/results` in the following JSON structure:

```
{
    "vid_id": "vid_id",
    "detections": [
        [
            {
                "TRACK_ID": [X_1, Y_1, X_2, Y_2]
            },
            ...
        ],
        ...
    ]
}
```

#### 2. Flow Prediction

* Processes each JSON file in `perception/results` to compute traffic metrics: **average speed**, **density**, and **flow**.
* Uses these features to train a **Random Forest** regression model for traffic flow prediction.
* Evaluates performance using standard metrics such as **MAE** and **RMSE**.

Currently, I'm trying to integrate **LSTM** networks for improved temporal modeling and long-term prediction accuracy. This also requires a richer and more diverse dataset for better accuracy.

#### 3. Signal Timing Optimization
The optimization part of this project includs:
* Simulate traffic networks with graphs.
* * Determine known metrics and constraints specific to each edges and nodes.
* Formulates graph-based **Linear Programming (LP)** problems to solve for approriate timing at each intersection (node).

The current implementation is more of a theoretical context-specific solution to the optimization problem. For a more generalized approach, I'm planning on incorporating realistic simulations via **SuMO**, then develop **MDP-RL** based on such simulations for an adaptive, real-time traffic signal control.
