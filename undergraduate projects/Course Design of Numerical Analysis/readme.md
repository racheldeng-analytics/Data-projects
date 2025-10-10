## 📘 Overview
This project focuses on the **numerical computation of initial value problems for ordinary differential equations (ODEs)** and their application to real-world modeling — specifically, simulating the **ascent process of a small single-stage rocket**.  
Through theoretical validation and numerical experiments, the report compares several numerical methods, including:
- Euler Method  
- Improved Euler Method  
- Trapezoidal Method  
- Runge–Kutta Method (4th order)

The project also builds a mathematical model of rocket ascent to analyze the relationships between **velocity, height, and acceleration over time**, providing insights into optimizing rocket design and fuel efficiency.

---

## 🧮 Contents
1. **Numerical Experiments:**  
   Validation and comparison of numerical methods for ODE initial value problems.  
   - Implementation of Euler, Improved Euler, Trapezoidal, and RK4 methods.  
   - Analysis of convergence order and stability.  

2. **Interpolation and Integration Tests:**  
   - Comparison of piecewise **Lagrange** and **Hermite** interpolation methods.  
   - Numerical integration using **composite trapezoidal formulas**.

3. **Application Example – Rocket Ascent Simulation:**  
   - Built a two-phase rocket motion model (with and without fuel).  
   - Analyzed effects of thrust, mass, and fuel burn rate on height and velocity.  
   - Implemented numerical solving and visualization in MATLAB.

---

## 🚀 Key Findings
- **Runge–Kutta (4th order)** shows the highest accuracy and stability among tested methods.  
- **Piecewise Hermite interpolation** achieves smaller error than **Lagrange interpolation**.  
- In the rocket model, increasing thrust or reducing mass significantly improves maximum height and velocity.  
- Excessive fuel mass increases duration but not necessarily efficiency.  

---

## 💻 Tools & Techniques
- **Programming Language:** MATLAB  
- **Numerical Methods:** Euler, Improved Euler, Trapezoidal, RK4  
- **Visualization:** MATLAB plotting and comparative graphs  
- **Mathematical Modeling:** Physics-based ODE modeling  

---

## 🧠 Skills Developed
- Numerical modeling and algorithm implementation  
- Differential equation solving using MATLAB  
- Scientific analysis and visualization  
- Research and technical writing in applied mathematics  

---
