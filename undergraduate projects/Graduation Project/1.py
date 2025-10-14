import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

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
# 去掉“年”并转为整数类型 df['year'] 后请立即排序
df['year'] = df['year'].str.replace('年', '', regex=False).astype(int)

df = df.sort_values('year').reset_index(drop=True)

# ========== 2. 缺失值插补（Spline + 前后填充） ==========
# 先把 year 设置为索引，这样插值就是按真实年份间隔进行的
cols = ['premium_income', 'working_ratio', 'sex_ratio', 'urban_ratio']
df = df.set_index('year')
df[cols] = (
    df[cols]
    .interpolate(method='spline', order=3)
    .ffill()
    .bfill()
)
# 恢复原表格结构
df = df.reset_index()

# ========== 3. 对数变换与一阶滞后项 ==========
# 对premium_income取对数
df['log_premium_income'] = np.log(df['premium_income'])
# 确保按年份再次排序
df = df.sort_values('year').reset_index(drop=True)
# 创建滞后一期的对数保费收入
df['log_premium_lag1'] = df['log_premium_income'].shift(1)
# 只因滞后列缺失而丢弃第一行，其它边界的NaN已被填充
df = df.dropna(subset=['log_premium_lag1']).reset_index(drop=True)

# ========== 4. 构造特征矩阵和响应变量 ==========
X = df[['working_ratio', 'sex_ratio', 'urban_ratio', 'log_premium_lag1']]
y = df['log_premium_income']

# ========== 5. 标准化处理 ==========
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

# ========== 6. OLS回归 ==========
X_sm = sm.add_constant(X_scaled_df)
model = sm.OLS(y, X_sm).fit()
print("====== 含滞后项的OLS回归结果 ======")
print(model.summary())

# ========== 7. Durbin-Watson自相关诊断 ==========
dw_stat = durbin_watson(model.resid)
print(f"\nDurbin-Watson统计量: {dw_stat:.3f}")
print("DW值解读： 接近2→无自相关; 接近0→正自相关; 接近4→负自相关")

# ========== 8. VIF检查（不含常数项） ==========
vif_data = pd.DataFrame({
    'Variable': X_scaled_df.columns,
    'VIF': [variance_inflation_factor(X_scaled_df.values, i)
            for i in range(X_scaled_df.shape[1])]
})
print("\n====== 更新后的VIF值 ======")
print(vif_data)

# ========== 9. 残差诊断图 ==========
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
