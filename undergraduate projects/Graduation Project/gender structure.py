import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
import math


def gm11(x0, predict_len=5):
    x0 = np.array(x0, dtype=float)
    n = len(x0)

    # 1. 累加生成序列 X(1)
    x1 = np.cumsum(x0)

    # 2. 计算背景值序列 Z(1)，通常采用相邻两项平均
    z1 = np.array([0.5 * (x1[i] + x1[i - 1]) for i in range(1, n)])

    # 3. 构造矩阵，最小二乘法估计参数 a 和 b
    B = np.column_stack((-z1, np.ones(n - 1)))
    Y = x0[1:].reshape((n - 1, 1))
    coeff, _, _, _ = np.linalg.lstsq(B, Y, rcond=None)
    a, b = coeff.flatten()

    # 4. 构造时间响应函数并预测累计序列 X(1)
    def calc_x1(k):
        return (x0[0] - b / a) * np.exp(-a * k) + b / a

    x1_pred = np.array([calc_x1(k) for k in range(n + predict_len)])

    # 5. 差分还原得到原始序列的预测值
    x0_pred = np.empty(n + predict_len)
    x0_pred[0] = x0[0]
    for k in range(1, n + predict_len):
        x0_pred[k] = x1_pred[k] - x1_pred[k - 1]

    return x0_pred, a, b


def posterior_error_ratio(real, pred):
    real = np.array(real, dtype=float)
    pred = np.array(pred, dtype=float)
    residuals = real - pred
    C = np.std(residuals, ddof=1) / np.std(real, ddof=1)
    return C


def calculate_metrics(real, pred):
    real = np.array(real, dtype=float)
    pred = np.array(pred, dtype=float)
    n = len(real)
    mape = np.mean(np.abs((real - pred) / real)) * 100  # 百分比
    return mape


def gm11_with_residual_correction(x0, predict_len=5):
    # GM(1,1)预测
    gm_pred, a, b = gm11(x0, predict_len=predict_len)
    n = len(x0)

    # 计算历史部分的残差
    residuals = np.array(x0) - gm_pred[:n]

    # AR模型拟合残差（采用 AR(1)）
    model = AutoReg(residuals, lags=1, old_names=False)
    model_fit = model.fit()
    lag = model_fit.model._maxlag  # 一般等于1

    # 为了避免初始预测nan，采用：
    # 对历史数据：前 lag 个残差直接用实际值，其余用模型预测
    in_sample_pred = model_fit.predict(start=lag, end=n - 1)
    res_hist = np.concatenate((residuals[:lag], in_sample_pred))

    # 对未来预测：直接用 AR 模型预测未来 predict_len 个残差
    res_forecast = model_fit.predict(start=n, end=n + predict_len - 1)

    # 拼接为完整的残差预测序列
    res_ar_pred = np.concatenate((res_hist, res_forecast))

    # 最终预测 = GM(1,1)预测 + AR(1)残差修正
    final_pred = gm_pred + res_ar_pred
    return final_pred, gm_pred, res_ar_pred


