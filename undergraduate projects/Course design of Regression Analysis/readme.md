## 📘 Overview
This project was completed as part of the **Regression Analysis** course at the **School of Mathematics, South China University of Technology**.  
It explores the relationship between **smoking status**, **gender**, and **medical expenses** using regression techniques and hypothesis testing.  
The analysis aims to determine whether smoking and gender significantly influence medical charges and to quantify their effects through a linear regression model.

---

## 🧠 Background
Medical cost prediction plays an important role in health economics and insurance pricing.  
In this project, a dataset containing personal characteristics (age, sex, BMI, smoking status, and medical charges) was analyzed to understand how smoking behavior and gender impact healthcare costs.

---

## 🧮 Methodology
1. **Data Preprocessing**
   - Filtered data by gender and smoking status.
   - Removed outliers and handled missing values.
   - Defined four groups:  
     - Male Smokers  
     - Female Smokers  
     - Male Non-Smokers  
     - Female Non-Smokers  

2. **Model Construction**
   - Built a **Multiple Linear Regression Model** to estimate medical expenses.  
   - Regression model:  
     \[
     \text{charges} = \beta_0 + \beta_1 \cdot \text{age} + \beta_2 \cdot \text{bmi} + \beta_3 \cdot \text{sex} + \beta_4 \cdot \text{smoker} + \varepsilon
     \]
   - Applied **dummy variable encoding** for categorical features (sex, smoker).

3. **Hypothesis Testing**
   - Tested whether smokers have significantly higher charges than non-smokers.
   - Examined gender differences in average medical charges.
   - Performed **t-tests** and **F-tests** to validate regression coefficients.

4. **Model Evaluation**
   - Evaluated model fit using **R²**, **Adjusted R²**, and **RMSE**.
   - Conducted residual diagnostics to check for normality and homoscedasticity.

---

## 📊 Results and Analysis
- **Smoking status** has a strong, statistically significant positive effect on medical charges.  
- **Gender** alone does not significantly affect charges, but **interaction effects** may exist.  
- The regression model achieved an **R² above 0.7**, indicating good explanatory power.  
- Model diagnostics confirmed the validity of linear regression assumptions.

**Key Insight:**  
Smokers incur substantially higher medical costs, confirming the long-term financial burden of smoking on healthcare systems.

---

## 💻 Tools and Environment
- **Language:** R  
- **Libraries:** `dplyr`, `ggplot2`, `car`, `lmtest`  
- **Techniques:** Regression modeling, hypothesis testing, residual diagnostics, data visualization  

---

## 🧠 Skills Demonstrated
- Regression model development and interpretation  
- Statistical hypothesis testing  
- Exploratory data analysis and visualization  
- Use of R for applied data science and econometrics  

---
