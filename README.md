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


# 2. preprocess.py 数据预处理与异常检测器构建

`preprocess.py` 文件主要负责两个关键任务：构建正常指标和追踪数据集，以及训练异常检测器。这是TVDiag数据处理流程中的重要环节，它将raw_process.py处理后的数据进一步加工，为后续的异常检测做准备。

## 2.1 构建正常指标和追踪数据集

该阶段的主要目标是从预处理数据中提取正常状态下的系统指标和服务追踪数据，为异常检测器提供训练基准。

### 处理流程

1. **加载数据**：
   - 读取标签数据(`MicroSS/gaia.csv`)
   - 加载预处理数据(`MicroSS/pre-data.pkl`)

2. **初始化数据容器**：
   ```python
   normal_metrics = {}  # 存储各pod的指标数据
   normal_traces = defaultdict(list)  # 存储追踪数据
   ```

3. **遍历标签数据**：
   - 跳过测试类型数据
   - 对每个索引，提取对应的数据块

4. **处理指标数据**：
   - 收集每个pod的各项指标数据
   ```python
   for pod, kpi_dic in chunk['metric'].items():
       if pod not in normal_metrics.keys():
           normal_metrics[pod] = defaultdict(list)
       for kpi, kpi_df in kpi_dic.items():
           normal_metrics[pod][kpi].append(kpi_df)
   ```

5. **处理追踪数据**：
   - 从URL中提取操作名称
   - 按父服务、目标服务和操作分组
   ```python
   trace_df['operation'] = trace_df['url'].str.split('?').str[0]
   trace_gp = trace_df.groupby(['parent_name', 'service_name', 'operation'])
   for (src, dst, op), call_df in trace_gp:
       name = src + '-' + dst + '-' + op
       normal_traces[name].append(call_df)
   ```

6. **合并数据**：
   - 将各pod的指标数据合并成一个完整的DataFrame
   ```python
   for pod in normal_metrics.keys():
       for kpi, kpi_dfs in normal_metrics[pod].items():
           normal_metrics[pod][kpi] = pd.concat(kpi_dfs)
   ```

7. **保存处理后的数据**：
   - 正常追踪数据保存为`MicroSS/detector/normal_traces.pkl`
   - 正常指标数据保存为`MicroSS/detector/normal_metrics.pkl`

## 2.2 构建异常检测器

该阶段使用之前准备的正常数据训练两类异常检测器：基于统计的指标检测器和基于孤立森林算法的追踪检测器。

### 指标检测器构建

1. **加载正常数据**：
   ```python
   normal_traces = io_util.load('MicroSS/detector/normal_traces.pkl')
   normal_metrics = io_util.load('MicroSS/detector/normal_metrics.pkl')
   ```

2. **构建指标检测器(基于均值和标准差)**：
   ```python
   metric_detectors = {}
   for pod in normal_metrics.keys():
       metric_detectors[pod] = {}
       for kpi, dfs in normal_metrics[pod].items():
           # 为每个指标存储均值和标准差
           metric_detectors[pod][kpi] = [
               normal_metrics[pod][kpi]['value'].mean(), 
               normal_metrics[pod][kpi]['value'].std()
           ]
   ```

   此检测器采用简单的统计方法，记录每个指标的均值和标准差，用于后续识别超出正常范围的指标值。

### 追踪检测器构建

1. **初始化孤立森林模型**：
   ```python
   trace_detectors = {}
   for name, call_dfs in normal_traces.items():
       trace_detectors[name] = {
           'dur_detector': IsolationForest(random_state=0, n_estimators=5),
           '500_detector': IsolationForest(random_state=0, n_estimators=5),
           '400_detector': IsolationForest(random_state=0, n_estimators=5)
       }
   ```
   
   为每种服务调用关系创建三种检测器：
   - `dur_detector`: 检测异常响应时间
   - `500_detector`: 检测异常500错误率
   - `400_detector`: 检测异常400错误率

