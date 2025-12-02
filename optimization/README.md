# **Traffic Flow Optimization Using Linear Programming**

This project formulates and solves a traffic-flow optimization problem on a directed network. Each path has a congestion threshold, and each road segment has a finite capacity. The objective is to maximize total usable traffic flow while respecting congestion and capacity constraints.

---

## **Problem Set-Up**

In general, a traffic network has multiple alternative paths to travel between an origin and destination.
Each directed road segment has a capacity representing the maximum flow it can support, and each path has a congestion threshold indicating when flow becomes inefficient.

Hence, a central question is established:

> **How can we maximize total traffic through the network while controlling congestion and preventing capacity violations?**

---

## **Graph Networks**

Traffic is represented using a **directed graph**:

* **Nodes:** intersections
* **Edges:** directed road segments, each with a capacity
* **Paths:** sequences of edges from a source to a sink

All feasible (source → sink) paths are discovered using BFS/DFS. These paths become the decision variables in the optimization model.

---

## **Translation into Mathematics**

The model uses the following notation:

* **Edges:**

  * ( m ) total
  * Capacities: ( b_i )

* **Paths:**

  * ( n ) total
  * Flow variables: ( x_j )
  * Congestion thresholds: ( c_k )

### **Incidence Matrix**

Let
[
A \in \mathbb{R}^{m \times n}, \qquad
A_{ij} =
\begin{cases}
1 & \text{if path } j \text{ uses edge } i \
0 & \text{otherwise}
\end{cases}
]

Then the total load on edge ( i ) is:
[
(Ax)_i
]

### **Capacity Constraint**

[
Ax \le b
]

### **Utility Function (piecewise linear)**

For each path:
[
f_k(x_k) =
\begin{cases}
x_k, & x_k \le c_k \
\frac{x_k + c_k}{2}, & x_k > c_k
\end{cases}
]

### **Network Optimization Problem**

[
\max \sum_{k=1}^n f_k(x_k)
\quad \text{s.t.} \quad
Ax \le b,;
x \ge 0
]

---

## **Standardizing the Linear Program**

To convert the piecewise objective into a linear program, we introduce auxiliary variables ( y_k ) representing the utility value.

### **Decision Vector**

[
z =
\begin{bmatrix}
x_1 \ \vdots \ x_n \ y_1 \ \vdots \ y_n
\end{bmatrix}
\in \mathbb{R}^{2n}
]

### **Objective (maximize total utility)**

[
p =
\begin{bmatrix}
0 \ \vdots \ 0 \ 1 \ \vdots \ 1
\end{bmatrix}
]

[
\max\ p^T z
]

---

### **Constraint 1 — Edge Capacities**

[
A_1 = [A ;; 0_{m \times n}], \qquad b_1 = b
]

[
A_1 z \le b_1
]

---

### **Constraint 2 — Linearizing ( y_k \le x_k )**

[
A_2 = [-I_n ;; I_n], \qquad b_2 = 0
]

[
A_2 z \le b_2
]

---

### **Constraint 3 — Linearizing ( y_k \le 0.5x_k + 0.5c_k )**

[
A_3 = [-0.5 I_n ;; I_n], \qquad b_3 = 0.5c
]

[
A_3 z \le b_3
]

---

### **Final LP Form**

[
A_{\text{LP}} =
\begin{bmatrix}
A_1 \ A_2 \ A_3
\end{bmatrix},
\qquad
b_{\text{LP}} =
\begin{bmatrix}
b_1 \ b_2 \ b_3
\end{bmatrix}
]

[
\max p^T z
\quad \text{s.t.} \quad
A_{\text{LP}} z \le b_{\text{LP}},;
z \ge 0
]

---

## **Solving**

The LP is solved using SciPy’s `linprog` solver (simplex or interior point).
A future extension is a custom implementation of the **dual simplex method** for specialized networks or performance tuning.

---

## **Reference**

The optimization framework is inspired by Exercise 102 from *Linear Programming Exercises* by Lieven Vandenberghe, Electrical Engineering Department, University of California, Los Angeles (2013–2014). The formulation follows the classical structure of capacity-constrained multi-path network flow problems with convexified utility.

