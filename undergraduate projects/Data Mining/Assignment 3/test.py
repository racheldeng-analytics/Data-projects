import numpy as np
import tensorflow as tf
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

def generateData(n):
    np.random.seed(12046)
    blobs = make_blobs(n_samples=n, centers=[[-2, -2], [2, 2]])
    circles = make_circles(n_samples=n, factor=.4, noise=.05)
    moons = make_moons(n_samples=n, noise=.05)
    blocks = np.random.rand(n, 2) - 0.5
    y = (blocks[:, 0] * blocks[:, 1] < 0) + 0
    blocks = (blocks, y)
    # 由于神经网络对数据的线性变换不稳定，因此将数据做归一化处理
    scaler = StandardScaler()
    blobs = (scaler.fit_transform(blobs[0]), blobs[1])
    circles = (scaler.fit_transform(circles[0]), circles[1])
    moons = (scaler.fit_transform(moons[0]), moons[1])
    blocks = (scaler.fit_transform(blocks[0]), blocks[1])

    return blobs, circles, moons, blocks

def plotData(datasets, titles):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    for ds, title, ax in zip(datasets, titles, axs.flatten()):
        ax.scatter(ds[0][:, 0], ds[0][:, 1], c=ds[1], cmap='viridis', edgecolor='k')
        ax.set_title(title)
    plt.show()

def trainAndPlot(datasets, titles):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle('Figure 2: Classification Results', fontsize=16)
    for ds, title, ax in zip(datasets, titles, axs.flatten()):
        X, y = ds
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(4, activation='sigmoid', input_shape=(2,)),
            tf.keras.layers.Dense(4, activation='sigmoid'),
            tf.keras.layers.Dense(2, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)
        y_pred = np.argmax(model.predict(X_test), axis=1)

        accuracy = accuracy_score(y_test, y_pred)
        scatter = ax.scatter(X_test[:, 0], X_test[:, 1], c=y_pred, cmap='viridis', edgecolor='k', marker='o')
        ax.set_title(f"{title} - Accuracy: {accuracy:.2f}")

    plt.show()

def plotLossCurves(datasets, titles):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.suptitle('Figure 3: Loss Curves', fontsize=16)
    for ds, title in zip(datasets, titles):
        X, y = ds
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(4, activation='sigmoid', input_shape=(2,)),
            tf.keras.layers.Dense(4, activation='sigmoid'),
            tf.keras.layers.Dense(2, activation='sigmoid')
        ])
        loss_curve = []
        for i in range(1, 1001):
            model.fit(X_train, y_train)
            loss_curve.append(model.loss_)
        ax.plot(range(1, 1001), loss_curve, label=title)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Loss')
    ax.set_title('Loss Curves')
    ax.legend()
    plt.show()


n_samples = 1000
datasets = generateData(n_samples)
titles = ['Blobs', 'Circles', 'Moons', 'Blocks']
plotData(datasets, titles)
trainAndPlot(datasets, titles)
plotLossCurves(datasets, titles)
