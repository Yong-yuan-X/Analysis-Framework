# Analysis-Framework

[English](./README.md) | [简体中文](./README.zh-CN.md) | [繁體中文](./README.zh-HK.md)

這是一個資料分析框架，包含一系列通用演算法和標準化工作流程。使用者可以根據需求自訂與調整演算法，並可靈活地啟用或停用它們，從而為資料處理任務提供一種彈性、模組化的解決方案。

這是目前專案的本地版本說明，描述的是倉庫中已經完成且可執行的內容，不是未來規劃草稿。

## 專案現況

這個倉庫目前已經是一個最小可執行的資料分析框架 `MVP`，支援：

- 讀取 `CSV` 原始資料
- 透過設定檔定義分析流程
- 依步驟執行內建演算法
- 輸出處理後的資料檔案
- 輸出分析結果摘要 `JSON`
- 透過命令列執行、驗證設定、查看演算法列表

目前內建了 4 個演算法：

1. `missing_values`
2. `descriptive_stats`
3. `categorical_frequency`
4. `correlation`

## 目前目錄結構

```text
Analysis-Framework/
├── README.md
├── README.zh-CN.md
├── README.zh-HK.md
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

### 根目錄

- `README.md`
  預設英文說明頁。

- `README.zh-CN.md`
  簡體中文說明頁。

- `README.zh-HK.md`
  繁體中文說明頁。

- `pyproject.toml`
  Python 專案設定，定義套件資訊與命令列入口。

- `requirements.txt`
  相依套件清單。

- `.env.example`
  本地環境變數範例。

- `main.py`
  一個簡單的歡迎入口，目前尚未參與主流程。

### `configs/`

- `default.yaml`
  預設設定範例。

- `pipelines/basic_analysis.yaml`
  目前可執行的基礎分析流程設定。

說明：
雖然這裡使用 `.yaml` 副檔名，但目前內容採用 `JSON` 相容格式，因此在未安裝 `PyYAML` 的環境中也能直接執行。

### `data/`

- `data/raw/example.csv`
  原始輸入資料。

- `data/processed/processed.csv`
  流程執行後輸出的處理結果資料。

- `data/processed/report.json`
  本次執行的分析摘要結果。

它們之間的關係可以簡單理解為：

- `raw` 是輸入
- `processed.csv` 是輸出資料
- `report.json` 是輸出報告

### `scripts/`

- `scripts/run_pipeline.py`
  主要執行入口。

- `scripts/validate_config.py`
  設定驗證入口。

### `src/analysis_framework/`

這是框架的核心程式碼。

- `cli.py`
  命令列解析，支援 `run`、`validate`、`list-algorithms`。

- `registry.py`
  演算法註冊中心，負責登記並建立演算法實例。

- `config/loader.py`
  讀取設定檔。

- `config/schema.py`
  驗證設定是否合法。

- `core/base.py`
  演算法基底類別定義。

- `core/pipeline.py`
  流程調度核心，依照設定順序執行各演算法。

- `core/result.py`
  定義 pipeline 的結果物件。

- `dataio/readers.py`
  讀取 `CSV` 資料。

- `dataio/writers.py`
  輸出 `CSV` 與 `JSON` 檔案。

- `algorithms/preprocessing/missing_values.py`
  缺失值處理演算法。

- `algorithms/statistics/descriptive.py`
  描述性統計演算法。

- `algorithms/statistics/frequency.py`
  類別頻次統計演算法。

- `algorithms/statistics/correlation.py`
  相關性分析演算法。

## 目前已完成功能

### 1. CSV 資料讀取

目前支援從 `CSV` 檔案讀取原始資料，例如：

```text
data/raw/example.csv
```

### 2. 設定驅動的流程執行

目前流程由設定檔控制，範例設定位於：

```text
configs/pipelines/basic_analysis.yaml
```

這份設定定義了：

- 輸入檔案路徑
- 要執行哪些步驟
- 每個步驟是否啟用
- 每個步驟的參數
- 輸出目錄

### 3. 缺失值處理演算法 `missing_values`

作用：
處理原始資料中的空值，避免後續分析出錯。

目前支援的策略：

- `mean`

在目前範例資料中：

- `age` 有缺失值
- `income` 有缺失值

執行後會以對應欄位的平均值補上。

### 4. 描述性統計演算法 `descriptive_stats`

作用：
對數值欄位產生基礎統計摘要。

目前輸出指標包括：

- `count`
- `min`
- `max`
- `mean`

### 5. 類別頻次統計演算法 `categorical_frequency`

作用：
對類別欄位做頻次統計，協助快速識別常見取值與基礎分佈情況。

目前輸出包括：

- `total`：該欄位非空值總數
- `unique`：去重後的取值數量
- `top_values`：依出現次數排序的高頻值、次數與占比

預設範例流程會分析 `city` 欄位，並保留前 `3` 個高頻值。

### 6. 相關性分析演算法 `correlation`

作用：
計算數值欄位之間的皮爾森相關係數，協助觀察欄位之間的線性關係。

結果範圍可大致理解為：

- 接近 `1`：強正相關
- 接近 `0`：相關性弱
- 接近 `-1`：強負相關

### 7. 輸出處理後資料

流程執行完後會產生：

```text
data/processed/processed.csv
```

它表示已經處理完成的資料，例如缺失值已被補齊。

### 8. 輸出分析報告

流程執行完後也會產生：

```text
data/processed/report.json
```

目前這個檔案主要包含：

- 本次執行的流程名稱 `pipeline`
- 實際執行過的步驟 `executed_steps`
- 每個步驟的結果摘要 `artifacts`

### 9. 命令列能力

目前支援 3 個命令：

- `run`
- `validate`
- `list-algorithms`

## 如何使用

### 安裝相依套件

```bash
pip install -r requirements.txt
```

### 驗證設定

```bash
python3 scripts/run_pipeline.py validate --config configs/pipelines/basic_analysis.yaml
```

### 查看現有演算法

```bash
python3 scripts/run_pipeline.py list-algorithms
```

### 執行分析流程

```bash
python3 scripts/run_pipeline.py run --config configs/pipelines/basic_analysis.yaml
```

### 查看結果

執行後會得到：

- [example.csv](/Users/a1-6/Analysis-Framework/data/raw/example.csv)
- [processed.csv](/Users/a1-6/Analysis-Framework/data/processed/processed.csv)
- [report.json](/Users/a1-6/Analysis-Framework/data/processed/report.json)

它們的關係是：

- `example.csv` 是原始資料
- `processed.csv` 是處理後的資料
- `report.json` 是分析摘要

## 目前測試情況

目前已經有基礎測試：

- [test_registry.py](/Users/a1-6/Analysis-Framework/tests/test_registry.py)
- [test_pipeline.py](/Users/a1-6/Analysis-Framework/tests/test_pipeline.py)

本地驗證通過：

```bash
python3 -m pytest -q
```

## 目前限制

這仍然是一個最小版本，目前有以下限制：

- 只支援 `CSV` 輸入
- 內建演算法只有 4 個
- 描述性統計結果仍較基礎
- 目前尚無視覺化輸出
- 尚未提供外掛系統與更多資料來源支援

## 下一步適合擴充的方向

後續很適合加入的內容包括：

1. 缺失率統計
2. 中位數、標準差、分位數
3. 標準化 / 正規化
4. 異常值檢測
5. Excel / JSON 資料輸入支援
