# Analysis-Framework

This is a data analysis framework that includes a set of common algorithms and standardized workflows. Users can customize and adjust algorithms, and toggle them on or off as needed, providing a flexible, modular approach to data processing tasks.

简体中文：
这是一个数据分析框架，包含一系列通用算法和标准化工作流程。用户可以根据需要自定义和调整算法，并可灵活地启用或禁用它们，从而为数据处理任务提供一种灵活、模块化的解决方案。

繁體中文：
這是一個資料分析框架，包含一系列通用演算法和標準化工作流程。使用者可以根據需求自訂與調整演算法，並可靈活地啟用或停用它們，從而為資料處理任務提供一種彈性、模組化的解決方案。

这是当前项目的本地版本说明。它描述的是仓库里已经完成并可运行的内容，不是未来规划稿。

## 项目现状

这个仓库现在已经是一个最小可运行的数据分析框架 `MVP`，支持：

- 读取 `CSV` 原始数据
- 通过配置文件定义分析流程
- 按步骤执行内置算法
- 输出处理后的数据文件
- 输出分析结果摘要 `JSON`
- 通过命令行运行、校验配置、查看算法列表

当前内置了 3 个算法：

1. `missing_values`
2. `descriptive_stats`
3. `correlation`

## 当前目录结构

```text
Analysis-Framework/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .env.example
├── main.py
├── configs/
│   ├── default.yaml
│   └── pipelines/
│       └── basic_analysis.yaml
├── data/
│   ├── raw/
│   │   └── example.csv
│   └── processed/
│       ├── processed.csv
│       └── report.json
├── examples/
│   └── run_basic_analysis.py
├── scripts/
│   ├── run_pipeline.py
│   └── validate_config.py
├── tests/
│   ├── conftest.py
│   ├── test_pipeline.py
│   └── test_registry.py
└── src/
    └── analysis_framework/
        ├── __init__.py
        ├── cli.py
        ├── constants.py
        ├── exceptions.py
        ├── logging.py
        ├── registry.py
        ├── config/
        │   ├── __init__.py
        │   ├── loader.py
        │   └── schema.py
        ├── core/
        │   ├── __init__.py
        │   ├── base.py
        │   ├── pipeline.py
        │   └── result.py
        ├── dataio/
        │   ├── __init__.py
        │   ├── readers.py
        │   └── writers.py
        └── algorithms/
            ├── __init__.py
            ├── preprocessing/
            │   ├── __init__.py
            │   └── missing_values.py
            └── statistics/
                ├── __init__.py
                ├── correlation.py
                └── descriptive.py
```

## 各部分作用

### 根目录

- `README.md`
  当前本地版本说明。

- `pyproject.toml`
  Python 项目配置，定义包信息和命令行入口。

- `requirements.txt`
  依赖列表。

- `.env.example`
  本地环境变量示例。

- `main.py`
  一个简单的欢迎入口，目前不参与主流程。

### `configs/`

- `default.yaml`
  默认配置示例。

- `pipelines/basic_analysis.yaml`
  当前可运行的基础分析流程配置。

说明：
这里虽然使用 `.yaml` 后缀，但当前内容写成了 `JSON` 兼容格式，这样在没有安装 `PyYAML` 的环境里也能直接运行。

### `data/`

- `data/raw/example.csv`
  原始输入数据。

- `data/processed/processed.csv`
  流程执行后的处理结果数据。

- `data/processed/report.json`
  本次执行的分析摘要结果。

关系可以简单理解为：

- `raw` 是输入
- `processed.csv` 是输出数据
- `report.json` 是输出报告

### `scripts/`

- `scripts/run_pipeline.py`
  主运行入口。

- `scripts/validate_config.py`
  配置校验入口。

### `src/analysis_framework/`

这是框架核心代码。

- `cli.py`
  命令行解析，支持 `run`、`validate`、`list-algorithms`。

- `registry.py`
  算法注册中心，负责登记和创建算法实例。

