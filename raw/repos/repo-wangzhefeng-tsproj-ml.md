---
source_type: repo
source_url: https://github.com/wangzhefeng/tsproj_ml
source_local_path: raw/repos/tsproj_ml
created_at: 2026-04-05
updated_at: 2026-04-12
topics:
  - 时间序列预测
  - machine-learning-forecasting
related_concepts:
  - 机器学习时间序列预测
  - 预测特征工程
  - 机器学习时间序列多步预测策略
status: summarized
---

# tsproj_ml 仓库入口笔记

## 仓库信息

- 仓库名：`tsproj_ml`
- 仓库地址：https://github.com/wangzhefeng/tsproj_ml
- 本地路径：`raw/repos/tsproj_ml`
- README 入口：`README.md`（本地仓库包含完整文档）
- 主要用途：围绕机器学习模型构建时间序列预测的训练、测试、预测闭环，并系统比较多种多步预测策略。
- 代码框架：`tsproj_ml_mvp/` 目录包含主要的实现代码，支持7种预测策略（USMDO, USMD, USMR, USMDR, MSMD, MSMR, MSMDR）。

## 仓库要解决的问题

- 如何把机器学习模型系统化地用于时间序列预测，而不是只写一个零散 demo。
- 如何在单变量/多变量、直接/递归/混合多步预测之间做清晰的方法选择。
- 如何把特征工程、模型训练、测试验证和预测输出组织成可复用流程。

## 关键入口

- 仓库总入口：`README.md` - 包含完整的7种预测方法说明、决策树、实现checklist和性能对比
- 主要代码入口：`tsproj_ml_mvp/main.py` - 主程序入口
- 运行脚本：
  - `tsproj_ml_mvp/run_model_benchmarks.py` - 模型基准测试
  - `tsproj_ml_mvp/run_single_method.py` - 单方法运行
  - `run.py` - 根目录运行脚本
  - `main.py` - 根目录主程序

## 关键目录与素材

### 核心代码结构（tsproj_ml_mvp/）
- `config/` - 配置管理
  - `model_config.py` - 模型配置类
- `data_provider/` - 数据加载与处理
  - `data_loader.py` - 数据加载
  - `outlier_process.py` - 异常值处理
- `features/` - 特征工程
  - `FeatureEngineering.py` - 特征工程主类
  - `FeatureScalering.py` - 特征缩放
  - `FeatureSelection.py` - 特征选择
  - `DataAugment.py` - 数据增强
- `models/` - 模型实现
  - `ModelFactory.py` - 模型工厂
  - `ModelTesting.py` - 模型测试
  - `ModelEnsemble.py` - 模型集成
- `strategies/` - 预测策略
  - `PredictionStrategy.py` - 预测策略实现（超过600行代码，包含7种策略的具体实现）

### 文档与资源
- `README.md` - 完整的技术文档，包含7种预测方法的详细说明、特征构成、训练过程、优缺点分析
- `docs/` - 文档目录，包含示意图和详细说明
- `config/` - 根目录配置，包含默认配置文件

## 核心预测策略体系

仓库实现了7种机器学习时间序列预测方法：

1. **USMDO** - 单变量多步直接输出预测（仅使用外生变量）
2. **USMD** - 单变量多步直接预测（目标变量滞后+外生变量）
3. **USMR** - 单变量多步递归预测
4. **USMDR** - 单变量多步直接递归预测（分块递归）
5. **MSMD** - 多变量多步直接预测 ⭐（重点修复）
6. **MSMR** - 多变量多步递归预测
7. **MSMDR** - 多变量多步直接递归预测

每种方法在README中都有详细说明，包括：
- 特征构成（代码示例）
- 目标构成
- 训练过程
- 预测过程
- 优点/缺点
- 适用场景
- 与相关方法的区别

## 技术特点

1. **模块化设计**：配置、数据、特征、模型、策略分离，便于维护和扩展
2. **多策略支持**：完整覆盖单变量/多变量、直接/递归/混合预测策略
3. **特征工程丰富**：时间特征、滞后特征、外生变量、多变量滞后特征
4. **工程化实现**：包含模型持久化、测试验证、基准测试等完整功能
5. **决策支持**：提供方法选择决策树和具体场景推荐策略

## 建议拆分的知识单元

1. **预测策略体系与决策方法**
   - 7种预测方法的核心思想与适用场景对比
   - 方法选择决策树与场景推荐策略
   - 不同策略的特征构成与目标构成差异

2. **特征工程与数据预处理**
   - 时间特征构造（周期性编码、节假日标记等）
   - 滞后特征设计（单变量与多变量滞后）
   - 外生变量集成与特征缩放
   - 异常值处理与数据增强

3. **模型训练与评估框架**
   - 统一的模型接口与配置管理
   - MultiOutputRegressor多输出训练模式
   - 模型测试、集成与持久化
   - 基准测试与性能对比方法

4. **预测策略实现细节**
   - 直接预测、递归预测、分块递归的实现差异
   - 多变量预测的特征构造与目标组织
   - 预测过程中的历史更新与误差控制

## 首轮判断

- 该仓库内容非常丰富，涵盖了机器学习时间序列预测的完整方法论和工程实现。
- 首轮已经建立了3个核心知识单元的来源卡，覆盖了策略体系、特征工程和训练闭环。
- 现在有了本地仓库，可以进一步深入源码级分析，特别是`PredictionStrategy.py`中7种策略的具体实现。
- 建议后续可以针对每种预测策略进行更详细的源码分析和案例研究。
