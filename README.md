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

## 数据集下载

在开始数据处理之前，首先需要下载GAIA数据集。使用以下命令下载数据集：

```bash
git clone --branch release-v1.0 https://github.com/CloudWise-OpenSource/GAIA-DataSet.git
```

该命令会直接克隆仓库并检出到 `release-v1.0` 标签所指向的代码状态，下载完成后会得到完整的GAIA数据集文件。

## 数据完整性校验

为确保下载的数据集完整性，建议在解压数据前进行MD5校验和验证。

### 1. 放置校验和文件

将提供的`checksums.md5`文件放置到MicroSS目录中：

```bash
# 将checksums.md5文件复制到MicroSS目录
cp checksums.md5 GAIA-DataSet/MicroSS/
```

### 2. 验证数据完整性

进入MicroSS目录并执行校验：

```bash
cd GAIA-DataSet/MicroSS
md5sum -c checksums.md5
```

### 3. 校验结果说明

- **验证成功**：所有文件显示"OK"，表示数据完整
- **验证失败**：显示"FAILED"的文件需要重新下载

**示例输出**：
```bash
business/business_split.z01: OK
business/business_split.z02: OK
...
metric/metric_split.z01: OK
...
run/run.zip: OK
...
trace/trace_split.z01: OK
...
MicroSS system description.docx: OK
```

**注意**：校验和文件包含83个文件的MD5值，包括：
- Business目录：32个文件
- Metric目录：17个文件  
- Run目录：1个文件
- Trace目录：32个文件
- 文档文件 (MicroSS system description.docx)：1个文件 (这个实际不需要，校验完删除即可)

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

windows直接解压 `.zip` 文件即可，压缩工具会自动识别并合并所有分卷文件。

ubuntu上推荐使用7z解压，安装 7zip（如未安装）：
```bash
sudo apt install p7zip-full  # Ubuntu/Debian
```
在business文件夹中解压：
```bash
7z x business_split.zip
```
在metric文件夹中解压：
```bash
7z x metric_split.zip
```
在run文件夹中解压：
```bash
7z x run.zip
```
在trace文件夹中解压：
```bash
7z x trace_split.zip
```

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

# 4. event_extractor.py 异常事件提取

`event_extractor.py`是TVDiag数据处理流程的第四步，也是关键的异常检测环节。该文件负责整合和协调三种不同类型的事件提取器，从多维度监控数据中提取关键的异常事件，为后续故障诊断提供基础支撑。

## 4.1 整体处理流程

`event_extractor.py`的核心功能是对监控数据进行异常事件提取，大致流程如下：

```python
# 加载预处理后的监控数据和标签数据
data: dict = io_util.load('MicroSS/post-data-10.pkl')
label_df = pd.read_csv('MicroSS/gaia.csv', index_col=0)

# 加载预训练好的异常检测器
metric_detectors = io_util.load('MicroSS/detector/metric-detector-strict-host.pkl')
trace_detectors = io_util.load('MicroSS/detector/trace-detector.pkl')
```

1. **加载数据和检测器**：
   - 加载故障后的监控数据(`post-data-10.pkl`)
   - 加载标签数据(`gaia.csv`)
   - 加载之前在`preprocess.py`中训练好的指标和追踪异常检测器

2. **初始化存储容器**：
   ```python
   metric_events_dic = defaultdict(list)  # 存储各时间点的指标异常事件
   trace_events_dic = defaultdict(list)    # 存储各时间点的追踪异常事件
   log_events_dic = defaultdict(list)     # 存储各时间点的日志异常事件
   ```

3. **遍历故障时间点**：
   ```python
   for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
       chunk = data[idx]  # 获取当前时间点的数据块
   ```

   对每个标记的故障时间点，分别执行三种事件提取。

4. **保存提取结果**：
   ```python
   io_util.save_json('events/log/log.json', log_events_dic)
   io_util.save_json('events/metric/metric.json', metric_events_dic)
   io_util.save_json('events/trace/trace.json', trace_events_dic)
   ```