2. **数据特征提取**：
   ```python
   for call_df in call_dfs:
       _, durs, err_500_ps, err_400_ps = slide_window(call_df, 30 * 1000)
       train_ds.extend(durs)  # 持续时间特征
       train_500_ep.extend(err_500_ps)  # 500错误特征
       train_400_ep.extend(err_400_ps)  # 400错误特征
   ```
   
   使用`slide_window`函数处理追踪数据，提取三类特征：
   - 平均响应时间
   - 500错误数量
   - 400错误数量

3. **训练检测器**：
   ```python
   dur_clf.fit(np.array(train_ds).reshape(-1,1))
   err_500_clf.fit(np.array(err_500_ps).reshape(-1,1))
   err_400_clf.fit(np.array(err_400_ps).reshape(-1,1))
   ```
   
   分别训练三个孤立森林模型，用于检测异常值。

4. **保存模型**：
   ```python
   io_util.save('MicroSS/detector/trace-detector.pkl', trace_detectors)
   io_util.save('MicroSS/detector/metric-detector-strict-host.pkl', metric_detectors)
   ```

## 2.3 滑动窗口函数详解

`slide_window`函数是追踪数据异常检测的核心，它通过时间窗口对追踪数据进行特征提取：

```python
def slide_window(df, win_size):
    """滑动窗口函数，计算时间窗口内的追踪指标"""
    sts, ds, err_500_ps, err_400_ps=[], [], [], []
    
    # 计算每个span的持续时间
    df['duration'] = df['end_time']-df['start_time']
    
    # 初始化窗口起始时间和最大时间
    i, time_max=df['start_time'].min(), df['start_time'].max()
    
    # 滑动窗口处理
    while i < time_max:
        # 获取当前窗口内的数据
        temp_df = df[(df['start_time']>=i)&(df['start_time']<=i+win_size)]
        if temp_df.empty:
            i+=win_size
            continue
            
        # 记录窗口开始时间    
        sts.append(i)
        
        # 统计500和400错误数量
        err_500_ps.append(len(temp_df[temp_df['status_code']==500]))
        err_400_ps.append(len(temp_df[temp_df['status_code']==400]))
        
        # 计算窗口平均持续时间
        ds.append(temp_df['duration'].mean())
        i+=win_size
        
    return np.array(sts), np.array(ds), np.array(err_500_ps), np.array(err_400_ps)
```

该函数的输入是追踪数据DataFrame和窗口大小(毫秒)，输出是四个数组：
- `sts`: 窗口开始时间数组
- `ds`: 窗口平均持续时间数组
- `err_500_ps`: 窗口500错误数量数组
- `err_400_ps`: 窗口400错误数量数组

### 处理示例

假设我们有以下追踪数据：

| start_time | end_time | status_code |
|------------|----------|-------------|
| 1000       | 1100     | 200         |
| 1050       | 1200     | 200         |
| 1120       | 1220     | 500         |
| 1200       | 1350     | 200         |
| 1600       | 1700     | 400         |

使用30秒(30000毫秒)的窗口大小，处理后得到：

| 窗口开始时间 | 平均持续时间 | 500错误数 | 400错误数 |
|------------|------------|----------|----------|
| 1000       | 116.67     | 1        | 0        |
| 1600       | 100        | 0        | 1        |

这些特征将用于训练孤立森林模型，识别异常的响应时间和错误率。

<think>

用户要求我参考 `log_template_extractor.py` 和 `drain_template_extractor.py` 继续撰写 README，写出这部分的详细处理步骤。

首先让我分析这两个文件：

1. `log_template_extractor.py`：
   - 加载预处理后的日志数据和标签数据
   - 收集所有训练集的日志消息
   - 使用Drain算法提取日志模板
   - 对聚类结果按大小降序排序
   - 保存模板信息到CSV文件

2. `drain_template_extractor.py`：
   - 实现了Drain算法的核心功能
   - `init_drain()`: 初始化Drain模板挖掘器
   - `extract_templates()`: 从日志列表中提取模板
   - `match_template()`: 将日志匹配到已有模板

从代码流程看，这是第3步：日志模板提取，使用Drain算法进行日志解析。

