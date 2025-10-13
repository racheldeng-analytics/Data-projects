import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import os
from skimage.metrics import structural_similarity as ssim


# 已经有了一个RGB图片，将其转换为numpy数组
img = Image.open(r'C:\College\数学\大三下学习资料\数据挖掘\数据挖掘作业（第1次作业聚类分析）\数据挖掘作业（第1次作业聚类分析）\图片1.png').convert('RGB')
img_array = np.array(img)

# 获取图片的高度和宽度
m, n, _ = img_array.shape  # 这里的_用于接收通道数，因为我们知道它是3（RGB）

# 第一步：将三维数据转化为二维数据
pixels = img_array.reshape(-1, 3)

# 第二步：聚类

num_clusters = 48  # 设置聚类数为16
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(pixels)
labels = kmeans.labels_  # 每个像素点的聚类下标
cluster_centers = kmeans.cluster_centers_  # 聚类中心颜色

# 第三步：我们已经有了特征值和聚类下标，不需要额外操作

# 第四步：使用for循环遍历每个像素，并将其颜色替换为对应的聚类中心颜色
compressed_img_array = np.zeros_like(img_array)  # 创建一个与原图同样大小的零数组用于存放压缩后的颜色
for i in range(m):
    for j in range(n):
        index = i * n + j  # 计算当前像素在二维数组中的索引
        label = labels[index]  # 获取当前像素的聚类标签
        compressed_img_array[i, j] = cluster_centers[label]  # 设置压缩后的颜色

# 显示原始图片和压缩后的图片
from matplotlib import pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(img_array)
axs[0].set_title('Original Image')
axs[1].imshow(compressed_img_array.astype(np.uint8))
axs[1].set_title('Compressed Image')
plt.show()

# 如果你想要保存压缩后的图片
compressed_img = Image.fromarray(compressed_img_array.astype(np.uint8), 'RGB')
compressed_img.save('compressed_image.jpg')



# 假设原始图像和压缩后的图像文件路径分别为
original_image_path = "C:\College\数学\大三下学习资料\数据挖掘\数据挖掘作业（第1次作业聚类分析）\数据挖掘作业（第1次作业聚类分析）\图片1.png"
compressed_image_path = "C:\College\数学\大三下学习资料\数据挖掘\数据挖掘作业（第1次作业聚类分析）\数据挖掘作业（第1次作业聚类分析）\compressed_image.jpg"

# 获取文件大小
original_size = os.path.getsize(original_image_path)
compressed_size = os.path.getsize(compressed_image_path)

# 计算压缩比
compression_ratio = original_size / compressed_size
print(f"Compression Ratio: {compression_ratio:.2f}")

# 计算MSE
# 读取图像

with Image.open(original_image_path) as original_img:
    original_image = np.array(original_img)

with Image.open(compressed_image_path) as compressed_img:
    compressed_image = np.array(compressed_img)

# 确保图像具有相同的维度
if original_image.shape != compressed_image.shape:
    raise ValueError("Images must have the same shape")

# 如果图像是彩色的，则它们应该是三维的。为了计算MSE，我们需要将它们转换为一维
if len(original_image.shape) == 3:
    original_image = original_image.reshape(-1)
    compressed_image = compressed_image.reshape(-1)

# 计算MSE
mse = np.mean((original_image - compressed_image) ** 2)
print(f"Mean Squared Error (MSE): {mse:.2f}")

# 计算SSIM
ssim_value = ssim(original_image, compressed_image, multichannel=True)
print(f"Structural Similarity Index (SSIM): {ssim_value:.4f}")

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

# 计算PSNR
psnr = calculate_psnr(original_image, compressed_image)
print(f"Peak Signal-to-Noise Ratio (PSNR): {psnr:.2f} dB")