## 4.2 指标异常事件提取

指标异常事件提取基于3-sigma规则，检测指标值是否超出正常范围：

```python
# 提取指标异常事件
st = time.time()
metric_events = []
# 遍历每个pod-host组合的指标数据
for pod_host, kpi_dic in chunk['metric'].items():
    # 使用3-sigma方法检测异常指标
    kpi_events = extract_metric_events(pod_host, kpi_dic, metric_detectors[pod_host])
    metric_events.extend(kpi_events)
metric_costs.append(time.time()-st)  # 记录耗时
metric_events_dic[idx] = metric_events  # 存储当前时间点的指标异常
```

### 4.2.1 3-Sigma异常检测方法

`metric_event_extractor.py`中的`k_sigma`函数实现了3-sigma异常检测：

```python
def k_sigma(detector, test_arr, k=3):
    """使用k-sigma方法检测异常值"""
    mean = detector[0]  # 均值
    std = detector[1]   # 标准差
    # 计算上下界
    up, lb = mean + k * std, mean - k * std

    # 遍历测试数组
    for idx, v in enumerate(test_arr.tolist()):
        if v > up:  # 高于上界
            return idx, 'up'    # 返回异常索引和方向
        elif v < lb:  # 低于下界
            return idx, 'down'
    
    # 无异常
    return -1, None
```

**处理示例**：
假设某个指标的正常均值和标准差为：`mean=10, std=2`，那么:
- 上界: `up = 10 + 3*2 = 16`
- 下界: `lb = 10 - 3*2 = 4`

对于测试数据`[7, 9, 15, 18, 8]`，第3个值(18)超过了上界(16)，因此会被检测为向上异常(`up`)。

### 4.2.2 指标异常事件格式

每个检测到的指标异常事件格式为`[pod, host, kpi, direction]`，例如：
```
["dbservice1", "0.0.0.4", "docker_memory_stats_rss", "up"]
```

这表示`dbservice1`服务在主机`0.0.0.4`上的`docker_memory_stats_rss`指标异常上升。

## 4.3 追踪异常事件提取

追踪异常事件提取基于孤立森林算法，检测服务间调用的异常模式：

```python
# 提取追踪异常事件
st = time.time()
# 使用孤立森林检测追踪异常(性能下降、500/400错误)
trace_events = extract_trace_events(chunk['trace'], trace_detectors)
trace_events_dic[idx] = trace_events
trace_costs.append(time.time()-st)
```

### 4.3.1 滑动窗口特征提取

`trace_event_extractor.py`中的`slide_window`函数先对追踪数据进行特征提取：

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
```

对每个30秒的时间窗口，计算三类特征：
- 平均响应时间
- 500错误数量
- 400错误数量

### 4.3.2 孤立森林异常检测

使用预训练的孤立森林模型检测异常特征：

```python
def iforest(detector, test_arr):
    """使用孤立森林模型进行异常检测"""
    labels = detector.predict(test_arr.reshape(-1,1)).tolist()
    try:
        idx = labels.index(-1)  # -1表示异常
    except:
        return -1
    return idx