让我按照README的写作风格来继续撰写这部分内容。
</think>
# 3. log_template_extractor.py 日志模板提取

`log_template_extractor.py` 是TVDiag数据处理流程的第三步，主要功能是使用Drain算法从大量日志数据中提取结构化的日志模板。这一步骤对于后续的日志异常检测至关重要，因为它将非结构化的日志文本转换为可以进行模式识别和异常检测的结构化模板。

## 3.1 Drain算法简介

Drain是一种高效的在线日志模板提取算法，能够从大量的日志消息中自动识别和提取日志模板。其核心思想是：
- **固定深度解析树**：使用固定深度的前缀树来组织日志模板
- **相似度匹配**：通过计算日志消息与现有模板的相似度来决定是否归类到现有模板
- **在线学习**：支持增量式学习，可以处理流式日志数据

## 3.2 处理流程详解

### 3.2.1 数据加载和准备

```python
# 加载预处理后的日志数据和标签数据
data: dict = io_util.load('MicroSS/post-data-10.pkl')  # 加载预处理后的数据字典
label_df = pd.read_csv('MicroSS/gaia.csv', index_col=0)  # 加载标签数据，第一列作为索引
```

1. **加载数据源**：
   - `post-data-10.pkl`: 包含故障发生后10分钟时间窗口内的日志、追踪和指标数据
   - `gaia.csv`: 包含故障标签信息，用于区分训练集和测试集

2. **数据筛选**：
   - 只使用训练集数据来训练Drain模型
   - 跳过测试集数据，确保模型的泛化能力

### 3.2.2 日志消息收集

```python
# 收集所有训练集的日志消息
logs = []
for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
    if row['data_type'] == 'test':  # 跳过测试数据
        continue
    chunk = data[idx]  # 获取当前索引对应的数据块
    logs.extend(chunk['log']['message'].values.tolist())  # 收集日志消息
```

这一步将所有训练集中的日志消息合并到一个列表中，为后续的模板提取做准备。

**处理示例**：
假设我们有以下几条日志消息：
```
"2021-07-01 10:54:21,949 | INFO | 0.0.0.1 | 172.17.0.4 | redisservice1 | c124e30fb40651dc | redis write success"
"2021-07-01 10:54:22,706 | INFO | 0.0.0.1 | 172.17.0.4 | redisservice1 | c124e30fb40651dc | service accept, status_code: 200"
"2021-07-01 10:55:15,342 | ERROR | 0.0.0.1 | 172.17.0.3 | dbservice1 | a567d89fb2c3451e | database connection failed"
```

### 3.2.3 Drain模板提取

```python
# 使用Drain算法提取日志模板
miner = extract_templates(
    log_list=logs,  # 传入所有日志消息列表
    save_pth='drain/gaia-drain.pkl'  # 保存训练好的Drain模型路径
)
```

#### Drain初始化过程

```python
def init_drain():
    config = TemplateMinerConfig()
    config_pth = os.path.join(
        os.path.dirname(__file__),
        "drain3.ini"
    )
    config.load(config_pth)
    config.profiling_enabled = True
    template_miner = TemplateMiner(config=config)
    return template_miner
```

1. **配置加载**：从`drain3.ini`文件加载Drain算法的配置参数
2. **参数设置**：包括相似度阈值、树的深度、最大子节点数等关键参数
3. **性能监控**：启用性能分析功能，用于监控算法执行效率

#### 模板提取过程

```python
def extract_templates(log_list: list, save_pth: str):
    KEEP_TOP_N_TEMPLATE = 1000
    
    miner = init_drain()
    
    # 逐条处理日志消息
    for line in tqdm(log_list):
        log_txt = line.rstrip()
        miner.add_log_message(log_txt)
```

1. **逐条处理**：对每条日志消息调用`add_log_message()`方法
2. **增量学习**：Drain算法会自动判断该日志是否匹配现有模板，或需要创建新模板
3. **模板聚类**：相似的日志会被归类到同一个模板cluster中

