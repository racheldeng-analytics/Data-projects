import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import KBinsDiscretizer
# 禁用joblib多线程警告
os.environ["LOKY_MAX_CPU_COUNT"] = "4"


class GM11:
    def __init__(self, data, predict_step=5):
        self.data = np.array(data, dtype=np.float64)
        self.predict_step = predict_step
        self.a = None
        self.b = None
        self.C = None
        self.mape = 0.0  # 默认初始化
        self.fitted_values = np.zeros_like(self.data)
        self.valid = True

    def _ratio_test(self):
        ratios = self.data[:-1] / self.data[1:]
        lower, upper = np.exp(-2 / (len(self.data) + 1)), np.exp(2 / (len(self.data) + 1))
        return np.all((ratios > lower) & (ratios < upper))

    def fit(self):
        if not self._ratio_test():
            self.valid = False
            self.fitted_values = self.data.copy()
            return

        AGO = np.cumsum(self.data).reshape(-1, 1)
        B = np.ones((len(self.data) - 1, 2))
        B[:, 0] = -0.5 * (AGO[:-1] + AGO[1:]).flatten()
        Y = self.data[1:].reshape(-1, 1)

        try:
            [[a], [b]] = np.linalg.inv(B.T @ B) @ B.T @ Y
        except np.linalg.LinAlgError:
            a, b = 0.1, 0.1  # 处理奇异矩阵

        self.a, self.b = a, b
        self.fitted_values = (self.data[0] - b / a) * (1 - np.exp(a)) * np.exp(-a * np.arange(len(self.data)))

        residuals = self.data - self.fitted_values
        S1 = np.var(self.data, ddof=1)
        S2 = np.var(residuals, ddof=1)
        self.C = S2 / S1
        self.mape = np.mean(np.abs((self.data - self.fitted_values) / self.data)) * 100

    def predict(self):
        t = np.arange(len(self.data), len(self.data) + self.predict_step)
        return (self.data[0] - self.b / self.a) * (1 - np.exp(self.a)) * np.exp(-self.a * t)


class MarkovChain:
    def __init__(self, n_states=3):
        self.n_states = n_states
        self.trans_mat = None

    def fit(self, states):
        trans_counts = np.zeros((self.n_states, self.n_states))
        for i in range(len(states) - 1):
            trans_counts[states[i], states[i + 1]] += 1
        self.trans_mat = trans_counts / (trans_counts.sum(axis=1, keepdims=True) + 1e-8)  # 防止除零

    def predict_next(self, current_state):
        return np.random.choice(self.n_states, p=self.trans_mat[current_state])


class GreyMarkov:
    def __init__(self, data, predict_step=5, n_states=3):
        self.data = np.array(data)
        self.predict_step = predict_step
        self.n_states = n_states
        self.gm = GM11(data, predict_step)
        self.markov = MarkovChain(n_states)
        self.state_bins = None
        self.fitted_values = None
        self.C = None
        self.mape = 0.0  # 新增MAPE记录

    def fit(self):
        self.gm.fit()
        residuals = self.gm.data - self.gm.fitted_values

        # 修复subsample警告
        discretizer = KBinsDiscretizer(n_bins=self.n_states, encode='ordinal',
                                       strategy='kmeans', subsample=None)
        states = discretizer.fit_transform(residuals.reshape(-1, 1)).flatten().astype(int)
        self.state_bins = discretizer.bin_edges_[0]

        self.markov.fit(states)
        residual_centers = [(self.state_bins[s] + self.state_bins[s + 1]) / 2 for s in states]
        self.fitted_values = self.gm.fitted_values + residual_centers

        new_residuals = self.data - self.fitted_values
        S1 = np.var(self.data, ddof=1)
        S2 = np.var(new_residuals, ddof=1)
        self.C = S2 / S1
        self.mape = np.mean(np.abs((self.data - self.fitted_values) / self.data)) * 100  # 记录MAPE

    def predict(self):
        gm_pred = np.concatenate([self.gm.fitted_values, self.gm.predict()])

        # 状态预测
        current_state = max(0, min(int((self.data[-1] - self.fitted_values[-1] - self.state_bins[0]) //
                                       (self.state_bins[1] - self.state_bins[0])), self.n_states - 1))
        state_path = [current_state]
        for _ in range(self.predict_step):
            next_state = self.markov.predict_next(current_state)
            state_path.append(next_state)
            current_state = next_state

        residual_centers = [(self.state_bins[s] + self.state_bins[s + 1]) / 2 for s in state_path[-self.predict_step:]]
        final_pred = gm_pred[-self.predict_step:] + residual_centers
        return np.concatenate([gm_pred[:len(self.data)], final_pred])


