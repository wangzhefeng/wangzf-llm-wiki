"""
realistic_data_generator.py
===========================
生成贴近中国电力现货市场真实特征的 VPP 时序数据集。

覆盖 1 年 × 15 min 分辨率（共 35040 点），包含：
- 节点边际电价 (LMP, ¥/kWh): 具备 TOU、残差负荷响应、AR(1) 自相关、Poisson 尖峰、周末折价、季节性
- 分布式光伏出力 (kW): 基于简化天文日照模型 + Markov 链云量 + 尺度季节性
- 用户负荷 (kW): 双峰日模式 + 周末差异 + 温度敏感项 + AR(1) 扰动
- 边际电网排放因子 (kgCO2/kWh): 随残差负荷变化，体现"中午低、晚间高"
- 温度序列 (°C): 正弦季节 + 日内波动（供 EF 和 Load 耦合）
- 预测序列：对每个时刻生成滚动的 1h/4h/24h 预测值（含随预测视野增长的误差）

设计参考（公开资料）：
- 山东/山西现货市场 TOU 结构与尖峰分布特征
- 典型工商业用户日负荷曲线（IEC 61853 / 国标 GB/T 31464）
- NASA POWER / CWEC 气象数据的统计特征
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple


# ======================================================================
# 核心配置
# ======================================================================
@dataclass
class DataConfig:
    # 时间
    start_date: str = "2024-01-01"
    n_days: int = 365
    freq_min: int = 15                 # 15-min 分辨率
    # 系统规模
    pv_capacity_kw: float = 120.0
    load_peak_kw: float = 100.0
    # 电价
    price_base: float = 0.35           # ¥/kWh, 基准电价
    price_peak_mult: float = 2.2       # 尖峰段倍率
    price_valley_mult: float = 0.35    # 低谷段倍率
    # 碳
    ef_coal: float = 0.85              # kg/kWh, 边际煤电
    ef_gas: float = 0.42               # 边际气电
    ef_re: float = 0.0                 # 可再生
    # 随机性
    seed: int = 42
    # AR 参数
    price_ar_rho: float = 0.72         # 价格 AR(1) 系数
    load_ar_rho: float = 0.85          # 负荷 AR(1) 系数
    # 尖峰事件
    spike_lambda_per_day: float = 0.15 # 每日尖峰事件强度（Poisson λ）
    spike_mult_lognormal_mu: float = 1.0
    spike_mult_lognormal_sigma: float = 0.3
    # 季节性
    summer_peak_day: int = 200         # 7 月下旬，一年中最热
    winter_peak_day: int = 20          # 1 月下旬，最冷


# ======================================================================
# 工具函数
# ======================================================================
def _seasonal(day_of_year: np.ndarray, peak_day: int, amplitude: float) -> np.ndarray:
    """一年一次的余弦季节信号，peak_day 为峰值日。"""
    return amplitude * np.cos(2 * np.pi * (day_of_year - peak_day) / 365.25)


def _clear_sky_pv(hour_of_day: np.ndarray, day_of_year: np.ndarray,
                  capacity: float) -> np.ndarray:
    """
    简化晴空 PV 出力模型（中国华东纬度 ≈ 30°N）。
    - 日内：sin² 型，仅 6:00-18:00 有输出
    - 季节性：夏季峰值约为冬季 1.3 倍
    """
    solar_elevation = np.maximum(
        0.0,
        np.sin(np.pi * (hour_of_day - 6) / 12)
    )
    # 季节强度: 夏高冬低
    day_angle = 2 * np.pi * (day_of_year - 172) / 365.25  # 172 = 夏至
    seasonal_strength = 1.0 + 0.15 * np.cos(day_angle)
    # 空气质量系数（简化，冬季雾霾更多→略低）
    aq = 0.95 + 0.05 * np.cos(day_angle)
    clear_sky = capacity * (solar_elevation ** 1.2) * seasonal_strength * aq
    return np.clip(clear_sky, 0, capacity)


def _simulate_cloud_factor(n_steps: int, steps_per_day: int,
                           rng: np.random.Generator) -> np.ndarray:
    """
    用两级 Markov 链生成云量因子（0=全阴到 1=晴朗）。
    日间云量有持续性：晴→晴概率高，阴→阴概率高。
    """
    n_days = n_steps // steps_per_day + 1
    # 每天的天气类型：晴(0)/多云(1)/阴(2)
    trans = np.array([
        [0.70, 0.25, 0.05],
        [0.30, 0.50, 0.20],
        [0.15, 0.40, 0.45],
    ])
    state = 0
    daily_states = []
    for _ in range(n_days):
        daily_states.append(state)
        state = rng.choice(3, p=trans[state])
    daily_states = np.array(daily_states)

    # 每天内的云量：晴 Beta(5,1) 均值 0.83，多云 Beta(2,2) 均值 0.5，阴 Beta(1,5) 均值 0.17
    factors = np.zeros(n_steps)
    for d in range(n_days):
        start, end = d * steps_per_day, min((d + 1) * steps_per_day, n_steps)
        s = daily_states[d]
        if s == 0:
            base = rng.beta(5, 1)
            noise_std = 0.05
        elif s == 1:
            base = rng.beta(2, 2)
            noise_std = 0.12
        else:
            base = rng.beta(1, 5)
            noise_std = 0.15
        # 日内缓慢变化 + 白噪声
        day_len = end - start
        if day_len <= 0:
            continue
        slow = 0.1 * np.sin(np.linspace(0, 2 * np.pi, day_len)) + base
        noise = rng.normal(0, noise_std, day_len)
        factors[start:end] = np.clip(slow + noise, 0.0, 1.0)
    return factors[:n_steps]


def _ar1_process(n: int, rho: float, sigma: float,
                 rng: np.random.Generator) -> np.ndarray:
    """生成 AR(1) 平稳随机扰动。"""
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + rng.normal(0, sigma)
    return x


# ======================================================================
# 主生成函数
# ======================================================================
def generate_vpp_dataset(cfg: DataConfig = None) -> pd.DataFrame:
    """生成一年 VPP 场景的 15-min 数据。"""
    if cfg is None:
        cfg = DataConfig()

    rng = np.random.default_rng(cfg.seed)

    steps_per_day = int(24 * 60 / cfg.freq_min)
    n_steps = cfg.n_days * steps_per_day

    # 时间轴
    ts = pd.date_range(
        start=cfg.start_date, periods=n_steps,
        freq=f"{cfg.freq_min}min"
    )
    doy = ts.day_of_year.values.astype(float)
    hod = ts.hour.values + ts.minute.values / 60.0
    dow = ts.day_of_week.values  # Mon=0 ... Sun=6
    is_weekend = (dow >= 5).astype(float)

    # --------------------------------------------------------------
    # 1. 温度 (°C): 正弦季节 + 日内温差
    # --------------------------------------------------------------
    seasonal_temp = 15.0 + 15.0 * (
        -np.cos(2 * np.pi * (doy - cfg.winter_peak_day) / 365.25)
    )  # 冬季最低约 0°C，夏季最高约 30°C
    diurnal_temp = 4.0 * np.sin(2 * np.pi * (hod - 14) / 24)  # 14 点最热
    temp_noise = _ar1_process(n_steps, 0.9, 0.8, rng)
    temperature = seasonal_temp + diurnal_temp + temp_noise

    # --------------------------------------------------------------
    # 2. PV 出力
    # --------------------------------------------------------------
    clear_sky = _clear_sky_pv(hod, doy, cfg.pv_capacity_kw)
    cloud_factor = _simulate_cloud_factor(n_steps, steps_per_day, rng)
    # 日内快速扰动（云团遮挡）
    fast_noise = rng.normal(0, 0.03, n_steps) * (clear_sky > 0)
    pv_actual = clear_sky * cloud_factor + cfg.pv_capacity_kw * fast_noise
    pv_actual = np.clip(pv_actual, 0, cfg.pv_capacity_kw)

    # --------------------------------------------------------------
    # 3. 用户负荷 (kW): 形态 = 基准日形 × 季节 × 工作日修正 + 温度响应 + 噪声
    # --------------------------------------------------------------
    # 基准工作日双峰
    base_load = (
        30.0
        + 20.0 * np.exp(-((hod - 8.5) ** 2) / 4.0)   # 早峰
        + 35.0 * np.exp(-((hod - 19.5) ** 2) / 3.0)  # 晚峰
        + 10.0 * (hod > 8) * (hod < 22)              # 白天基础抬升
    )
    # 周末：早峰减弱，晚峰后延
    weekend_adjust = np.where(
        is_weekend > 0,
        0.85 + 0.10 * np.exp(-((hod - 21.0) ** 2) / 5.0),
        1.0,
    )
    # 温度响应：>26°C 制冷，<8°C 制热
    cooling = np.maximum(0, temperature - 26) * 1.8   # kW/°C
    heating = np.maximum(0, 8 - temperature) * 1.2
    thermal_load = cooling + heating
    # AR(1) 随机扰动
    load_noise = _ar1_process(n_steps, cfg.load_ar_rho, 2.5, rng)
    load = base_load * weekend_adjust + thermal_load + load_noise
    load = np.clip(load, 20.0, cfg.load_peak_kw * 1.3)

    # --------------------------------------------------------------
    # 4. 残差负荷 (决定电价和 EF)
    # --------------------------------------------------------------
    # 系统层残差负荷 = 系统总负荷 - 系统总可再生
    # 这里用 VPP 层作为代理，并放大到系统尺度
    residual = load - pv_actual  # 单个 VPP 的净购电需求

    # --------------------------------------------------------------
    # 5. 电价 (¥/kWh)
    #    = 基准 × TOU × 残差响应 × 季节 × 周末 + AR 噪声 + 尖峰
    # --------------------------------------------------------------
    # (a) TOU 乘子
    tou = np.ones(n_steps)
    # 早峰 8-11
    mask_peak_morning = (hod >= 8) & (hod < 11)
    # 晚峰 18-22
    mask_peak_evening = (hod >= 18) & (hod < 22)
    # 低谷 23-7
    mask_valley = (hod >= 23) | (hod < 7)
    # 平段为默认 1.0
    tou[mask_peak_morning] = 1.6
    tou[mask_peak_evening] = cfg.price_peak_mult
    tou[mask_valley] = cfg.price_valley_mult

    # (b) 残差负荷敏感性（归一化到 [-1, 1]）
    resid_norm = (residual - np.median(residual)) / (np.std(residual) + 1e-6)
    resid_sensitivity = 0.12 * np.tanh(resid_norm)  # ±12% 波动

    # (c) 季节：夏冬高，春秋低
    seasonal_price = 0.08 * np.abs(np.cos(2 * np.pi * (doy - cfg.summer_peak_day) / 365.25))
    seasonal_price += 0.05 * (-np.cos(2 * np.pi * (doy - cfg.winter_peak_day) / 365.25))

    # (d) 周末折价 ~15%
    weekend_price = np.where(is_weekend > 0, 0.88, 1.0)

    # (e) AR(1) 噪声
    price_noise = _ar1_process(n_steps, cfg.price_ar_rho, 0.04, rng)

    # (f) 尖峰事件（Poisson 到达，LogNormal 幅值，持续 2-6 步）
    n_days = cfg.n_days
    spikes = np.zeros(n_steps)
    for d in range(n_days):
        n_events = rng.poisson(cfg.spike_lambda_per_day)
        for _ in range(n_events):
            t_spike = d * steps_per_day + rng.integers(32, steps_per_day - 4)  # 8 AM 之后
            mult = rng.lognormal(cfg.spike_mult_lognormal_mu, cfg.spike_mult_lognormal_sigma)
            # 持续时间
            dur = rng.integers(2, 7)
            for k in range(dur):
                if t_spike + k < n_steps:
                    decay = np.exp(-k / 3.0)
                    spikes[t_spike + k] += (mult - 1.0) * decay

    price = (cfg.price_base
             * tou
             * (1 + resid_sensitivity)
             * (1 + seasonal_price)
             * weekend_price
             + price_noise
             + cfg.price_base * spikes)

    # 允许极少数负价（高新能源 + 低负荷夜间）
    neg_price_mask = (pv_actual > 0.6 * cfg.pv_capacity_kw) & (load < 0.5 * cfg.load_peak_kw)
    price[neg_price_mask] -= rng.uniform(0.0, 0.15, neg_price_mask.sum())
    price = np.clip(price, -0.2, 3.5)  # 允许负价，封顶在 3.5

    # --------------------------------------------------------------
    # 6. 排放因子 (kg/kWh): 随残差负荷上升而接近煤电
    # --------------------------------------------------------------
    # 归一化残差到 [0, 1]
    resid_norm_01 = (residual - residual.min()) / (residual.max() - residual.min() + 1e-6)
    # 插值 煤-气-再生
    ef = (cfg.ef_re * (1 - resid_norm_01) ** 2
          + cfg.ef_gas * 2 * resid_norm_01 * (1 - resid_norm_01)
          + cfg.ef_coal * resid_norm_01 ** 2)
    # 白天稍低（光伏稀释），晚上稍高
    day_dilution = np.where((hod >= 10) & (hod <= 15), 0.85, 1.0)
    ef *= day_dilution
    ef = np.clip(ef, 0.15, 1.0)

    # --------------------------------------------------------------
    # 7. 组装 DataFrame
    # --------------------------------------------------------------
    df = pd.DataFrame({
        "timestamp": ts,
        "hour": hod,
        "day_of_week": dow,
        "is_weekend": is_weekend.astype(int),
        "day_of_year": doy.astype(int),
        "temperature_c": temperature.round(2),
        "pv_kw": pv_actual.round(2),
        "pv_clear_sky_kw": clear_sky.round(2),
        "cloud_factor": cloud_factor.round(3),
        "load_kw": load.round(2),
        "residual_load_kw": (load - pv_actual).round(2),
        "price_cny_per_kwh": price.round(4),
        "emission_factor_kg_per_kwh": ef.round(4),
    })
    return df


# ======================================================================
# 预测序列生成（用于状态特征）
# ======================================================================
def add_forecast_columns(df: pd.DataFrame,
                         horizons_minutes=(15, 60, 240, 1440),
                         seed: int = 999) -> pd.DataFrame:
    """
    为 price/pv/load 添加滚动预测列，预测误差满足：
    - 对 pv/load: 相对误差 σ 随视野对数增长 ~ 3% + 8% * log(h/15)
    - 对 price: 更难预测，基础 σ 更大
    预测 = 真实值 × (1 + ε)，其中 ε ~ Normal(bias, sigma)
    """
    rng = np.random.default_rng(seed)
    df = df.copy()

    for col, sigma_base, sigma_slope in [
        ("pv_kw",    0.03, 0.08),
        ("load_kw",  0.02, 0.05),
        ("price_cny_per_kwh", 0.05, 0.12),
    ]:
        values = df[col].values
        for h_min in horizons_minutes:
            k_steps = h_min // 15
            # 未来 h_min 分钟的真实值
            future = np.roll(values, -k_steps)
            future[-k_steps:] = values[-1]
            # 预测误差
            sigma = sigma_base + sigma_slope * np.log(max(h_min / 15.0, 1.0) + 1e-6)
            eps = rng.normal(0, sigma, len(values))
            forecast = future * (1 + eps)
            if col == "pv_kw":
                forecast = np.clip(forecast, 0, None)
            if col == "price_cny_per_kwh":
                forecast = np.clip(forecast, -0.2, 3.5)
            df[f"forecast_{col}_h{h_min}min"] = forecast.round(3)
    return df


# ======================================================================
# 命令行入口
# ======================================================================
if __name__ == "__main__":
    cfg = DataConfig(
        start_date="2024-01-01",
        n_days=365,
        freq_min=15,
        pv_capacity_kw=120.0,
        load_peak_kw=100.0,
        seed=42,
    )

    print("正在生成一年 VPP 数据...")
    df = generate_vpp_dataset(cfg)
    print(f"  基础数据: {df.shape}")

    df = add_forecast_columns(df, horizons_minutes=(15, 60, 240, 1440))
    print(f"  加入预测列后: {df.shape}")

    # 保存
    out_path = "/home/claude/morl_refined/vpp_year_dataset.csv"
    df.to_csv(out_path, index=False)
    print(f"  已保存到 {out_path}")

    # 打印统计
    print("\n=== 关键变量描述性统计 ===")
    summary = df[[
        "price_cny_per_kwh", "pv_kw", "load_kw",
        "emission_factor_kg_per_kwh", "temperature_c"
    ]].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).round(3)
    print(summary)

    print("\n=== 价格分布特征 ===")
    p = df["price_cny_per_kwh"]
    print(f"  负价占比:         {(p < 0).mean() * 100:.2f}%")
    print(f"  >1 ¥/kWh 占比:    {(p > 1.0).mean() * 100:.2f}%")
    print(f"  偏度 (skewness):  {p.skew():.3f}")
    print(f"  峰度 (kurtosis):  {p.kurtosis():.3f}")
