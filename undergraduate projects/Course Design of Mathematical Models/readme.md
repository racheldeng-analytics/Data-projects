# 🧬 Stability Analysis and Visualization of a Two-Species Competition Model

## 📘 Overview
This project analyzes and visualizes the **stability of a two-species competition model** using **differential equations** and **Matlab App Designer**.  
The goal is to explore how two species compete for limited resources, determine the conditions for coexistence or extinction, and visualize population dynamics under varying parameters.  
The project applies **mathematical modeling**, **stability theory**, and **numerical simulation** to provide theoretical support for ecological and environmental protection.

---

## ⚙️ Model Description

### 🧩 Model Assumptions
1. Two populations, *x(t)* and *y(t)*, follow the **Logistic growth law** when living independently.  
2. Each population negatively affects the other's growth rate in proportion to its population size.  
3. The model assumes a **shared food source** and limited environmental capacity.

### 📈 Mathematical Model
The model is based on the following system of differential equations:

\[
\begin{cases}
\frac{dx}{dt} = r_1x(1 - \frac{x + \alpha y}{N_1}) \\
\frac{dy}{dt} = r_2y(1 - \frac{y + \beta x}{N_2})
\end{cases}
\]

where  
- \( x(t), y(t) \): population sizes of species X and Y  
- \( r_1, r_2 \): intrinsic growth rates  
- \( N_1, N_2 \): carrying capacities  
- \( \alpha, \beta \): competition coefficients  

### 🧮 Stability Analysis
- Linearized the nonlinear system and analyzed equilibrium points.  
- Identified four equilibrium states:  
  1. Both species extinct  
  2. Species X dominates  
  3. Species Y dominates  
  4. Coexistence equilibrium  

Stability was determined using **eigenvalue analysis** and **Jacobian matrix** methods.  
Different parameter configurations lead to outcomes such as extinction, dominance, or coexistence.

---

## 💻 Visualization Design

The visualization was implemented in **Matlab App Designer** and consists of:
- **Login interface** – includes entry, exit, and information display functions.  
- **Visualization interface** – allows users to:
  - Adjust model parameters interactively  
  - Plot real-time population trends  
  - Save or clear results  
  - Exit the program  

### 🖼️ Example Output
The app dynamically displays how population trajectories change under different growth rates and carrying capacities.  
Users can simulate:
- Faster growth rate of one species → quicker dominance  
- Higher carrying capacity → slower stabilization  
- Different initial populations → altered convergence speed  

---

## 🔍 Key Findings
- Growth rate, carrying capacity, and initial conditions affect **stabilization speed**, but not the qualitative outcome.  
- **Competition coefficients** fundamentally determine whether species coexist or one dominates.  
- The model effectively predicts coexistence or extinction, offering potential applications in **ecological management** and **market competition modeling**.

---

## 🧠 Learnings & Insights
This project enhanced my understanding of:
- Nonlinear differential equation modeling  
- Stability and equilibrium point analysis  
- Practical use of **Matlab App Designer** for visualization  
- The connection between **theoretical models** and **real-world ecological systems**

---

## 🛠️ Tools & Technologies
- **Language:** Matlab  
- **Framework:** App Designer  
- **Core Methods:** Numerical simulation, linearization, eigenvalue analysis  
- **Visualization:** Interactive parameter control and trend plotting  

---
