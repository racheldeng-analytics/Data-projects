import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, f1_score

# 加载数据
data = loadmat('data3.mat')
X = data['X']
y = data['y'].flatten()  # 将y转化为numpy数组
Xval = data['Xval']
yval = data['yval'].flatten()

# 可视化训练数据
plt.scatter(X[y == 0, 0], X[y == 0, 1], color='blue', label='Class 0')
plt.scatter(X[y == 1, 0], X[y == 1, 1], color='red', label='Class 1')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

Cs = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]
gammas = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]  # 注意这里的值实际上对应于1 / (2 * sigma^2)
best_score = -1
best_C = None
best_gamma = None

for C in Cs:
    for gamma in gammas:
        clf = svm.SVC(kernel='rbf', C=C, gamma=gamma)
        # 假设我们使用5折交叉验证
        scores = cross_val_score(clf, X, y, cv=5)
        if np.mean(scores) > best_score:
            best_score = np.mean(scores)
            best_C = C
            best_gamma = gamma

print(f"Best C: {best_C}, Best gamma: {best_gamma}, Best score: {best_score}")

# 使用最佳参数训练SVM
clf = svm.SVC(kernel='rbf', C=best_C, gamma=best_gamma)
clf.fit(X, y)

# 预测训练集和测试集
y_train_pred = clf.predict(X)
y_val_pred = clf.predict(Xval)

# 定义绘制边界的参数范围
ax_min, ax_max = X[:, 0].min() - 1, X[:, 0].max() + 1
ay_min, ay_max = X[:, 1].min() - 1, X[:, 1].max() + 1

# 创建网格
hx = (ax_max - ax_min) / 200
hy = (ay_max - ay_min) / 200
xx, yy = np.meshgrid(np.arange(ax_min, ax_max, hx), np.arange(ay_min, ay_max, hy))

# 使用训练好的SVM模型预测网格上的点
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# 将预测结果重新组织成网格的形状
Z = Z.reshape(xx.shape)

# 绘制决策边界和样本点
plt.figure()
plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
plt.scatter(X[y == 0, 0], X[y == 0, 1], color='blue', label='Class 0', alpha=0.5)
plt.scatter(X[y == 1, 0], X[y == 1, 1], color='red', label='Class 1', alpha=0.5)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.title('SVM with RBF kernel')
plt.show()

# 缩小绘图范围，使数据点在图中看起来更大
ax_min, ax_max = X[:, 0].min() - 0.2, X[:, 0].max() + 0.2
ay_min, ay_max = X[:, 1].min() - 0.2, X[:, 1].max() + 0.2

# 创建网格
hx = (ax_max - ax_min) / 200
hy = (ay_max - ay_min) / 200
xx, yy = np.meshgrid(np.arange(ax_min, ax_max, hx), np.arange(ay_min, ay_max, hy))

# 使用训练好的SVM模型预测网格上的点
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# 将预测结果重新组织成网格的形状
Z = Z.reshape(xx.shape)

# 绘制决策边界和样本点
plt.figure()
plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

plt.scatter(X[y == 0, 0], X[y == 0, 1], color='blue', label='Class 0', alpha=0.5)
plt.scatter(X[y == 1, 0], X[y == 1, 1], color='red', label='Class 1', alpha=0.5)

plt.xlim(ax_min, ax_max)  # 设置x轴的范围
plt.ylim(ay_min, ay_max)  # 设置y轴的范围

plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.title('SVM with RBF kernel')
plt.show()

# 评估模型
# 计算训练集上的性能
train_accuracy = accuracy_score(y, y_train_pred)
train_precision = precision_score(y, y_train_pred, average='binary')  # 假设是二分类问题
train_f1 = f1_score(y, y_train_pred, average='binary')  # 假设是二分类问题
# 计算验证集上的性能
val_accuracy = accuracy_score(yval, y_val_pred)
val_precision = precision_score(yval, y_val_pred, average='binary')  # 假设是二分类问题
val_f1 = f1_score(yval, y_val_pred, average='binary')  # 假设是二分类问题

# 打印结果
print(f"Training Accuracy: {train_accuracy}")
print(f"Training Precision: {train_precision}")
print(f"Training F1 Score: {train_f1}")
print(f"Validation Accuracy: {val_accuracy}")
print(f"Validation Precision: {val_precision}")
print(f"Validation F1 Score: {val_f1}")