**模板提取示例**：
从上述示例日志中，Drain可能提取出以下模板：
```
模板1: "<*> | INFO | <*> | <*> | redisservice1 | <*> | redis write success"
模板2: "<*> | INFO | <*> | <*> | redisservice1 | <*> | service accept, status_code: <*>"
模板3: "<*> | ERROR | <*> | <*> | dbservice1 | <*> | database connection failed"
```

其中`<*>`表示可变参数部分。

### 3.2.4 模板排序和筛选

```python
# 对聚类结果按大小降序排序
sorted_clusters = sorted(miner.drain.clusters, key=lambda it: it.size, reverse=True)
```

1. **按频率排序**：根据每个模板出现的频次进行降序排序
2. **筛选重要模板**：保留top 1000个最频繁的模板
3. **过滤噪声**：去除出现频次过低的模板，减少噪声影响

### 3.2.5 模板信息保存

```python
# 准备模板统计信息
template_ids = []    # 存储模板ID
template_counts = [] # 存储模板出现次数  
templates = []       # 存储模板内容

# 遍历排序后的聚类结果
for cluster in sorted_clusters:
    templates.append(cluster.get_template())  # 获取模板字符串
    template_ids.append(cluster.cluster_id)   # 记录模板ID
    template_counts.append(cluster.size)      # 记录模板出现次数

# 创建DataFrame保存模板信息
template_df = pd.DataFrame(data={
    'id': template_ids,      # 模板ID列
    'template': templates,   # 模板内容列
    'count': template_counts # 模板出现次数列
})

# 将模板信息保存到CSV文件
template_df.to_csv('./drain/gaia-template.csv', index=False)
```

**输出文件示例** (`gaia-template.csv`):
| id | template | count |
|----|----------|-------|
| 1  | `<*> \| INFO \| <*> \| <*> \| redisservice1 \| <*> \| redis write success` | 1250 |
| 2  | `<*> \| INFO \| <*> \| <*> \| redisservice1 \| <*> \| service accept, status_code: <*>` | 890 |
| 3  | `<*> \| ERROR \| <*> \| <*> \| dbservice1 \| <*> \| database connection failed` | 45 |

同时保存训练好的Drain模型到`drain/gaia-drain.pkl`文件，供后续的日志匹配使用。

## 3.3 模板匹配功能

`drain_template_extractor.py`中还提供了模板匹配功能，用于将新的日志消息匹配到已有的模板：

```python
def match_template(miner: drain3.TemplateMiner, log_list: list):
    IDs = []
    templates = []
    params = []

    for log in tqdm(log_list):
        cluster = miner.match(log)
        
        if cluster is None:
            # 无匹配模板
            IDs.append(None)
            templates.append(None)
        else:
            template = cluster.get_template()
            param = miner.get_parameter_list(template, log)

            IDs.append(cluster.cluster_id)
            templates.append(template)
            params.append(param)

    return IDs, templates, params
```

### 匹配过程示例

假设有新日志：`"2021-07-01 11:30:45,123 | INFO | 0.0.0.1 | 172.17.0.4 | redisservice1 | d890e12fb5c7896f | redis write success"`

匹配结果：
- **模板ID**: 1
- **匹配模板**: `<*> | INFO | <*> | <*> | redisservice1 | <*> | redis write success`
- **参数列表**: `["2021-07-01 11:30:45,123", "0.0.0.1", "172.17.0.4", "d890e12fb5c7896f"]`

## 3.4 配置文件说明

Drain算法的行为由`drain3.ini`配置文件控制，主要参数包括：

- **depth**: 解析树的深度
- **sim_th**: 相似度阈值，决定日志是否匹配现有模板
- **max_children**: 每个内部节点的最大子节点数
- **max_clusters**: 最大模板聚类数量

这些参数需要根据具体的日志格式和业务需求进行调优。

## 3.5 处理效果

通过Drain算法处理后，原始的非结构化日志被转换为：
1. **结构化模板**：便于模式识别和异常检测
2. **参数化表示**：将可变部分提取为参数
3. **统计信息**：每个模板的出现频次，用于识别常见和异常模式

这为后续的日志事件提取和异常检测奠定了基础。