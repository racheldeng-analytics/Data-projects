import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.preprocessing import StandardScaler

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

n_samples = 1000
datasets = generateData(n_samples)
titles = ['Blobs', 'Circles', 'Moons', 'Blocks']
plotData(datasets, titles)