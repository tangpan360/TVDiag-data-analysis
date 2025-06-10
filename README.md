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