```

孤立森林算法基于"隔离"原理，异常点通常更容易被孤立出来。

### 4.3.3 追踪异常事件格式

每个检测到的追踪异常事件格式为`[源服务, 目标服务, 操作, 异常类型]`，例如：
```
["webservice1", "dbservice1", "http://0.0.0.1:9379/db_query", "PD"]
```

这表示从`webservice1`到`dbservice1`的`db_query`操作出现了性能下降(PD)。异常类型包括：
- `PD`: 性能下降(Performance Degradation)
- `500`: HTTP 500错误
- `400`: HTTP 400错误

## 4.4 日志异常事件提取

日志异常事件提取基于两种规则：低频模板和错误模板：

```python
# 提取日志异常事件
st = time.time()
miner = io_util.load('./drain/gaia-drain.pkl')  # 加载预训练的Drain日志模板挖掘器
log_df = chunk['log']  # 获取当前时间点的日志数据
# 检测低频日志模板和错误日志(阈值设为0.5)
log_events = extract_log_events(log_df, miner, 0.5)
log_events_dic[idx] = log_events
log_costs.append(time.time()-st)
```

### 4.4.1 日志异常判定规则

`log_event_extractor.py`使用两种规则判定日志异常：

```python
# 筛选异常模板
for idx, c in enumerate(sorted_clusters):
    # 1. 选择前low_freq_p百分比的低频模板
    if idx < int(low_freq_p * len(sorted_clusters)):
        select_events.append(c.cluster_id)
        continue
    # 2. 选择包含错误关键词的模板
    for keyword in err_keywords:
        if keyword in c.get_template().lower():
            select_events.append(c.cluster_id)
            break
```

1. **低频模板**: 出现频率低于阈值(0.5)的模板被视为异常
2. **错误关键词**: 包含"error"、"fail"或"exception"关键词的模板被视为异常

### 4.4.2 日志模板匹配流程

每条日志消息通过以下步骤进行处理：
1. 使用预训练的Drain模型匹配日志模板
2. 如果没有匹配到模板，赋予特殊ID `-1`
3. 筛选出满足异常条件的模板ID
4. 按模板ID和服务名分组统计

### 4.4.3 日志异常事件格式

每个检测到的日志异常事件格式为`[服务名, 模板ID]`，例如：
```
["dbservice1", "35"]
```

这表示`dbservice1`服务产生了ID为`35`的异常日志模板。

## 4.5 事件提取效率分析

代码中还记录了三类事件提取的平均耗时：
```python
print(f'the time cost of extract metric events is {metric_time}')
print(f'the time cost of extract trace events is {trace_time}')
print(f'the time cost of extract log events is {log_time}')
```

**运行结果**：
- 指标事件提取: 0.18秒/故障点
- 追踪事件提取: 0.23秒/故障点
- 日志事件提取: 0.66秒/故障点

日志事件提取耗时最长，这主要是由于日志模板匹配的复杂性。

## 4.6 异常事件存储

最终，所有提取的异常事件按照类型分别存储为JSON文件：

```python
# 创建存储目录
import os
os.makedirs('events/log', exist_ok=True)
os.makedirs('events/metric', exist_ok=True)
os.makedirs('events/trace', exist_ok=True)

# 保存各类异常事件数据
io_util.save_json('events/log/log.json', log_events_dic)
io_util.save_json('events/metric/metric.json', metric_events_dic)
io_util.save_json('events/trace/trace.json', trace_events_dic)
```

### 4.6.1 输出JSON示例

**指标异常(metric.json)**:
```json
{
  "0": [
    ["dbservice1", "0.0.0.4", "docker_memory_stats_rss", "up"],
    ["webservice1", "0.0.0.1", "docker_cpu_total", "up"]
  ],
  "1": [
    ["redisservice1", "0.0.0.2", "docker_memory_limit", "down"]
  ]
}
```

**追踪异常(trace.json)**:
```json
{
  "0": [
    ["webservice1", "dbservice1", "http://0.0.0.1:9379/db_query", "PD"],
    ["mobservice1", "redisservice1", "http://0.0.0.3:9377/redis_write", "500"]
  ],
  "1": [
    ["webservice2", "logservice1", "http://0.0.0.5:9378/log_write", "400"]
  ]
}
```

**日志异常(log.json)**:
```json
{
  "0": [
    ["dbservice1", "35"],
    ["redisservice1", "42"]
  ],
  "1": [
    ["logservice1", "17"]
  ]
}
```

这些异常事件文件构成了故障诊断的重要依据，下一步将用于构建故障依赖图和定位故障根因。

# 5. deployment_extractor.py 服务依赖关系提取

`deployment_extractor.py`是TVDiag数据处理流程的第五步，也是最后一个预处理步骤。该文件的主要功能是构建微服务系统的依赖关系图，将物理部署信息和服务调用关系结合起来，为后续的故障诊断和根因定位提供拓扑结构支持。

## 5.1 整体处理流程

`deployment_extractor.py`的核心任务是构建服务依赖关系图，处理流程如下：

```python
# 加载故障后的数据
failure_post_data: dict = io_util.load('MicroSS/post-data-10.pkl')
# 加载标签数据，并将第一列设置为索引
label_df = pd.read_csv('MicroSS/gaia.csv', index_col=0)
```

1. **加载数据**：
   - 加载故障后的监控数据(`post-data-10.pkl`)
   - 加载标签数据(`gaia.csv`)

2. **遍历故障事件**：
   ```python
   for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
       # 获取当前故障对应的数据块
       chunk = failure_post_data[idx]
       # 获取trace数据
       trace_df = chunk['trace']
   ```

## 5.2 构建节点到服务的映射关系

首先，通过分析指标文件名提取节点上部署的服务信息：

```python
# 构建节点到服务的映射关系
node2svcs = defaultdict(list)
# 遍历metric目录下的所有文件
for f in os.listdir('./MicroSS/metric'):
    # 解析文件名获取服务名和主机名
    splits = f.split('_')
    svc, host = splits[0], splits[1]
    # 过滤掉系统服务
    if svc in ['system', 'redis', 'zookeeper']:
        continue
    # 如果服务还未添加到该节点的服务列表中，则添加
    if svc not in node2svcs[host]:
        node2svcs[host].append(svc)
