import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler, PowerTransformer
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt

# 1. 读取并整理原始数据
df_raw = pd.read_csv(r'C:\College\毕业\毕业设计\model sm.csv', encoding='gbk')
year_cols = [c for c in df_raw.columns if c.endswith('年') and c[:4].isdigit()]

# 宽转长：用“指标”作列名，年份作行
df = (
    df_raw
    .set_index('指标')[year_cols]
    .T
    .reset_index()
    .rename(columns={'index': 'year'})
)
df['year'] = df['year'].str.replace('年', '').astype(int)

# 2. 缺失值插补（Spline + 前后填充）
cols = ['premium_income', 'working_ratio', 'sex_ratio', 'urban_ratio']
df[cols] = (
    df[cols]
    .interpolate(method='spline', order=3)
    .ffill().bfill()
)

# 3. 偏度检查
print("各变量偏度：")
print(df[cols].skew(), "\n")

# 4. 变量变换
#  4.1 premium_income 做对数
df['log_premium_income'] = np.log(df['premium_income'])

#  4.2 edu_ratio 做 Box–Cox（仅对正值）
#pt_edu = PowerTransformer(method='box-cox', standardize=False)
#df['edu_ratio_bc'] = pt_edu.fit_transform((df[['edu_ratio']] + 1e-6))

#  4.3 working_ratio 做 Yeo–Johnson（可处理负偏/正偏）
#pt_wr = PowerTransformer(method='yeo-johnson', standardize=False)
#df['working_ratio_yj'] = pt_wr.fit_transform(df[['working_ratio']])

# 5. 构造特征矩阵和目标向量
X = df[['working_ratio', 'sex_ratio', 'urban_ratio']]
y = df['log_premium_income']

# 6. 特征标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# 7. OLS 回归
X_sm = sm.add_constant(X_scaled_df)
model = sm.OLS(y, X_sm).fit()
print("====== OLS 回归结果 ======")
print(model.summary(), "\n")

# 8. VIF 检查（包括常数项）
vif_df = X_scaled_df.copy()
vif_df['const'] = 1
vif = pd.DataFrame({
    'Variable': vif_df.columns,
    'VIF': [variance_inflation_factor(vif_df.values, i)
            for i in range(vif_df.shape[1])]
})
print("====== VIF 检查 ======")
print(vif, "\n")

# 9. 残差正态性 & 异方差性诊断（可选）
resid = model.resid

# 9.2 Breusch-Pagan 异方差检验
bp_test = sm.stats.diagnostic.het_breuschpagan(resid, model.model.exog)
labels = ['LM Statistic', 'LM p-value', 'F-Statistic', 'F p-value']
print("Breusch-Pagan test:")
print(dict(zip(labels, bp_test)))
