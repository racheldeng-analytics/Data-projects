import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# 1. 数据准备
df = pd.read_excel("C:\College\数学\大三下学习资料\数据挖掘\数据挖掘作业（第1次作业聚类分析）\数据挖掘作业（第1次作业聚类分析）\去除因子数据.xlsx")

# 假设df是包含所有股票数据的DataFrame，并且已经按年度筛选
# 假设我们只关注某一年的数据，例如2000年
df_2000 = df[df['年份'] == 2000].drop('年份', axis=1)

# X是特征矩阵，即除去股票号之外的所有指标数据
X = df_2000.drop('股票号', axis=1)

# 2. 确定合适的聚类数目K

# 初始化一个用于存储不同K值对应的SSE的列表
distortions = []

# 设定要测试的K值范围
K = range(1, 7)  # 例如，测试从1到10个聚类

# 对于每个K值，计算SSE并存储
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    distortions.append(kmeans.inertia_)

# 绘制手肘图
plt.plot(K, distortions, '-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()

# 观察图形并选择SSE开始平缓下降的点作为K值
optimal_k = 7 # 根据图形选择合适的K值

# 3. K-均值聚类
# 使用最佳的K值进行K-均值聚类
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(X)

# 获取每个股票的聚类标签
labels = kmeans.labels_

# 将聚类标签添加到原始DataFrame中
df_2000['Cluster'] = labels
print(df_2000.columns)

# 4. 划分股票板块
# 打印每个聚类的股票列表
for i in range(optimal_k):
    cluster_stocks = df_2000[df_2000['Cluster'] == i]['股票号'].tolist()
    print(f"Cluster {i+1}: {cluster_stocks}")

# 5. 评价各类的优劣性

# 计算轮廓系数
silhouette_avg = silhouette_score(X, labels)
print("The average silhouette_score is :", silhouette_avg)

# SSE即聚类目标函数值
sse_final = kmeans.inertia_
print("SSE (Clustering Objective Function):", sse_final)

from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score


from sklearn.metrics import calinski_harabasz_score
# 首先，我们需要将特征列和聚类标签分开
X_features = df_2000.drop('Cluster', axis=1)  # 特征数据矩阵
clusters = df_2000['Cluster']  # 聚类标签数组

# 计算Calinski-Harabasz Index
calinski_harabasz = calinski_harabasz_score(X_features, clusters)
print("Calinski-Harabasz Index: ", calinski_harabasz)

# 计算Davies-Bouldin Index
davies_bouldin = davies_bouldin_score(X_features, clusters)
print("Davies-Bouldin Index:",  davies_bouldin)