```

该步骤通过分析指标文件名(如`dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv`)提取服务名和主机名，并构建从主机到服务的映射关系。

### 5.2.1 节点到服务映射示例

对于以下指标文件：
```
dbservice1_0.0.0.4_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv
webservice1_0.0.0.1_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv
mobservice2_0.0.0.2_docker_cpu_core_0_pct_2021-07-01_2021-07-15.csv
```

构建的映射关系为：
```
{
    '0.0.0.4': ['dbservice1'],
    '0.0.0.1': ['webservice1'],
    '0.0.0.2': ['mobservice2']
}
```

## 5.3 捕获同一节点上服务的影响关系

接下来，为同一节点上的服务创建双向影响关系：

```python
# 处理每个节点上的服务关系
for node, pods in node2svcs.items():
    # 将当前节点的服务添加到总服务列表中
    svcs.extend(pods)
    # 为同一节点上的服务创建双向影响关系
    for i in range(len(pods)):
        for j in range(i + 1, len(pods)):
            influences.append([pods[i], pods[j]]) 
            influences.append([pods[j], pods[i]])
```

这一步骤基于这样的假设：部署在同一节点上的服务可能会相互影响。例如，如果一个服务占用了大量CPU或内存资源，可能会影响同一节点上的其他服务。

### 5.3.1 同节点服务影响关系示例

假设在节点`0.0.0.3`上部署了`dbservice2`和`logservice1`两个服务，则生成的影响关系为：
```
['dbservice2', 'logservice1']
['logservice1', 'dbservice2']
```

## 5.4 捕获服务调用关系

然后，从追踪数据中提取服务间的调用关系：

```python
# 捕获服务调用关系
edges = []
# 定义调用关系的列名
edge_columns = ['service_name', 'parent_name']
# 从trace数据中提取调用关系，并去重
calls = trace_df.dropna(subset=['parent_name']).drop_duplicates(subset=edge_columns)[edge_columns].values.tolist()
# 将调用关系和影响关系合并
calls.extend(influences)
# 对合并后的关系去重    
calls = pd.DataFrame(calls).drop_duplicates().reset_index(drop=True).values.tolist()
```

这一步从追踪数据中提取服务间的调用关系，并与之前识别的同节点影响关系合并，形成完整的服务依赖图。

### 5.4.1 服务调用关系示例

假设追踪数据包含以下调用关系：
```
['dbservice1', 'webservice1']  # dbservice1被webservice1调用
['redisservice1', 'mobservice2']  # redisservice1被mobservice2调用
```

合并同节点影响关系后可能形成如下依赖关系：
```
['dbservice1', 'webservice1']
['redisservice1', 'mobservice2']
['dbservice2', 'logservice1']
['logservice1', 'dbservice2']
```

## 5.5 将服务关系转换为索引形式

最后，将服务名转换为索引形式，以便于图算法处理：

```python
# 将服务关系转换为索引形式
for call in calls:
    source, target = call[1], call[0]
    source_idx, target_idx = svcs.index(source), svcs.index(target)
    edges.append([source_idx, target_idx])
