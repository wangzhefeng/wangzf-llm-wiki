---
source_type: notes
created_at: 2026-04-21
topics:
  - reinforcement-learning
status: inbox
---

# MORL 精细化实现：交付报告

> **上下文**：在基础调研文档的基础上，对虚拟电厂 (VPP) 多目标强化学习的环境模型与数据生成做工业级细化，并用 MILP Oracle 建立性能基准。

---

## 1. 交付清单

### 数据层
| 文件 | 说明 | 规模 |
|---|---|---|
| `realistic_data_generator.py` | 一年 15-min VPP 时序数据生成器 | 500 行代码 |
| `vpp_year_dataset.csv` | 生成的一年数据（2024 全年） | 35,040 行 × 25 列 |
| `visualize_dataset.py` | 数据质量诊断脚本 | — |
| `fig1_typical_days.png` | 夏冬典型日曲线 | — |
| `fig2_heatmap.png` | 全年 月 × 时 热力图 | — |
| `fig3_price_distribution.png` | 价格分布与 Q-Q 图 | — |
| `fig4_statistics.png` | ACF、预测误差、季节性 | — |

### 环境层
| 文件 | 说明 |
|---|---|
| `refined_vpp_env.py` | 精细 VPP MOMDP 环境 |

### 算法层
| 文件 | 说明 |
|---|---|
| `numpy_envelope_demo.py` | **沙箱可运行**的纯 NumPy Envelope Q-Learning 表格实现 |
| `train_envelope_vpp.py` | **生产级** MORL-Baselines + PyTorch 训练脚本（本地 GPU 运行） |

### 评估层
| 文件 | 说明 |
|---|---|
| `milp_oracle.py` | MILP Oracle 基线（ε-约束法生成真实 Pareto 前沿） |
| `visualize_policy_behavior.py` | 同一天多偏好策略对比可视化 |
| `final_benchmark.py` | MORL vs MILP vs 规则基线综合对比 |
| `fig5_policy_behavior.png` | 4 面板：SOC、电池出力、净功率、累计收益 |
| `fig6_pareto_scatter.png` | 策略空间在目标空间的投影 |
| `fig7_milp_pareto.png` | MILP Oracle 的 3D + 2D Pareto 前沿 |
| `fig8_final_comparison.png` | **最终综合对比图** |
| `pareto_approximation.csv`, `final_benchmark.csv` | 量化结果表 |

---

## 2. 数据真实性验证

生成的数据在以下维度已贴近中国现货市场真实特征：

| 特征 | 生成数据 | 真实市场参考 |
|---|---|---|
| 日均电价 | 0.378 ± 0.266 ¥/kWh | 山东/山西 0.3-0.5 |
| 负价占比 | 0.53% | 山东 2024 ~ 1-3% |
| 尖峰 (>1¥) 占比 | 0.95% | 夏季高峰月典型 1-2% |
| 价格偏度 | 0.89（右偏重尾） | 现货典型重尾分布 |
| 自相关 | 15-min 强相关，96-步周期峰 | 日内 TOU 模式 |
| PV 容量因子 | 0.165 | 华东/华南 0.13-0.18 |
| 负荷率 | 0.46 | 典型工商业 0.4-0.6 |
| 碳 EF 均值 | 0.52 kg/kWh | 中国电网平均 0.5-0.6 |

---

## 3. 环境精细化项

相对基础版本的核心改进：

**(a) 电池退化模型 — DoD 加权循环**

$$
\text{cycle\_loss} = \frac{0.5 \cdot |\Delta\text{SOC}|^{1.8}}{\text{CycleLife}_{\text{100\%DoD}}}
$$

指数 1.8 反映深放对寿命的非线性加速。加上日历老化：

$$
\text{total\_loss} = \text{cycle\_loss} + \frac{\text{calendar\_loss\_per\_year}}{\text{steps\_per\_year}}
$$

最终货币化为退化成本：

$$
\text{Cost}_{\text{deg}} = \text{total\_loss} \cdot E_{\text{cap}} \cdot \text{CAPEX}_{/kWh}
$$

**(b) 物理约束**
- SOC 硬约束通过**动作裁剪**实现（充/放电功率自动限制）；
- 爬坡约束：$|P^{\text{batt}}_t - P^{\text{batt}}_{t-1}| \leq R_{\max}$；
- 充放电互斥（通过 MILP 的二进制变量，RL 环境通过动作空间设计）；
- 电网联络线限值。

**(c) 风险目标 — 滚动 CVaR**

用滑动窗口 $W$（默认 24 步 = 6 小时）内的负收益 $\alpha$ 分位数及其条件期望：

$$
\text{CVaR}_\alpha = \mathbb{E}[L | L \geq \text{VaR}_\alpha], \quad L = \{-r_t | r_t < 0\}
$$

