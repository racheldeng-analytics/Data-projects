import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc


# 加载数据
data = loadmat('data1.mat')
X = data['X']  # 假设X是特征数据
y = data['y']  # 假设y是标签数据

# 可视化数据
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', marker='o')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Dataset Visualization')
plt.show()

X_train = X
y_train = y.reshape(-1,)

# 选择一系列C值来训练SVM
Cs = [1, 10, 50, 100, 1000]
colors = ['red', 'orange', 'green', 'black', 'purple']

# 绘制原始数据
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', marker='o', label='Data')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

# 遍历C值并绘制决策边界
for C, color in zip(Cs, colors):
    # 使用SVC创建SVM分类器，并设置C值
    clf = svm.SVC(kernel='linear', C=C)
    # 拟合模型
    clf.fit(X_train, y_train)

    # 绘制决策函数
    ax = plt.gca()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # 创建评估模型所需的网格
    xx = np.linspace(xlim[0], xlim[1], 30)
    yy = np.linspace(ylim[0], ylim[1], 30)
    YY, XX = np.meshgrid(yy, xx)
    xy = np.vstack([XX.ravel(), YY.ravel()]).T
    Z = clf.decision_function(xy).reshape(XX.shape)

    # 绘制决策边界和边距
    ax.contour(XX, YY, Z, colors=color, levels=[-1, 0, 1], alpha=0.5,
               linestyles=['--', '-', '--'])

    # 标记支持向量
    ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80,
               facecolors='none', edgecolors=color)

plt.legend()

plt.show()
