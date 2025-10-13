import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from scipy.io import loadmat
from mlxtend.plotting import plot_decision_regions

# 加载data2.mat数据集
data = loadmat('data2.mat')  # 假设data2.mat在你的工作目录下
X = data['X']  # 假设数据矩阵名为X
y = data['y']  # 假设标签矩阵名为y

# 可视化数据
if X.shape[1] == 2:
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', marker='o')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Visualization of data2.mat')
    plt.show()
else:
    print("Cannot visualize data in more than 2 dimensions.")

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 确保y_train和y_test都是一维数组
y_train = y_train.ravel()
y_test = y_test.ravel()

# 创建基于高斯核函数的SVM分类器
clf = svm.SVC(kernel='rbf', C=50.0, gamma='scale')

# 训练模型
clf.fit(X_train_scaled, y_train)

# 预测测试集
y_pred = clf.predict(X_test_scaled)

# 评估模型
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 展示分类结果和决策边界（仅对二维数据有效）
if X_train_scaled.shape[1] == 2:
    plt.figure(figsize=(10, 6))
    plot_decision_regions(X_test_scaled, y_test, clf=clf, legend=2)
    plt.scatter(X_test_scaled[:, 0], X_test_scaled[:, 1], c=y_test, cmap='viridis', marker='o')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Nonlinear SVM with RBF Kernel')
    plt.show()
else:
    print("Cannot visualize decision boundary in more than 2 dimensions.")
