# Big Data Course Design: Ridge Regression Analysis

## 📘 Overview
This project was developed as part of the **Big Data Applications** course at the **School of Mathematics, South China University of Technology**.  
It focuses on reproducing and applying the mathematical theory and numerical experiments from Hoerl and Kennard’s seminal 1970 paper on **Ridge Regression: Biased Estimation for Nonorthogonal Problems**.

The goal of this project is to understand the theoretical foundation of ridge regression, reproduce its mathematical proofs, and apply it to a real-world dataset for predictive modeling.

---

## 🧠 Background
**Ridge Regression** is a regularized regression technique designed to handle **multicollinearity** in data.  
Unlike ordinary least squares (OLS), ridge regression introduces a penalty term to shrink regression coefficients and stabilize estimates when predictors are highly correlated.

**Key points:**
- Addresses instability in OLS estimates under multicollinearity  
- Introduces a regularization parameter (**λ**) to control coefficient shrinkage  
- Achieves a bias-variance trade-off for improved prediction accuracy  
- Commonly used in bioinformatics, finance, and NLP  

---

## 🧮 Theoretical Components
This report reproduces and explores several core mathematical results from Hoerl and Kennard’s original work:

1. Properties of Best Linear Unbiased Estimators (BLUE)  
2. Derivation of Ridge Estimators  
3. Ridge Trace Analysis  
4. Mean Squared Error (MSE) Behavior  
5. General Form of Ridge Regression  
6. Selection of the Optimal Regularization Parameter  

Each section includes formula derivations and discussions on estimator bias, covariance, and eigenvalue sensitivity.

---

## 🧑‍💻 Application Example
The practical implementation uses the **Wisconsin Breast Cancer Biopsy dataset** (699 samples, 9 features).  
The analysis was conducted in **R**, including the following steps:

### 1. Data Preprocessing
- Loaded and cleaned the dataset  
- Renamed variables and handled missing values  
- Split data into training (70%) and testing (30%) sets  

### 2. Model Building
- Built a **Multiple Linear Regression model** using `lm()`  
- Checked **Variance Inflation Factor (VIF)** using `car::vif()` to detect multicollinearity  
- Applied **Ridge Regression** using `glmnet()` with `alpha = 0`  

### 3. Evaluation
- Tracked iteration metrics (λ values, %Dev explained, degrees of freedom)  
- Visualized coefficient shrinkage paths  
- Computed misclassification error and accuracy  
- Evaluated performance with **ROC curve** and **AUC score**

**Result:**  
The ridge regression achieved an **AUC ≈ 1** and a **misclassification rate of ~4.4%**, showing excellent performance.

---

## 📊 Key Findings
- Ridge regression effectively mitigated multicollinearity issues.  
- The optimal λ (~0.05) balanced bias and variance.  
- Model accuracy and AUC indicated strong classification capability.  
- Ridge regression improved prediction stability over OLS.  

---

## 🧾 Code and Tools
**Language:** R  

**Libraries Used:**
- `MASS`
- `glmnet`
- `car`
- `pROC`
- `openxlsx`

**Core Functions:**
`lm()`, `vif()`, `glmnet()`, `predict()`, `roc()`, and custom `misClassError()`.

---