这比简单的方差更适合刻画"尾部风险"——对应电力交易中极端亏损日的担忧。

**(d) 状态特征升级**
- 三变量 × 3 预测视野（15min / 1h / 4h）；
- 每变量的"预测不确定性代理"$\sigma$；
- 滚动 6 步价格均值与标准差；
- 正弦/余弦时间编码替代线性 `t/T`。

**(e) 奖励向量扩展至 4 维**
`[收益, -碳成本, -退化, -风险]`，完整刻画 VPP 运营的关键权衡。

---

## 4. 性能对比（2024-07-15 夏季典型日）

在"**纯收益最大化**"目标下：

| 方法 | 收益 (¥) | 相对 MILP |
|---|---|---|
| MILP Oracle（完美信息上界） | **+23.66** | 100% |
| TOU 规则基线 | -81.69 | — |
| MORL（本沙箱表格法，500 ep） | -267.17 | 13.5% 回收率 |
| 不调度电池 | -312.53 | 0% |

**坦诚的解读**：

1. **MILP Oracle 是不可达上界**——它假设完美预见未来 96 步。现实中任何在线策略都低于此。
2. **TOU 规则在该日表现优异**——因为数据 TOU 结构强。真实场景（含尖峰、随机事件）规则会失效。
3. **MORL 表格版的低回收率主要源于实现粗糙**：
   - 22 维连续观察被离散化到 5 维桶 → 严重信息损失；
   - 仅 500 episodes 训练（约 48k 步）远少于工业标准（300k+）；
   - 无神经网络泛化。
4. **生产级预期**：使用 `train_envelope_vpp.py` 中的 MLP + 300k 步训练，学界论文报告的 **回收率通常在 70-90%**。

**MORL 的真正价值不在"单偏好超越 MILP"**，而在于：
- 单一模型支持 N 个偏好（MILP 要跑 N 次）；
- 毫秒级推断（MILP 每次数秒到数分钟）；
- 对不确定性鲁棒（MILP 鲁棒化代价极高）；
- 跨日泛化（MILP 需重构建模）。

---

## 5. 推荐生产部署路线

**阶段 1 — 离线预训练（1-2 周）**

1. 用 MILP Oracle 在历史数据上生成"完美信息"专家轨迹；
2. 行为克隆 (BC) 初始化 Envelope Q 网络；
3. 验证：BC 后策略的收益 ≥ TOU 规则。

**阶段 2 — 在线微调（2-4 周）**

1. 部署 MO-Gymnasium 封装的真实环境；
2. Envelope Q-Learning 在历史 + 仿真数据上训练；
3. 验证集超体积指标（HV）随训练步数单调增长。

**阶段 3 — 生产部署（持续）**

1. **MILP 作为安全层**：MORL 输出动作 → MILP 做单步投影 → 确保 SOC、联络线硬约束；
2. **业务 UI**：权重滑块（经济/碳/寿命/风险）代替代码修改；
3. **持续学习**：每月用最新数据微调模型，应对市场规则/补贴/碳价变化；
4. **监控**：记录实际收益、每日偏好选择与 Pareto 点映射的漂移。

---

## 6. 关键代码片段索引

**数据生成核心**（`realistic_data_generator.py`）：
- `_simulate_cloud_factor()` — 二级 Markov 链天气
- `_clear_sky_pv()` — 简化天文模型
- `generate_vpp_dataset()` — 主函数，整合所有组件
- `add_forecast_columns()` — 滚动预测误差（误差随视野对数增长）

**环境核心**（`refined_vpp_env.py`）：
- `_apply_soc_constraints()` — 物理约束裁剪
- `_compute_degradation_cost()` — DoD 加权退化
- `_compute_risk_cost()` — 滚动 CVaR
- `_build_obs()` — 22 维观察

**算法核心**（`numpy_envelope_demo.py`）：
- `_envelope_target()` — Envelope 操作的 NumPy 实现
- `update()` — 向量 TD 更新

**MILP Oracle**（`milp_oracle.py`）：
- `solve_milp()` — 单次 MILP 求解（支持单目标/加权/ε-约束三种模式）
- `generate_pareto_front()` — ε-约束网格扫描 + 非支配过滤

---

## 7. 后续工作建议

1. **替换为神经网络 Envelope**：将 `numpy_envelope_demo.py` 迁移到 `morl-baselines` + PyTorch；
2. **多智能体 MORL**：用 MO-MADDPG 处理多 VPP 联合投标；
3. **偏好推断**：基于运营人员历史选择推断隐式偏好（逆 MORL）；
4. **真实预测接入**：替换合成预测为实际的 LightGBM / Transformer 预测输出；
5. **约束 MORL (CMORL)**：用对偶方法处理碳配额、偏差罚款等硬约束。
