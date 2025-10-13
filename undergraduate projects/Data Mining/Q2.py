import numpy as np
import tensorflow as tf
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


# 生成数据集
def generateData(n):
    blobs = make_blobs(n_samples=n, centers=[[-2, -2], [2, 2]], random_state=42)
    circles = make_circles(n_samples=n, factor=.4, noise=.05, random_state=42)
    moons = make_moons(n_samples=n, noise=.05, random_state=42)
    blocks = np.random.rand(n, 2) - 0.5
    y_blocks = (blocks[:, 0] * blocks[:, 1] < 0).astype(int)
    blocks = (blocks, y_blocks)

    # 归一化数据
    scaler = StandardScaler()
    blobs = (scaler.fit_transform(blobs[0]), blobs[1])
    circles = (scaler.fit_transform(circles[0]), circles[1])
    moons = (scaler.fit_transform(moons[0]), moons[1])
    blocks = (scaler.fit_transform(blocks[0]), blocks[1])

    return blobs, circles, moons, blocks


# 创建神经网络模型
'''def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(4, activation='sigmoid', input_shape=(2,)),
        tf.keras.layers.Dense(4, activation='sigmoid'),
        tf.keras.layers.Dense(2, activation='softmax')  # 假设是多分类问题
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model'''

def trainAndPlot(datasets, titles):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle('Figure 2: Classification Results', fontsize=16)
    for ds, title, ax in zip(datasets, titles, axs.flatten()):
        X, y = ds
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(4, activation='sigmoid', input_shape=(2,)),
            tf.keras.layers.Dense(4, activation='sigmoid'),
            tf.keras.layers.Dense(2, activation='softmax')  # 假设是多分类问题
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)
        y_pred = np.argmax(model.predict(X_test), axis=1)

        accuracy = accuracy_score(y_test, y_pred)
        scatter = ax.scatter(X_test[:, 0], X_test[:, 1], c=y_pred, cmap='viridis', edgecolor='k', marker='o')
        ax.set_title(f"{title} - Accuracy: {accuracy:.2f}")

    plt.show()

# 训练和预测
'''def train_and_predict(model, X_train, y_train, X_test):
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)
    y_pred = np.argmax(model.predict(X_test), axis=1)
    return y_pred


# 绘制分类结果
def plot_classification_results(X, y_true, y_pred, title):
    plt.figure(figsize=(8, 6))
    plt.scatter(X[y_pred == y_true, 0], X[y_pred == y_true, 1], c='blue', edgecolor='k', marker='o', label='Correct')
    plt.scatter(X[y_pred != y_true, 0], X[y_pred != y_true, 1], c='red', edgecolor='k', marker='x', label='Incorrect')
    plt.title(f"{title} - Accuracy: {accuracy:.2f}")
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.show()'''


# 主程序
n_samples = 1000  # 样本数量
blobs, circles, moons, blocks = generateData(n_samples)

'''datasets = {
    'Blobs': blobs,
    'Circles': circles,
    'Moons': moons,
    'Blocks': blocks
}'''


datasets = generateData(n_samples)
titles = ['Blobs', 'Circles', 'Moons', 'Blocks']

'''for i, (name, (X, y)) in enumerate(datasets.items()):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = create_model()
    y_pred = train_and_predict(model, X_train, y_train, X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Dataset: {name}, Accuracy: {accuracy:.2f}")
    plot_classification_results(X_test, y_test, y_pred, f"Classification Results for {name}")
    #plot_classification_results(X_test, y_test, y_pred, ax=axs[i], title=f"Classification Results for {name}")
    #plot_all_classification_results(datasets, model)'''

trainAndPlot(datasets, titles)