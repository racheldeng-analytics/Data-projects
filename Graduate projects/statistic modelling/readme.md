# Statistic Modelling assignment 1

## Salary Analysis Using Linear Regression in R

### 📘 Overview
This project analyzes how **experience** and **education level** influence **salary** using statistical methods and regression modeling in R. It was completed as part of the **MDA9159 course (Fall 2025)** under the guidance of Dr. Guowen Huang.

### 🎯 Objectives
- Compute and visualize salary distributions.
- Examine the relationship between salary, experience, and education.
- Build and interpret regression models.
- Perform hypothesis testing and interval estimation.

### 🧩 Methods
- **Data Source**: `p130.txt` (salary dataset with experience, education, and management level)
- **Tools Used**: R, ggplot2
- **Analytical Steps**:
  1. Descriptive statistics (mean, standard deviation)
  2. Grouped mean salary by education level
  3. Scatterplots of salary vs. experience by education and management
  4. Simple linear regression: `Salary ~ Experience`
  5. Multiple regression including education as a factor
  6. ANOVA to test significance of education
  7. Confidence and prediction intervals for salary estimation

### 📊 Key Findings
- **Positive correlation** between salary and experience.
- Higher education levels lead to higher average salaries.
- Model including education (`Salary ~ Experience + Education`) explains **~41%** of salary variation.
- Education has a statistically significant impact on salary (p < 0.01).

### 🧠 Statistical Concepts Used
- Linear Regression (`lm()`)
- ANOVA for model comparison
- Confidence vs. Prediction intervals
- Dummy variable encoding for categorical predictors

### 🛠️ Technologies
- R Programming
- ggplot2
- Data visualization and regression analysis

### 📈 Sample Visualization
Scatterplots and regression lines showing salary trends by experience and education.

---
