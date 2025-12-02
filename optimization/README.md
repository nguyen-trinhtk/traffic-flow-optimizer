# **Traffic Flow Optimization Using Linear Programming**

This project formulates and solves a traffic-flow optimization problem over a directed network.
Each path has a congestion threshold, and each road segment has a finite capacity.
The goal is to **maximize total usable traffic flow** while enforcing congestion and capacity limits.

---

## **Problem Set-Up**

A traffic network contains several alternative routes between an origin and destination.
Each directed road segment (edge) has a finite capacity, and each path has a congestion threshold indicating when traffic becomes inefficient.

Thus the core question becomes:

> **How can we maximize overall network throughput while preventing congestion and avoiding capacity violations?**

---

## **Graph Networks**

Traffic is modeled as a **directed graph**:

* **Nodes** = intersections
* **Edges** = directed road segments, each with a capacity
* **Paths** = sequences of edges from a source to a sink

All feasible paths (source → destination) are discovered using BFS.
These paths become the **decision variables** in the optimization model.

---

## **Translation into Mathematics**

We define:

* $m$ = number of edges
* $b_i$ = capacity of edge $i$
* $n$ = number of paths
* $x_j$ = flow rate on path $j$
* $c_k$ = congestion threshold for path $k$

### **Incidence Matrix**

Let

$$
A \in \mathbb{R}^{m \times n},
\qquad A_{ij} = 1 \text{ if path } j \text{ uses edge } i \text{, }
0 \text{ otherwise.}
$$

The load on edge $i$ is

$$
(Ax)_i
$$

### **Capacity Constraint**

$$
Ax \le b
$$

### **Utility Function (piecewise linear)**

Each path contributes utility

$$
y_k= min ( x_k, \frac{x_k + c_k}{2} )
$$

### **Network Optimization Problem**

$$
\max \sum_{k=1}^n y_k
\quad
\text{s.t.}
\quad
Ax \le b\quad
x \ge 0
$$

---

## **Standardizing the Linear Program**

To linearize the objective, introduce auxiliary variables $y_k$ representing utility for each path.

### **Decision Vector**

$$
z =
\begin{bmatrix}
x_1 \ ... \ x_n \quad y_1 \ ... \ y_n
\end{bmatrix}^T
\in \mathbb{R}^{2n}
$$

### **Objective Function**

$$
p =
\begin{bmatrix}
0 \ ... \ 0 \quad 1 \ ... \ 1
\end{bmatrix}
$$

$$
\max \quad p^T z
$$

---

### **Constraint 1 — Edge Capacities**

Extend $A$ with zeros to include $y$ variables:

$$
A_1 = \begin{bmatrix} A \quad 0_{m \times n} \end{bmatrix},
\qquad
b_1 = b
$$

$$
A_1 z \le b_1
$$

---

### **Constraint 2 — Linearizing $y_k \le x_k$**

$$
A_2 = \begin{bmatrix} -I_n \quad I_n \end{bmatrix},
\qquad
b_2 = 0
$$

$$
A_2 z \le b_2
$$

---

### **Constraint 3 — Linearizing $y_k \le 0.5x_k + 0.5c_k$**

$$
A_3 = \begin{bmatrix} -0.5 I_n \quad I_n \end{bmatrix},
\qquad
b_3 = 0.5c
$$

$$
A_3 z \le b_3
$$

---

### **Final LP Form**

$$
A_{\text{LP}}=
\begin{bmatrix}
A_1 \ A_2 \ A_3
\end{bmatrix},
\qquad
b_{\text{LP}}=
\begin{bmatrix}
b_1 \ b_2 \ b_3
\end{bmatrix}
$$

The final linear program is:

$$
\max \quad p^T z
\quad \text{s.t.} \quad
A_{\text{LP}} z \le b_{\text{LP}}, \quad
z \ge 0
$$

---

## **Solving**

The LP is currently solved using SciPy’s `linprog`.
Theoretically, this problem can be effectively solved using the **dual simplex** method by forming a dual tableau and executing appropriate Jordan exchanges.

---

## **Reference**

This formulation is inspired by **Exercise 102** from *Linear Programming Exercises* by Lieven Vandenberghe, UCLA, 2013–2014. It follows the standard structure of capacity-constrained, multi-path network flow optimization with convexified utility.