- `config/loader.py`
  读取配置文件。

- `config/schema.py`
  校验配置是否合法。

- `core/base.py`
  算法基类定义。

- `core/pipeline.py`
  流程调度核心，按配置顺序执行各算法。

- `core/result.py`
  定义 pipeline 的结果对象。

- `dataio/readers.py`
  读取 CSV 数据。

- `dataio/writers.py`
  输出 `CSV` 和 `JSON` 文件。

- `algorithms/preprocessing/missing_values.py`
  缺失值处理算法。

- `algorithms/statistics/descriptive.py`
  描述性统计算法。

- `algorithms/statistics/correlation.py`
  相关性分析算法。

## 当前已完成功能

### 1. CSV 数据读取

当前支持从 `CSV` 文件读取原始数据，例如：

```text
data/raw/example.csv
```

### 2. 配置驱动流程执行

当前流程由配置文件控制，示例配置在：

```text
configs/pipelines/basic_analysis.yaml
```

这个配置里定义了：

- 输入文件路径
- 要执行哪些步骤
- 每个步骤是否启用
- 每个步骤的参数
- 输出目录

### 3. 缺失值处理算法 `missing_values`

作用：
处理原始数据中的空值，避免后续分析出错。

当前支持的策略：

- `mean`

在当前示例数据中：

- `age` 有缺失值
- `income` 有缺失值

运行后会用对应列的平均值补上。

### 4. 描述性统计算法 `descriptive_stats`

作用：
对数值列做基础统计摘要。

当前输出指标包括：

- `count`
- `min`
- `max`
- `mean`

### 5. 相关性分析算法 `correlation`

作用：
计算数值列之间的皮尔逊相关系数，帮助观察字段之间的线性关系。

输出结果范围：

- 接近 `1`：强正相关
- 接近 `0`：相关性弱
- 接近 `-1`：强负相关

### 6. 输出处理后数据

流程跑完后会生成：

```text
data/processed/processed.csv
```

它表示已经经过处理后的数据，比如缺失值已经被补齐。

### 7. 输出分析报告

流程跑完后还会生成：

```text
data/processed/report.json
```

当前这个文件主要包含：

- 本次执行的流程名 `pipeline`
- 实际执行过的步骤 `executed_steps`
- 每个步骤的结果摘要 `artifacts`

### 8. 命令行能力

当前支持 3 个命令：

- `run`
- `validate`
- `list-algorithms`

## 如何使用

### 安装依赖

```bash
pip install -r requirements.txt
```

### 校验配置

```bash
python3 scripts/run_pipeline.py validate --config configs/pipelines/basic_analysis.yaml
```

### 查看已有算法

```bash
python3 scripts/run_pipeline.py list-algorithms
```

### 运行分析流程

```bash
python3 scripts/run_pipeline.py run --config configs/pipelines/basic_analysis.yaml
```

### 查看结果

运行后会得到：

- [example.csv](/data/raw/example.csv)
- [processed.csv](/data/processed/processed.csv)
- [report.json](/data/processed/report.json)

它们的关系是：

- `example.csv` 是原始数据
- `processed.csv` 是处理后的数据
- `report.json` 是分析摘要

## 当前测试情况

当前已经有基础测试：

- [test_registry.py](/tests/test_registry.py)
- [test_pipeline.py](/tests/test_pipeline.py)

本地验证通过：

```bash
python3 -m pytest -q
```

## 当前限制

这还是一个最小版本，目前有这些限制：

- 只支持 `CSV` 输入
- 内置算法只有 3 个
- 描述性统计结果还比较基础
- 目前没有可视化输出
- 还没有插件系统和更多数据源支持

## 下一步适合继续扩展的方向

后面比较适合继续加的内容有：

1. 缺失率统计
2. 中位数、标准差、分位数
3. 类别列频次统计
4. 标准化 / 归一化
5. 异常值检测
6. Excel / JSON 数据输入支持
