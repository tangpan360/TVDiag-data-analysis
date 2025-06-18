# 故障数据可视化工具使用说明

此工具用于可视化故障前后40分钟的数据，帮助分析故障影响。

## 功能特点

- 提取故障点前40分钟和后40分钟的数据
- 自动标记故障开始时间点（红色竖线）和结束时间点（蓝色竖线）
- 用红色半透明区域标记整个故障期间
- 支持中文显示
- 自动识别故障类型，支持按类型筛选可视化
- 支持限制每种故障类型可视化的数量
- 支持选择特定索引的故障进行可视化
- 按故障类型和故障索引组织结果文件夹，便于分析
- 为每个服务节点的每个指标生成单独的可视化图表
- 结果保存为图片，便于后续分析

## 故障类型识别

工具会自动根据消息内容提取故障类型，目前支持识别以下类型：
- login failure (登录失败，如二维码过期)
- memory_anomalies (内存异常)
- file moving program (文件移动程序)
- normal memory freed label (正常内存释放标签)
- access permission denied exception (访问权限拒绝异常)

## 使用方法

1. 确保您已有以下数据文件：
   - MicroSS/gaia.csv （故障标签数据）
   - MicroSS/metric/ （指标数据目录）

2. 基本运行方式：

```bash
cd 011-TVDiag-data-analysis
python extractor/fault_visualization.py
```

3. 高级使用方式（带参数）：

```bash
# 仅可视化指定类型的故障，每种类型最多2个
python extractor/fault_visualization.py --anomaly_types "memory_anomalies,file moving program" --num_per_type 2

# 仅可视化特定索引的故障
python extractor/fault_visualization.py --indices "0,5,9"

# 指定输出目录
python extractor/fault_visualization.py --save_dir "my_visualization_results"
```

4. 完整参数列表：

```
--label_path     故障标签文件路径，默认为"MicroSS/gaia.csv"
--save_dir       可视化结果保存目录，默认为"visualization_results"
--anomaly_types  需要处理的故障类型，多个类型用逗号分隔
--indices        需要处理的故障索引，多个索引用逗号分隔
--num_per_type   每种故障类型最多处理的样本数量，默认为1，0表示处理所有
```

## 输出结果组织结构

可视化结果按以下层次结构组织：

```
visualization_results/
├── 故障类型1/
│   ├── 索引0/
│   │   ├── pod1_metric1.png
│   │   ├── pod1_metric2.png
│   │   └── ...
│   └── 索引5/
│       ├── pod2_metric1.png
│       └── ...
├── 故障类型2/
│   ├── 索引1/
│   │   └── ...
│   └── ...
└── ...
```

每个图包含：
- 指标随时间变化的曲线
- 故障开始时间（红色虚线）
- 故障结束时间（蓝色虚线）
- 故障期间（红色半透明区域）

## 注意事项

- 首次运行时脚本会读取原始指标数据，可能需要较长时间
- 后续运行时会使用缓存的数据（MicroSS/processed_metric_data.pkl），加快处理速度
- 如果您更新了原始数据，请删除缓存文件以确保使用最新数据
- 使用筛选功能可以大大减少处理时间和输出量
- 默认每种故障类型只处理1个样本，可以通过`--num_per_type`参数调整

## 自定义选项

如需修改可视化参数，可以编辑以下内容：

- 时间窗口：修改`extract_data_around_fault`函数的`window_minutes`参数（默认40分钟）
- 图表尺寸：修改`visualize_metrics`函数中的`figsize`参数
- 输出目录：使用`--save_dir`参数或修改代码中的默认值
- 故障类型识别逻辑：修改`extract_anomaly_type`函数中的关键词列表 