# -------------------------- 主程序 --------------------------
if __name__ == "__main__":
    # 示例数据（请替换为实际数据）
    years = np.arange(2013, 2024)  # 历史数据年份：2013-2023年
    male_population = np.array([70063, 70522, 70857, 71307, 71650, 71864, 72039,
                 72357, 72311, 72206, 72032])
    female_population = np.array([66663, 67124, 67469, 67925, 68361, 68677,
                   68969, 68855, 68949, 68969, 68935])
    predict_len = 5  # 预测未来5年

    # 分别计算两种模型的预测结果
    # GM(1,1) + AR(1) 残差修正
    male_final_pred, male_gm_pred, male_res_pred = gm11_with_residual_correction(male_population, predict_len)
    female_final_pred, female_gm_pred, female_res_pred = gm11_with_residual_correction(female_population, predict_len)

    # 计算历史区间评价指标（仅计算原GM和改进模型在历史数据上的表现）
    male_gm_C = posterior_error_ratio(male_population, male_gm_pred[:len(male_population)])
    male_final_C = posterior_error_ratio(male_population, male_final_pred[:len(male_population)])
    female_gm_C = posterior_error_ratio(female_population, female_gm_pred[:len(female_population)])
    female_final_C = posterior_error_ratio(female_population, female_final_pred[:len(female_population)])

    male_gm_mape = calculate_metrics(male_population, male_gm_pred[:len(male_population)])
    male_final_mape = calculate_metrics(male_population,
                                                                         male_final_pred[:len(male_population)])
    female_gm_mape = calculate_metrics(female_population,
                                                                      female_gm_pred[:len(female_population)])
    female_final_mape = calculate_metrics(female_population, female_final_pred[
                                                                                                  :len(
                                                                                                      female_population)])

    # 输出各项评价指标
    print("男性 GM(1,1) 模型:")
    print(f"  后验差值比: {male_gm_C:.4f}, MAPE: {male_gm_mape:.2f}%")
    print("男性 GM+AR(1) 模型:")
    print(
        f"  后验差值比: {male_final_C:.4f}, MAPE: {male_final_mape:.2f}%")
    print("女性 GM(1,1) 模型:")
    print(
        f"  后验差值比: {female_gm_C:.4f}, MAPE: {female_gm_mape:.2f}%")
    print("女性 GM+AR(1) 模型:")
    print(
        f"  后验差值比: {female_final_C:.4f}, MAPE: {female_final_mape:.2f}%")

    # 构造完整的年份数组（历史 + 预测）
    years_pred = np.arange(years[0], years[-1] + predict_len + 1)
    # 计算性别比（男/女）：
    # 分别对 GM(1,1) 模型和 GM+AR(1) 模型计算性别比，其中预测结果长度一致
    ratio_gm = male_gm_pred / female_gm_pred
    ratio_final = male_final_pred / female_final_pred
    # 原始数据的性别比（仅历史数据）
    original_ratio = male_population / female_population

    # 绘图展示
    plt.figure(figsize=(12, 7))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # ------------------ Figure 1：男性、女性预测 ------------------
    fig1, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax_male, ax_female = axes

    # 男性子图
    ax_male.plot(years, male_population, 'bo-', label="历史男性人口")
    ax_male.plot(years_pred, male_gm_pred, 'b--', label="GM(1,1)预测 (男)")
    ax_male.plot(years_pred, male_final_pred, 'b:', label="GM+AR(1)预测 (男)")
    ax_male.set_ylabel("男性人口数")
    ax_male.set_title("男性人口预测")
    ax_male.grid(True)
    # 添加评价指标文本（以相对坐标显示在图内左上角）
    male_annotation = (
        "GM(1,1): C={:.4f}, MAPE={:.2f}%\n"
        "GM+AR(1): C={:.4f}, MAPE={:.2f}%"
            .format(male_gm_C, male_gm_mape,
                    male_final_C, male_final_mape)
    )
    ax_male.text(0.05, 0.95, male_annotation, transform=ax_male.transAxes,
                 fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))
    # 将图例放在右侧
    ax_male.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    # 女性子图
    ax_female.plot(years, female_population, 'ro-', label="历史女性人口")
    ax_female.plot(years_pred, female_gm_pred, 'r--', label="GM(1,1)预测 (女)")
    ax_female.plot(years_pred, female_final_pred, 'r:', label="GM+AR(1)预测 (女)")
    ax_female.set_xlabel("年份")
    ax_female.set_ylabel("女性人口数")
    ax_female.set_title("女性人口预测")
    ax_female.grid(True)
    # 添加评价指标文本
    female_annotation = (
        "GM(1,1): C={:.4f}, MAPE={:.2f}%\n"
        "GM+AR(1): C={:.4f}, MAPE={:.2f}%"
            .format(female_gm_C, female_gm_mape,
                    female_final_C, female_final_mape)
    )
    ax_female.text(0.05, 0.95, female_annotation, transform=ax_female.transAxes,
                   fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6))
    ax_female.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    plt.tight_layout()
    plt.show()

    # ------------------ Figure 2：性别比预测 ------------------
    fig2, ax_ratio = plt.subplots(figsize=(10, 5))
    # 绘制原始数据性别比（仅历史数据）
    ax_ratio.plot(years, original_ratio, 'ko-', label="原始数据 性别比", markersize=6)
    # 绘制预测模型的性别比
    ax_ratio.plot(years_pred, ratio_gm, 'k--', label="GM(1,1) 性别比", linewidth=2)
    ax_ratio.plot(years_pred, ratio_final, 'k:', label="GM+AR(1) 性别比", linewidth=2)
    ax_ratio.set_xlabel("年份")
    ax_ratio.set_ylabel("性别比 (男/女)")
    ax_ratio.set_title("性别比预测")
    ax_ratio.grid(True)
    # 图例放右侧
    ax_ratio.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

    plt.tight_layout()
    plt.show()