import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression

# ========== 1. 读取并整理数据 ==========
csv_path = r'C:\College\毕业\毕业设计\model sm.csv'
df_raw = pd.read_csv(csv_path, encoding='gbk')
# 挑选年度列并做宽转长格式
year_cols = [c for c in df_raw.columns if c.endswith('年') and c[:4].isdigit()]
df = (
    df_raw
    .set_index('指标')[year_cols]
    .T
    .reset_index()
    .rename(columns={'index': 'year'})
)
# 去掉“年”并转为整数类型
df['year'] = df['year'].str.replace('年', '', regex=False).astype(int)
# 按年排序并重置索引
df = df.sort_values('year').reset_index(drop=True)

# ========== 2. 缺失值插补（Spline + 前后填充） ==========
cols = ['premium_income', 'working_ratio', 'sex_ratio', 'urban_ratio']
df = df.set_index('year')
df[cols] = (
    df[cols]
    .interpolate(method='spline', order=3)
    .ffill()
    .bfill()
)
df = df.reset_index()

# ========== 3. 对数变换与一阶滞后项 ==========
df['log_premium_income'] = np.log(df['premium_income'])
df = df.sort_values('year').reset_index(drop=True)
df['log_premium_lag1'] = df['log_premium_income'].shift(1)
df = df.dropna(subset=['log_premium_lag1']).reset_index(drop=True)

# ========== 4. 构造特征矩阵和响应变量 ==========
X = df[['working_ratio', 'sex_ratio', 'urban_ratio', 'log_premium_lag1']]
y = df['log_premium_income']

# ========== 5. 标准化处理 ==========
scaler_X = StandardScaler()
X_scaled = scaler_X.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
# 同时标准化 y 为后续 PLS 使用
y_array = y.values.reshape(-1, 1)
scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y_array)

# ========== 6. OLS回归 ==========
X_sm = sm.add_constant(X_scaled_df)
model = sm.OLS(y, X_sm).fit()
print("====== 含滞后项的OLS回归结果 ======")
print(model.summary())

# Durbin-Watson 自相关诊断
dw_stat = durbin_watson(model.resid)
print(f"\nDurbin-Watson统计量: {dw_stat:.3f}")
print("DW值解读： 接近2→无自相关; 接近0→正自相关; 接近4→负自相关")

# VIF 检查（不含常数项）
vif_data = pd.DataFrame({
    'Variable': X_scaled_df.columns,
    'VIF': [variance_inflation_factor(X_scaled_df.values, i)
            for i in range(X_scaled_df.shape[1])]
})
print("\n====== 更新后的VIF值 ======")
print(vif_data)

# ========== 7. PLS回归（缓解多重共线性） ==========
# 选择潜在成分数，可根据CV或经验确定
n_components = 2
pls = PLSRegression(n_components=n_components)
pls.fit(X_scaled_df, y_scaled)
# 预测并反标准化
y_pred_scaled = pls.predict(X_scaled_df)
y_pred = scaler_y.inverse_transform(y_pred_scaled)
# 输出PLS模型结果
print(f"\n====== PLS回归（{n_components} 个成分）结果 ======")
print("回归系数（标准化基础）：")
for name, coef in zip(X_scaled_df.columns, pls.coef_.ravel()):
    print(f"  {name}: {coef:.4f}")
r2_pls = pls.score(X_scaled_df, y_scaled)
print(f"PLS模型拟合 R^2: {r2_pls:.3f}")

# ========== 8. 残差诊断图 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
# Q-Q图
sm.qqplot(model.resid, line='45', ax=axes[0])
axes[0].set_title('Q-Q图')
# 自相关图
pd.plotting.autocorrelation_plot(model.resid, ax=axes[1])
axes[1].set_title('残差自相关图')
plt.tight_layout()
plt.show()
