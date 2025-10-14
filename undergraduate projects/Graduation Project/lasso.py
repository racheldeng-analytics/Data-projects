import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV
from sklearn.metrics import mean_squared_error

# 1. 读取并清洗数据
df_raw = pd.read_csv(r'C:\College\毕业\毕业设计\model sm.csv', encoding='gbk')
# 2. 看看有哪些指标
print("原始指标列表:", df_raw['指标'].unique())

# 3. 找到所有“年”字段
year_cols = [col for col in df_raw.columns if '年' in col and col[:4].isdigit()]

# 4. 转置，用原始指标名作为列名
df = df_raw.set_index('指标')[year_cols].T
df.columns = df_raw['指标'].values
df.index.name = 'year'
df.reset_index(inplace=True)

# 5. 数据清洗
df['year'] = df['year'].str.replace('年', '').astype(int)
df = df.apply(pd.to_numeric, errors='coerce').interpolate().ffill().bfill()



# 3. 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Lasso 回归 + 交叉验证选择最优 alpha
lasso_cv = LassoCV(cv=5, random_state=0, max_iter=10000).fit(X_scaled, y)

# 5. 输出结果
print(f"Best alpha selected by CV: {lasso_cv.alpha_:.6f}")

coefs = pd.Series(lasso_cv.coef_, index=X.columns)
print("Lasso coefficients:")
print(coefs)

# 6. 模型性能
y_pred = lasso_cv.predict(X_scaled)
mse = mean_squared_error(y, y_pred)
print(f"\nMean Squared Error: {mse:.2f}")

# 7. （可选）将预测和实际放在 DataFrame 中对比
comparison = pd.DataFrame({
    'year': df['year'],
    'actual_premium': y,
    'predicted_premium': y_pred
})
print("\nActual vs Predicted:")
print(comparison.set_index('year'))