# 将处理结果保存到数据块中
chunk['nodes'] = svcs
chunk['edges'] = edges
```

这一步将服务名替换为其在服务列表中的索引位置，便于后续图算法处理。

### 5.5.1 索引转换示例

假设服务列表和关系如下：
```
svcs = ['webservice1', 'dbservice1', 'mobservice2', 'redisservice1', 'logservice1', 'dbservice2']
calls = [
    ['dbservice1', 'webservice1'],
    ['redisservice1', 'mobservice2']
]
```

转换后的边为：
```
edges = [
    [0, 1],  # webservice1 -> dbservice1
    [2, 3]   # mobservice2 -> redisservice1
]
```

## 5.6 保存服务依赖关系

处理完所有故障事件后，将节点和边的关系数据保存为JSON文件：

```python
# 保存节点和边的关系数据
edges = {}
nodes = {}
# 遍历所有故障事件
for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
    chunk = failure_post_data[idx]
    # 收集每个故障的边和节点信息
    edges[idx] = chunk['edges']
    nodes[idx] = chunk['nodes']
# 将结果保存为json文件
io_util.save_json('MicroSS/nodes.json', nodes)
io_util.save_json('MicroSS/edges.json', edges)
```

### 5.6.1 输出JSON示例

**nodes.json**:
```json
{
  "0": ["webservice1", "dbservice1", "mobservice2", "redisservice1", "logservice1"],
  "1": ["webservice2", "dbservice2", "mobservice1", "redisservice2"]
}
```

**edges.json**:
```json
{
  "0": [
    [0, 1],  // webservice1 -> dbservice1
    [2, 3],  // mobservice2 -> redisservice1
    [1, 4]   // dbservice1 -> logservice1
  ],
  "1": [
    [0, 1],  // webservice2 -> dbservice2
    [0, 2]   // webservice2 -> mobservice1
  ]
}
```

## 5.7 服务依赖图构建方法分析

`deployment_extractor.py`采用了两种方法来构建服务依赖图：

1. **物理部署依赖**：
   - 基于服务的部署位置
   - 同一节点上的服务之间存在双向影响关系
   - 优点：反映了资源竞争问题
   - 缺点：可能引入不必要的依赖

2. **服务调用依赖**：
   - 基于服务间的实际调用关系
   - 从追踪数据中提取
   - 优点：反映了实际的服务交互
   - 缺点：可能因为追踪数据不完整而遗漏依赖

通过合并这两类依赖关系，`deployment_extractor.py`构建了一个更全面的服务依赖图，为后续的故障传播分析和根因定位提供了拓扑基础。

## 5.8 服务依赖图的应用

服务依赖图在微服务系统的故障诊断中具有重要意义：

1. **故障传播分析**：
   - 依赖关系决定了故障可能的传播路径
   - 帮助识别故障的级联效应

2. **根因定位**：
   - 结合异常事件和依赖图，可以推断最初的故障源
   - 区分直接原因和间接影响

3. **故障模式匹配**：
   - 不同类型的故障在依赖图上表现出不同的异常模式
   - 可用于识别重复出现的故障类型

4. **系统健康监控**：
   - 依赖图可用于预测潜在的脆弱点
   - 指导监控资源的优化分配

通过这种方式构建的服务依赖图是TVDiag系统进行故障诊断和根因分析的基础框架。