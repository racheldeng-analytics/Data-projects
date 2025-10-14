import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# ========== 1. 读取并整理数据 ==========
csv_path = r'C:\College\毕业\毕业设计\model sm.csv'
df_raw = pd.read_csv(csv_path, encoding='gbk')
year_cols = [c for c in df_raw.columns if c.endswith('年') and c[:4].isdigit()]
df = (
    df_raw
    .set_index('指标')[year_cols]
    .T
    .reset_index()
    .rename(columns={'index': 'year'})
)
df['year'] = df['year'].str.replace('年', '', regex=False).astype(int)
df = df.sort_values('year').reset_index(drop=True)

# ========== 2. 缺失值插补（Spline + 前后填充） ==========
cols = ['premium_income', 'working_ratio', 'sex_ratio', 'urban_ratio']
df = df.set_index('year')
df[cols] = df[cols].interpolate(method='spline', order=3).ffill().bfill()
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

y_array = y.values.reshape(-1, 1)
scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y_array).ravel()

# ========== 6. OLS回归 ==========
X_sm = sm.add_constant(X_scaled_df)
ols_model = sm.OLS(y, X_sm).fit()
print("====== 含滞后项的OLS回归结果 ======")
print(ols_model.summary())

dw_stat = durbin_watson(ols_model.resid)
print(f"\nDurbin-Watson统计量: {dw_stat:.3f}")
print("DW值解读： 接近2→无自相关; 接近0→正自相关; 接近4→负自相关")

vif_data = pd.DataFrame({
    'Variable': X_scaled_df.columns,
    'VIF': [variance_inflation_factor(X_scaled_df.values, i)
            for i in range(X_scaled_df.shape[1])]
})
print("\n====== 更新后的VIF值 ======")
print(vif_data)

# ========== 7. PLS回归：选择最佳组件数并评估 ==========
max_comp = min(X_scaled_df.shape[1], X_scaled_df.shape[0] - 1)
cv = KFold(n_splits=5, shuffle=True, random_state=0)
mse_list, mae_list, r2_list = [], [], []
for n_comp in range(1, max_comp + 1):
    pls = PLSRegression(n_components=n_comp)
    y_cv_scaled = cross_val_predict(pls, X_scaled_df, y_scaled, cv=cv)
    y_cv = scaler_y.inverse_transform(y_cv_scaled.reshape(-1, 1)).ravel()
    mse_list.append(mean_squared_error(y, y_cv))
    mae_list.append(mean_absolute_error(y, y_cv))
    r2_list.append(r2_score(y, y_cv))

print("\n组件数  MSE      MAE      R2")
for i, (mse, mae, r2) in enumerate(zip(mse_list, mae_list, r2_list), start=1):
    print(f"{i:>2d}    {mse:.3f}   {mae:.3f}   {r2:.3f}")
best_n = int(np.argmin(mse_list) + 1)
print(f"\n最佳组件数（基于最小MSE）: {best_n}")

# 用最佳组件数重拟合 PLS
pls_best = PLSRegression(n_components=best_n)
pls_best.fit(X_scaled_df, y_scaled)
y_pred_scaled = pls_best.predict(X_scaled_df)
y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

print("\n====== 最终PLS模型（组件数={}）性能 ======".format(best_n))
print(f"全样本 MSE: {mean_squared_error(y, y_pred):.3f}")
print(f"全样本 MAE: {mean_absolute_error(y, y_pred):.3f}")
print(f"全样本 R2: {r2_score(y, y_pred):.3f}")
print("回归系数（标准化基础）：")
for name, coef in zip(X_scaled_df.columns, pls_best.coef_.ravel()):
    print(f"  {name}: {coef:.4f}")

# ========== 8. 计算 VIP (变量重要性投影值) ==========
def calculate_vip(pls_model, X, y):
    t = pls_model.x_scores_
    w = pls_model.x_weights_
    q = pls_model.y_loadings_.ravel()
    p, h = w.shape
    # 每个成分对 y 的解释度
    SSY = np.array([(t[:, i] ** 2 * q[i] ** 2).sum() for i in range(h)])
    total_SSY = SSY.sum()
    vip = np.zeros((p,))
    for j in range(p):
        weight_sq = np.array([ (w[j, i] ** 2) * SSY[i] for i in range(h) ])
        vip[j] = np.sqrt(p * weight_sq.sum() / total_SSY)
    return vip

vip_scores = calculate_vip(pls_best, X_scaled_df.values, y_scaled)
vip_df = pd.DataFrame({'Variable': X_scaled_df.columns, 'VIP': vip_scores})
print("\n====== 变量重要性投影（VIP）======")
print(vip_df.to_string(index=False))

# ========== 9. 残差诊断图 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sm.qqplot(ols_model.resid, line='45', ax=axes[0])
axes[0].set_title('Q-Q图')
pd.plotting.autocorrelation_plot(ols_model.resid, ax=axes[1])
axes[1].set_title('残差自相关图')
plt.tight_layout()
plt.show()
