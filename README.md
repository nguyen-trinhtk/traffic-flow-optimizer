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

* Trains **YOLOv8** models for vehicle detection.
* Tracks detected objects using **DeepSort**.
* Iterates through `.mp4` videos in `dataset/vid` (local only, not committed).
* Exports detection and tracking results to `perception/results` in the following JSON structure:

```json
{
    "vid_id": "vid_id",
    "detections": [
        [
            {
                "TRACK_ID": [X_1, Y_1, X_2, Y_2] // Object bounding box coordinates
            },
            ... // Additional objects
        ],
        ... // Additional frames
    ]
}
```

#### 2. Flow Prediction

* Processes each JSON file in `perception/results` to compute traffic metrics: **average speed**, **density**, and **flow**.
* Uses these features to train a **Random Forest** regression model for traffic flow prediction.
* Evaluates performance using standard metrics such as **MAE** and **RMSE**.
* *In development:* Integration of **LSTM** networks for improved temporal modeling and long-term prediction accuracy.

#### 3. Signal Optimization

* **Current implementation:** Formulates graph-based **Linear Programming (LP)** problems to identify optimal traffic signal timings that maximize flow under predefined constraints.
* *In development:* Incorporate realistic simulations via **SUMO** and develop **MDP/RL-based** approaches for adaptive, real-time traffic signal control.