class MonteCarloGM:
    def __init__(self, data, pred_steps=5, trials=1000, noise_scale=0.1):
        self.data = np.array(data)
        self.pred_steps = pred_steps
        self.trials = trials
        self.noise_scale = noise_scale
        self.pred_matrix = None

    def run_simulation(self):
        """执行蒙特卡洛模拟（添加异常处理）"""
        self.pred_matrix = np.full((self.trials, len(self.data) + self.pred_steps), np.nan)

        for i in range(self.trials):
            try:
                # 添加正态分布噪声
                noise = np.random.normal(0, self.noise_scale * np.std(self.data), len(self.data))
                noisy_data = self.data + noise

                # 拟合模型
                model = GM11(noisy_data, self.pred_steps)
                model.fit()
                if model.valid:  # 仅记录有效预测
                    self.pred_matrix[i] = np.concatenate([model.fitted_values, model.predict()])
            except:
                continue  # 跳过失败的试验

    def get_intervals(self, alpha=0.05):
        """计算置信区间（处理NaN）"""
        lower = np.nanpercentile(self.pred_matrix, 100 * alpha / 2, axis=0)
        upper = np.nanpercentile(self.pred_matrix, 100 * (1 - alpha / 2), axis=0)
        return lower, upper


age_groups = {
    "0-14": [22423, 22712, 22824, 23252, 23522, 23751, 23689, 25277, 24678, 23908, 23063],
    "15-64": [101041, 101032, 100978, 100943, 100528, 100065, 99552, 96871, 96526, 96289, 96228],
    "65+": [13262, 13902, 14524, 15037, 15961, 16724, 17767, 19064, 20056, 20978, 21676]
}

years = np.arange(2013, 2024)
pred_years = 5
all_years = np.arange(years[0], years[-1] + pred_years + 1)
results = {}
metrics = {}

# 统一处理所有年龄段
for name, data in age_groups.items():
    data_array = np.array(data)
    try:
        if name == "0-14":
            model = GreyMarkov(data_array, pred_years, 3)
            model.fit()
            results[name] = model.predict()
            metrics[name] = {"C": model.C, "MAPE": model.mape}

        elif name == "65+":
            # 基础模型
            base_model = GM11(data_array, pred_years)
            base_model.fit()

            # 蒙特卡洛模拟
            mc = MonteCarloGM(data_array, pred_years, trials=5000, noise_scale=0.15)
            mc.run_simulation()
            lower, upper = mc.get_intervals()

            # 存储结果
            results[name] = {
                'base': np.concatenate([base_model.fitted_values, base_model.predict()]),
                'lower': lower,
                'upper': upper
            }
            metrics[name] = {"C": base_model.C, "MAPE": base_model.mape}  # 新增

        else:
            model = GM11(data_array, pred_years)
            model.fit()
            results[name] = np.concatenate([model.fitted_values, model.predict()])
            metrics[name] = {"C": model.C, "MAPE": model.mape}

    except Exception as e:
        print(f"{name}预测失败: {str(e)}")
        results[name] = np.zeros(len(all_years))
        metrics[name] = {"C": 1.0, "MAPE": 100.0}

# 可视化（修复标签语法）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
colors = {'0-14': '#1f77b4', '15-64': '#ff7f0e', '65+': '#2ca02c'}

plt.figure(figsize=(14, 8))
for name in age_groups:
    # 绘制实际数据点
    plt.scatter(years, age_groups[name], color=colors[name], s=80, edgecolor='k',
                zorder=5, label=f'{name}实际')

    # 绘制预测曲线
    if name == "65+":
        # 置信区间
        plt.fill_between(all_years, results[name]['lower'], results[name]['upper'],
                         color=colors[name], alpha=0.2)
        # 预测线
        plt.plot(all_years, results[name]['base'], '--', color=colors[name],
                 label=f'{name}预测 (C={metrics[name]["C"]:.4f}, MAPE={metrics[name]["MAPE"]:.1f}%)')
    else:
        plt.plot(all_years, results[name], '--', color=colors[name],
                 label=f'{name}预测 (C={metrics[name]["C"]:.4f}, MAPE={metrics[name]["MAPE"]:.1f}%)')

plt.axvline(2023, color='gray', linestyle=':', linewidth=2)
plt.title("人口年龄结构预测分析 (2013-2028)", fontsize=15)
plt.xlabel("年份", fontsize=12)
plt.ylabel("人口规模（万人）", fontsize=12)
plt.xticks(all_years[::2], rotation=45)
plt.grid(linestyle='--', alpha=0.6)
plt.legend(loc='upper left', bbox_to_anchor=(1, 0.9))
plt.tight_layout()
plt.show()

# 输出指标
print("\n模型检验指标：")
print("年龄段\t\tC值\t\tMAPE(%)")
print("----------------------------------------")
for name in metrics:
    print(f"{name}\t\t{metrics[name]['C']:.4f}\t\t{metrics[name]['MAPE']:.2f}")