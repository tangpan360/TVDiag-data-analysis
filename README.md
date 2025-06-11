# TVDiag 数据处理过程分析记录

## 项目结构

TVDiag对数据进行预处理的文件夹是 extractor，主要包括以下文件和目录：

```text
extractor
├── 1. raw_process.py
├── 2. preprocess.py
├── 3. log_template_extractor.py
├── 4. event_extractor.py
├── extractor
│   ├── 4.1 log_event_extractor.py
│   ├── 4.2 metric_event_extractor.py
│   └── 4.3 trace_event_extractor.py
├── 5. deployment_extractor.py
├── drain
│   ├── drain3.ini
│   └── drain_template_extractor.py
└── utils
    ├── detect_util.py
    ├── io_util.py
    └── time_util.py
```

## GAIA 数据集描述

数据集官方介绍地址[Dataset description](https://docs.aiops.cloudwise.com/zh/gaia/dataset-description.html#micross)

GAIA 数据集包含来自 MicroSS 和 Companion Data 的数据，旨在支持根因分析算法的评估。以下是数据集的主要特点和结构：

### 数据集概述
- **数据来源**: 
  - **MicroSS**: 包含超过 6,500 个指标和 7,000,000 条日志项目，详细的追踪数据在两周内持续收集。
  - **Companion Data**: 提供了额外的指标和日志数据，确保数据隐私且包含异常检测和度量预测的数据。

- **异常模拟**: 数据集中模拟了真实系统中可能发生的异常，并记录了所有异常注入，以公平的根因分析算法评估。

### 目录结构
1. **MicroSS 目录**
   - **metric**: 指标数据，以 CSV 格式存储，每个文件包含节点、IP 和对应指标值的时间序列数据。
   - **trace**: 追踪记录，提供详细的服务调用信息。
   - **business**: 业务日志，记录与 node 相关的业务操作信息。
   - **run**: 系统日志及异常注入记录。


2. **Companion Data 目录**
   - **log**: 包含日志解析、日志语义异常检测和命名实体识别相关数据。
   - **metric_detection**: 包含标记的时间序列数据，用于异常检测。
   - **metric_forecast**: 包含可用于时间序列预测的数据。

### 数据字段描述
- **业务日志**: datetime、service、message。
- **指标数据**: timestamp、value。
- **追踪记录**: timestamp、host_ip、service_name、trace_id 等。
- **系统日志**: 类似于业务日志，记录系统级别的操作和异常信息。

## GAIA-DataSet-release-v1.0.zip 解压内容
```text
GAIA-DataSet-release-v1.0
├── Companion_Data
│   ├── log.zip
│   ├── metric_detection.zip
│   └── metric_forecast.zip
├── MicroSS
│   ├── business
│   │   ├── business_split.z01
│   │   ├── business_split.z02
│   │   ├── business_split.z03
│   │   ├── business_split.z04
│   │   ├── business_split.z05
│   │   ├── business_split.z06
│   │   ├── business_split.z07
│   │   ├── business_split.z08
│   │   ├── business_split.z09
│   │   ├── business_split.z10
│   │   ├── business_split.z11
│   │   ├── business_split.z12
│   │   ├── business_split.z13
│   │   ├── business_split.z14
│   │   ├── business_split.z15
│   │   ├── business_split.z16
│   │   ├── business_split.z17
│   │   ├── business_split.z18
│   │   ├── business_split.z19
│   │   ├── business_split.z20
│   │   ├── business_split.z21
│   │   ├── business_split.z22
│   │   ├── business_split.z23
│   │   ├── business_split.z24
│   │   ├── business_split.z25
│   │   ├── business_split.z26
│   │   ├── business_split.z27
│   │   ├── business_split.z28
│   │   ├── business_split.z29
│   │   ├── business_split.z30
│   │   ├── business_split.z31
│   │   └── business_split.zip
│   ├── metric
│   │   ├── metric_split.z01
│   │   ├── metric_split.z02
│   │   ├── metric_split.z03
│   │   ├── metric_split.z04
│   │   ├── metric_split.z05
│   │   ├── metric_split.z06
│   │   ├── metric_split.z07
│   │   ├── metric_split.z08
│   │   ├── metric_split.z09
│   │   ├── metric_split.z10
│   │   ├── metric_split.z11
│   │   ├── metric_split.z12
│   │   ├── metric_split.z13
│   │   ├── metric_split.z14
│   │   ├── metric_split.z15
│   │   ├── metric_split.z16
│   │   └── metric_split.zip
│   ├── run
│   │   └── run.zip
│   ├── trace
│   │   ├── trace_split.z01
│   │   ├── trace_split.z02
│   │   ├── trace_split.z03
│   │   ├── trace_split.z04
│   │   ├── trace_split.z05
│   │   ├── trace_split.z06
│   │   ├── trace_split.z07
│   │   ├── trace_split.z08
│   │   ├── trace_split.z09
│   │   ├── trace_split.z10
│   │   ├── trace_split.z11
│   │   ├── trace_split.z12
│   │   ├── trace_split.z13
│   │   ├── trace_split.z14
│   │   ├── trace_split.z15
│   │   ├── trace_split.z16
│   │   ├── trace_split.z17
│   │   ├── trace_split.z18
│   │   ├── trace_split.z19
│   │   ├── trace_split.z20
│   │   ├── trace_split.z21
│   │   ├── trace_split.z22
│   │   ├── trace_split.z23
│   │   ├── trace_split.z24
│   │   ├── trace_split.z25
│   │   ├── trace_split.z26
│   │   ├── trace_split.z27
│   │   ├── trace_split.z28
│   │   ├── trace_split.z29
│   │   ├── trace_split.z30
│   │   ├── trace_split.z31
│   │   └── trace_split.zip
│   └── MicroSS system description.docx
├── LICENSE
└── README.md
```
## 分卷压缩文件说明

项目中出现的 `.z01`, `.z02`, ..., `.zip` 文件是分卷压缩文件(Split Archive)，由压缩工具(如 WinRAR、7-Zip 或 Zip 命令)生成。

### 分卷压缩文件的作用

大文件被拆分成多个小文件(分卷)的主要目的是：

1. 绕过单文件大小限制
   - 例如邮件附件大小限制
   - 云存储上传限制

2. 方便文件传输与存储
   - 支持分批传输(FTP等)
   - 便于使用USB等移动设备存储

### 解压方法

直接解压 `.zip` 文件即可，压缩工具会自动识别并合并所有分卷文件。

将 business_split.zip、metric_split.zip、trace_split.zip、run.zip 解压后如下：

```text
```text
GAIA-DataSet-release-v1.0
├── Companion_Data
│   ├── log.zip
│   ├── metric_detection.zip
│   └── metric_forecast.zip
├── MicroSS
│   ├── business
│   │   ├── business
│   │   │   ├── business_table_dbservice1_2021-07.csv
│   │   │   ├── business_table_dbservice2_2021-07.csv
│   │   │   ├── business_table_logservice1_2021-07.csv
│   │   │   ├── business_table_logservice2_2021-07.csv
│   │   │   ├── business_table_mobservice1_2021-07.csv
│   │   │   ├── business_table_mobservice2_2021-07.csv
│   │   │   ├── business_table_redisservice1_2021-07.csv
│   │   │   ├── business_table_redisservice2_2021-07.csv
│   │   │   ├── business_table_webservice1_2021-07.csv
│   │   │   └── business_table_webservice2_2021-07.csv
│   │   ├── business_split.z01
│   │   ├── business_split.z02
│   │   ├── business_split.z03
│   │   ├── business_split.z04
│   │   ├── business_split.z05
│   │   ├── business_split.z06
│   │   ├── business_split.z07
│   │   ├── business_split.z08
│   │   ├── business_split.z09
│   │   ├── business_split.z10
│   │   ├── business_split.z11
│   │   ├── business_split.z12
│   │   ├── business_split.z13
│   │   ├── business_split.z14
│   │   ├── business_split.z15
│   │   ├── business_split.z16
│   │   ├── business_split.z17
│   │   ├── business_split.z18
│   │   ├── business_split.z19
│   │   ├── business_split.z20
│   │   ├── business_split.z21
│   │   ├── business_split.z22
│   │   ├── business_split.z23
│   │   ├── business_split.z24
│   │   ├── business_split.z25
│   │   ├── business_split.z26
│   │   ├── business_split.z27
│   │   ├── business_split.z28
│   │   ├── business_split.z29
│   │   ├── business_split.z30
│   │   ├── business_split.z31
│   │   └── business_split.zip
│   ├── metric
│   │   ├── metric
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_0_norm_pct_2021-07-01_2021-07-15.csv
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_0_norm_pct_2021-07-15_2021-07-31.csv
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-15_2021-07-31.csv
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_0_ticks_2021-07-01_2021-07-15.csv
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_0_ticks_2021-07-15_2021-07-31.csv
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_1_norm_pct_2021-07-01_2021-07-15.csv
│   │   │   ├── dbservice1_0.0.0.4_docker_cpu_core_1_norm_pct_2021-07-15_2021-07-31.csv
│   │   │   ├── ...
│   │   │   ├── ...metric 文件共计 6640 个
│   │   │   ├── ...
│   │   │   └── zookeeper_0.0.0.1_zookeeper_server_sent_2021-07-15_2021-07-31.csv
│   │   ├── metric_split.z01
│   │   ├── metric_split.z02
│   │   ├── metric_split.z03
│   │   ├── metric_split.z04
│   │   ├── metric_split.z05
│   │   ├── metric_split.z06
│   │   ├── metric_split.z07
│   │   ├── metric_split.z08
│   │   ├── metric_split.z09
│   │   ├── metric_split.z10
│   │   ├── metric_split.z11
│   │   ├── metric_split.z12
│   │   ├── metric_split.z13
│   │   ├── metric_split.z14
│   │   ├── metric_split.z15
│   │   ├── metric_split.z16
│   │   └── metric_split.zip
│   ├── run
│   │   ├── run
│   │   │   └── run_table_2021-07.csv
│   │   └── run.zip
│   ├── trace
│   │   ├── trace
│   │   │   ├── trace_table_dbservice1_2021-07.csv
│   │   │   ├── trace_table_dbservice2_2021-07.csv
│   │   │   ├── trace_table_logservice1_2021-07.csv
│   │   │   ├── trace_table_logservice2_2021-07.csv
│   │   │   ├── trace_table_mobservice1_2021-07.csv
│   │   │   ├── trace_table_mobservice2_2021-07.csv
│   │   │   ├── trace_table_redisservice1_2021-07.csv
│   │   │   ├── trace_table_redisservice2_2021-07.csv
│   │   │   ├── trace_table_webservice1_2021-07.csv
│   │   │   └── trace_table_webservice2_2021-07.csv
│   │   ├── trace_split.z01
│   │   ├── trace_split.z02
│   │   ├── trace_split.z03
│   │   ├── trace_split.z04
│   │   ├── trace_split.z05
│   │   ├── trace_split.z06
│   │   ├── trace_split.z07
│   │   ├── trace_split.z08
│   │   ├── trace_split.z09
│   │   ├── trace_split.z10
│   │   ├── trace_split.z11
│   │   ├── trace_split.z12
│   │   ├── trace_split.z13
│   │   ├── trace_split.z14
│   │   ├── trace_split.z15
│   │   ├── trace_split.z16
│   │   ├── trace_split.z17
│   │   ├── trace_split.z18
│   │   ├── trace_split.z19
│   │   ├── trace_split.z20
│   │   ├── trace_split.z21
│   │   ├── trace_split.z22
│   │   ├── trace_split.z23
│   │   ├── trace_split.z24
│   │   ├── trace_split.z25
│   │   ├── trace_split.z26
│   │   ├── trace_split.z27
│   │   ├── trace_split.z28
│   │   ├── trace_split.z29
│   │   ├── trace_split.z30
│   │   ├── trace_split.z31
│   │   └── trace_split.zip
│   └── MicroSS system description.docx
├── LICENSE
└── README.md
```

我们只需要 MicroSS 文件夹中的内容，经整理后文件结构如下：

```text
MicroSS
├── business
│   ├── business_table_dbservice1_2021-07.csv
│   ├── business_table_dbservice2_2021-07.csv
│   ├── business_table_logservice1_2021-07.csv
│   ├── business_table_logservice2_2021-07.csv
│   ├── business_table_mobservice1_2021-07.csv
│   ├── business_table_mobservice2_2021-07.csv
│   ├── business_table_redisservice1_2021-07.csv
│   ├── business_table_redisservice2_2021-07.csv
│   ├── business_table_webservice1_2021-07.csv
│   └── business_table_webservice2_2021-07.csv
├── metric
│   ├── dbservice1_0.0.0.4_docker_cpu_core_0_norm_pct_2021-07-01_2021-07-15.csv
│   ├── dbservice1_0.0.0.4_docker_cpu_core_0_norm_pct_2021-07-15_2021-07-31.csv
│   ├── dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv
│   ├── dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-15_2021-07-31.csv
│   ├── dbservice1_0.0.0.4_docker_cpu_core_0_ticks_2021-07-01_2021-07-15.csv
│   ├── dbservice1_0.0.0.4_docker_cpu_core_0_ticks_2021-07-15_2021-07-31.csv
│   ├── dbservice1_0.0.0.4_docker_cpu_core_1_norm_pct_2021-07-01_2021-07-15.csv
│   ├── dbservice1_0.0.0.4_docker_cpu_core_1_norm_pct_2021-07-15_2021-07-31.csv
│   ├── ...
│   ├── ...metric 文件共计 6640 个
│   ├── ...
│   └── zookeeper_0.0.0.1_zookeeper_server_sent_2021-07-15_2021-07-31.csv
├── run
│   └── run_table_2021-07.csv
└── trace
    ├── trace_table_dbservice1_2021-07.csv
    ├── trace_table_dbservice2_2021-07.csv
    ├── trace_table_logservice1_2021-07.csv
    ├── trace_table_logservice2_2021-07.csv
    ├── trace_table_mobservice1_2021-07.csv
    ├── trace_table_mobservice2_2021-07.csv
    ├── trace_table_redisservice1_2021-07.csv
    ├── trace_table_redisservice2_2021-07.csv
    ├── trace_table_webservice1_2021-07.csv
    └── trace_table_webservice2_2021-07.csv
```

## 代码运行顺序

### 1. raw_process.py


此时还不能运行程序，还需要一个标签文件：label.csv

此标签文件从 TVDiag 代码仓库中的 /data/gaia/label.csv 获取（**具体怎么来的目前尚不清楚**），放置到 MicroSS 文件夹中，改名字为 gaia.csv 即可。

首次运行 ``raw_process.py`` 将 ``process_traces`` 和 ``process_logs`` 取消注释，并将 ``trace`` 改成 ``MicroSS/trace``，``business`` 改成 ``MicroSS/business``：

```python
trace_df = process_traces("MicroSS/trace")
log_df = process_logs("MicroSS/business")
```


### 处理流程总结

在这个项目中，`process_traces` 和 `process_logs` 函数负责处理来自不同服务的追踪和日志数据。以下是这两个函数的处理流程总结：

1. **`process_traces` 函数**：
   - **读取数据**：遍历指定目录中的所有 CSV 文件，筛选出以 `2021-07.csv` 结尾的文件，并将其读取为 Pandas DataFrame。
   - **数据合并**：通过左连接将 `parent_id` 和 `span_id` 进行合并，添加 `parent_name` 属性。
   - **时间戳转换**：将 `start_time` 和 `end_time` 列转换为时间戳格式。
   - **保存结果**：将处理后的 DataFrame 保存为 `trace.csv` 文件。

2. **`process_logs` 函数**：
   - **读取数据**：同样遍历指定目录中的所有 CSV 文件，筛选出以 `2021-07.csv` 结尾的文件，并将其读取为 Pandas DataFrame。
   - **提取时间戳**：从 `message` 列中提取时间戳，并将其转换为时间戳格式。
   - **保存结果**：将处理后的 DataFrame 保存为 `log.csv` 文件。

### 示例说明

以下是处理前后的数据对比，使用 Markdown 表格格式展示：

### 1. 追踪数据对比

#### 处理前的数据（`trace_table_webservice1_2021-07.csv`）：

| timestamp         | host_ip   | service_name | trace_id            | span_id            | parent_id | start_time | end_time | url                                 | status_code | message                                      |
|-------------------|-----------|--------------|---------------------|---------------------|-----------|------------|----------|--------------------------------------|-------------|----------------------------------------------|
| 2021/7/1 9:57     | 0.0.0.1  | webservice1  | 22741016938865b0    | 3a98d34fb3b6075e    | 0         | 57:04.3    | 57:04.3  | http://0.0.0.1:9379/web_login_service | 500         | request call function 1 webservice1.web_login_service |
| 2021/7/1 10:54    | 0.0.0.1  | webservice1  | c124e30fb40651dc    | e0be90c60eb65aeb    | 0         | 54:21.9    | 54:23.2  | http://0.0.0.1:9379/web_login_service | 200         | request call function 1 webservice1.web_login_service |

#### 处理后的数据（`trace.csv`）：

| start_time | end_time | host_ip   | service_name | trace_id            | span_id            | parent_id | parent_name |
|------------|----------|-----------|--------------|---------------------|---------------------|-----------|-------------|
| 1625115423000 | 1625115423000 | 0.0.0.1  | webservice1  | 22741016938865b0    | 3a98d34fb3b6075e    | 0         | None        |
| 1625115462000 | 1625115502000 | 0.0.0.1  | webservice1  | c124e30fb40651dc    | e0be90c60eb65aeb    | 0         | None        |

---

### 2. 日志数据对比

#### 处理前的数据（`business_table_redisservice1_2021-07.csv`）：

| datetime         | service        | message                                                                                       |
|-------------------|----------------|-----------------------------------------------------------------------------------------------|
| 2021/7/1          | redisservice1  | "2021-07-01 10:54:21,949 | INFO | 0.0.0.1 | 172.17.0.4 | redisservice1 | c124e30fb40651dc | redis write success" |
| 2021/7/1          | redisservice1  | "2021-07-01 10:54:22,706 | INFO | 0.0.0.1 | 172.17.0.4 | redisservice1 | c124e30fb40651dc | service accept, status_code: 200" |

#### 处理后的数据（`log.csv`）：

| timestamp         | service        | message                                                                                       |
|-------------------|----------------|-----------------------------------------------------------------------------------------------|
| 1625115461000     | redisservice1  | "2021-07-01 10:54:21,949 | INFO | 0.0.0.1 | 172.17.0.4 | redisservice1 | c124e30fb40651dc | redis write success" |
| 1625115462000     | redisservice1  | "2021-07-01 10:54:22,706 | INFO | 0.0.0.1 | 172.17.0.4 | redisservice1 | c124e30fb40651dc | service accept, status_code: 200" |

---

通过以上表格，可以清晰地看到数据在处理前后的变化，包括列名的调整、时间格式的转换以及新列的添加。

## read_all_metrics() 函数处理流程

让我们通过具体的文件名和数据示例来讲解 `read_all_metrics` 函数的整个流程。

### 文件示例

假设我们有以下四个文件：

1. `dbservice1_0.0.0.4_docker_cpu_core_0_norm_pct_2021-07-01_2021-07-15.csv`
2. `dbservice1_0.0.0.4_docker_cpu_core_0_norm_pct_2021-07-15_2021-07-31.csv`
3. `dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv`
4. `dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-15_2021-07-31.csv`

### 数据示例

假设其中一个文件 `dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv` 的内容如下：

```
timestamp,value
1626278400000,0.00038998529411764704
1626278430000,0.036145619753086417
1626278460000,0.00032236461916461916
1626278490000,0.0
1626278520000,0.0
1626278550000,0.0
1626278580000,0.0
1626278610000,0.032702104901960787
1626278640000,0.0
1626278670000,0.025628760396039604
1626278700000,0.0
```

### 处理流程

1. **定义服务和 Pod 名称**：
   - 函数开始时定义了服务名称（如 `dbservice`）并为每个服务创建两个 Pod 名称（如 `dbservice1` 和 `dbservice2`）。

2. **遍历指标文件**：
   - 函数使用 `os.listdir("MicroSS/metric")` 列出 `MicroSS/metric` 目录中的所有文件。

3. **筛选有效文件**：
   - 对于每个文件，函数会检查文件名是否包含有效的 Pod 名称（如 `dbservice1`）并且不包含特定日期（如 `2021-07-15_2021-07-31`）。
   - 例如，`dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-15_2021-07-31.csv` 是有效的文件。

4. **提取指标名称**：
   - 从文件名中提取指标名称。对于 `dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv`，指标名称为 `docker_cpu_core_0_pct`。

5. **读取数据**：
   - 使用 `pd.read_csv` 读取当前文件的数据到 DataFrame（例如 `df1`）。
   - 构造第二部分数据的文件名（如 `dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-15_2021-07-31.csv`），并读取数据到 `df2`。

6. **合并数据**：
   - 将 `df1` 和 `df2` 合并在一起，形成一个完整的指标数据集。

7. **存储数据**：
   - 创建一个键（如 `dbservice1_0.0.0.4`），并将合并后的数据存储在字典 `data` 中，键为指标名称。

8. **返回结果**：
   - 函数结束时返回包含所有指标数据的字典 `data`。

### 最终结果

经过处理，将得到一个类似于以下结构的字典：

```python
{
    'dbservice1_0.0.0.4': {
        'docker_cpu_core_0_pct': combined_dataframe,  # 合并后的 DataFrame
        'docker_cpu_core_0_norm_pct': another_combined_dataframe  # 另一个合并后的 DataFrame
    },
    # 其他 Pod 的数据...
}
```

## 提取故障附近数据的过程
以下是对代码中提取追踪、日志和指标数据的过程的逐步文字描述，以及具体的提取规则。

### 过程描述

1. **遍历故障标签**：
   - 使用 `iterrows()` 方法遍历 `label_df` 中的每一行，获取每个故障标签的相关信息。

2. **记录开始时间**：
   - 记录处理当前故障标签的开始时间，以便后续计算处理时间。

3. **获取故障索引和时间**：
   - 从当前行中提取故障的索引 `idx` 和开始、结束时间 `st_time` 和 `ed_time`。

4. **提取追踪数据**：
   - 调用 `extract_traces` 函数，传入追踪数据 DataFrame 和故障开始时间 `st_time`。
   - **提取规则**：
     - 定义一个 10 分钟的时间窗口。
     - 筛选出故障发生前 4 个时间窗口的数据（`start_time` 在 `st_time` 之前的时间）。
     - 筛选出故障发生后 1 个时间窗口的数据（`start_time` 在 `st_time` 之后的时间）。
   - 将提取到的追踪数据分别存储在 `pre_data` 和 `post_data` 字典中。

5. **提取日志数据**：
   - 调用 `extract_logs` 函数，传入日志数据 DataFrame 和故障开始时间 `st_time`。
   - **提取规则**：
     - 同样定义一个 10 分钟的时间窗口。
     - 筛选出故障发生前 4 个时间窗口的日志数据。
     - 筛选出故障发生后 1 个时间窗口的日志数据。
   - 将提取到的日志数据分别存储在 `pre_data` 和 `post_data` 字典中。

6. **提取指标数据**：
   - 初始化 `pre_metrics` 和 `post_metrics` 字典，用于存储故障前后的指标数据。
   - 遍历 `metric_data` 字典，获取每个 Pod 的指标数据。
   - 对于每个指标，调用 `extract_metrics` 函数，传入指标 DataFrame 和故障开始时间 `st_time`。
   - **提取规则**：
     - 定义一个 10 分钟的时间窗口。
     - 筛选出故障发生前 4 个时间窗口的指标数据。
     - 筛选出故障发生后 1 个时间窗口的指标数据。
   - 将提取到的指标数据分别存储在 `pre_metrics` 和 `post_metrics` 字典中。

7. **存储提取的数据**：
   - 将提取到的追踪、日志和指标数据存储在 `pre_data` 和 `post_data` 字典中，使用故障索引 `idx` 作为键。

8. **记录处理时间**：
   - 记录处理结束时间，计算并打印处理当前故障标签所用的时间。

9. **保存数据**：
   - 最后，将处理后的故障后数据保存到文件中。

### 总结

这个过程通过遍历故障标签，提取与故障相关的追踪、日志和指标数据，使用时间窗口来筛选数据，确保提取到的都是与故障发生前后相关的数据。每种数据的提取规则都基于相同的时间窗口逻辑，使得数据处理过程一致且高效。
