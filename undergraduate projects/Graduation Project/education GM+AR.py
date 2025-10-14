import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg  # statsmodels>=0.12.0


def gm11(x0, predict_step=3):
    """
    与之前相同的 GM(1,1) 实现
    """
    x0 = np.array(x0, dtype=float)
    n = len(x0)
    x1 = np.cumsum(x0)
    z1 = (x1[:-1] + x1[1:]) / 2.0
    B = np.column_stack([-z1, np.ones(n - 1)])
    Y = x0[1:].reshape(-1, 1)
    AB = np.linalg.inv(B.T @ B) @ B.T @ Y
    a, b = AB[0, 0], AB[1, 0]

    def x1_hat(k):
        return (x1[0] - b / a) * np.exp(-a * (k - 1)) + b / a

    x0_hat = [x0[0]]
    for k in range(2, n + 1):
        x0_hat.append(x1_hat(k) - x1_hat(k - 1))
    x0_hat = np.array(x0_hat)

    forecast = []
    for i in range(1, predict_step + 1):
        forecast_val = x1_hat(n + i) - x1_hat(n + i - 1)
        forecast.append(forecast_val)
    forecast = np.array(forecast)

    return x0_hat, forecast, a, b


def mape(true, pred):
    """
    计算 MAPE
    """
    true, pred = np.array(true), np.array(pred)
    mask = (true != 0)
    return np.mean(np.abs((true[mask] - pred[mask]) / true[mask])) * 100


def posterior_error_ratio(true, fitted):
    """
    计算后验差值比
    """
    residual = true - fitted
    std_res = np.std(residual, ddof=1)
    std_true = np.std(true, ddof=1)
    return std_res / std_true if std_true != 0 else np.nan


def fit_ar_model_auto(residual, maxlag=3):
    """
    利用 statsmodels.AutoReg 自动选择最优滞后阶数 (<= maxlag)，基于 AIC
    返回：模型对象及最优滞后阶数
    """
    best_aic = np.inf
    best_lag = 0
    best_model = None
    # 遍历 1 到 maxlag，选 AIC 最小者
    for lag in range(1, maxlag + 1):
        # 为防止样本过少产生溢出，需要判断 residual 长度
        if len(residual) <= lag:
            break
        try:
            model = AutoReg(residual, lags=lag, trend='c', old_names=False).fit()
            if model.aic < best_aic:
                best_aic = model.aic
                best_lag = lag
                best_model = model
        except:
            pass
    return best_model, best_lag


def forecast_ar_model(model, steps=3):
    """
    利用拟合的 AutoReg 模型进行未来 steps 步预测
    """
    if model is None:
        return np.zeros(steps)
    forecast_res = model.predict(start=len(model.model.endog), end=len(model.model.endog) + steps - 1, dynamic=True)
    return forecast_res


# ---------------------------
# 主流程：GM(1,1) + AR(p) ，p<=3 自适应阶数
if __name__ == "__main__":
    # 示例：假设我们有多个受教育程度的数据
    years = np.array([2013, 2014, 2016, 2017, 2018, 2019, 2021, 2022, 2023])
    data_dict = {

        "6岁及6岁以上未上过学人口数": [52010, 56255, 61448, 56152, 57483, 51892, 51186, 51393, 55292],
        "6岁及6岁以上小学人口数": [274658, 274858, 275939, 268406, 268951,
                     257030, 365918, 355354, 350424],
        "6岁及6岁以上初中人口数": [425144, 420432, 418395, 404872, 401864,
                     379039, 487144, 467993, 511117],
        "6岁及6岁以上高中人口数": [172088, 174847, 182171, 186735, 186794,
                     180285, 233626, 222881, 221678],
        "6岁及6岁以上大专及以上人口数": [117925, 120698, 139370, 147593, 149104,
                        148170, 264467, 265414, 270529],
    }
    predict_step = 5
    future_years = np.arange(years[-1] + 1, years[-1] + 1 + predict_step)

    results = {}

    for category, data in data_dict.items():
        data_arr = np.array(data, dtype=float)
        # 1. GM(1,1) 拟合
        gm_fitted, gm_forecast, a, b = gm11(data_arr, predict_step=predict_step)
        gm_residual = data_arr - gm_fitted

        # 2. 自动选择 AR(p) (p<=3)
        model_ar, best_lag = fit_ar_model_auto(gm_residual, maxlag=3)

        # 样本内残差拟合
        if model_ar is not None:
            # in-sample prediction (仅从 lag 后开始有值)
            # 这里为了简化，可用 model_ar.fittedvalues 作为样本内残差预测
            ar_insample = model_ar.fittedvalues
            # ar_insample 与 gm_residual 的长度可能不同，需要对齐（AutoReg略有差异）
            offset = len(gm_residual) - len(ar_insample)
            # 填充开头 offset 个残差为原始值
            ar2_fitted = np.concatenate([gm_residual[:offset], ar_insample])
        else:
            # 如果样本太短未成功拟合，就置为 0
            ar2_fitted = np.zeros_like(gm_residual)

        # 改进后的历史拟合
        improved_fitted = gm_fitted + ar2_fitted

        # 3. 未来残差预测
        ar_forecast_vals = forecast_ar_model(model_ar, steps=predict_step)
        improved_forecast = gm_forecast + ar_forecast_vals

        # 4. 评价指标
        gm_post = posterior_error_ratio(data_arr, gm_fitted)
        gm_m = mape(data_arr, gm_fitted)
        improved_post = posterior_error_ratio(data_arr, improved_fitted)
        improved_m = mape(data_arr, improved_fitted)

        results[category] = {
            "data": data_arr,
            "gm_fitted": gm_fitted,
            "gm_forecast": gm_forecast,
            "improved_fitted": improved_fitted,
            "improved_forecast": improved_forecast,
            "best_ar_lag": best_lag,
            "gm_posterior": gm_post,
            "gm_mape": gm_m,
            "improved_posterior": improved_post,
            "improved_mape": improved_m
        }

    # 绘图
    plt.figure(figsize=(12, 8))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    color_list = ['b', 'g', 'r', 'c', 'm', 'orange']
    for i, (cat, res) in enumerate(results.items()):
        all_years = np.concatenate([years, future_years])
        improved_full = np.concatenate([res["improved_fitted"], res["improved_forecast"]])
        plt.plot(years, res["data"], 'o', color=color_list[i], label=f"{cat} 实际")
        plt.plot(all_years, improved_full, '-', color=color_list[i],
                 label=(f"{cat} 改进(AR({res['best_ar_lag']}))\n"
                        f"后验比={res['improved_posterior']:.3f}, MAPE={res['improved_mape']:.2f}%"))
    plt.xlabel("年份")
    plt.ylabel("人口数（人）")
    plt.title("GM(1,1) + 自适应 AR(p) 改进模型预测结果")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 打印结果
    for cat, res in results.items():
        print(f"【{cat}】最佳 AR 滞后阶数: {res['best_ar_lag']}")
        print(f"  GM(1,1): 后验比={res['gm_posterior']:.3f}, MAPE={res['gm_mape']:.2f}%")
        print(f"  改进后:   后验比={res['improved_posterior']:.3f}, MAPE={res['improved_mape']:.2f}%")
        print("  预测结果（改进后）:")
        df_pred = pd.DataFrame({
            "Year": np.concatenate([years, future_years]),
            "Prediction": np.concatenate([res["improved_fitted"], res["improved_forecast"]]).round(2)
        })
        print(df_pred)
        print("-" * 40)
