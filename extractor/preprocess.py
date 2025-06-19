# 导入必要的库
import pandas as pd
from collections import defaultdict
from tqdm import tqdm  # 用于显示进度条
from utils import io_util

# # 加载标签数据和预处理数据
# labels = pd.read_csv('MicroSS/gaia.csv')  # 读取标签数据
# failure_pre_data: dict = io_util.load('MicroSS/pre-data.pkl')  # 加载预处理数据
#
# # 初始化存储正常指标和追踪数据的容器
# normal_metrics = {}  # 存储各pod的指标数据
# normal_traces = defaultdict(list)  # 存储追踪数据，使用defaultdict自动初始化列表
#
# # 遍历标签数据，构建正常指标和追踪数据集
# for idx, row in tqdm(labels.iterrows(), total=labels.shape[0]):
#     if row['data_type'] == 'test':  # 跳过测试数据
#         continue
#     index = row['index']
#     chunk = failure_pre_data[index]  # 获取对应索引的数据块
#
#     # 处理指标数据
#     for pod, kpi_dic in chunk['metric'].items():
#         if pod not in normal_metrics.keys():
#             normal_metrics[pod] = defaultdict(list)  # 为每个pod初始化指标容器
#         for kpi, kpi_df in kpi_dic.items():
#             normal_metrics[pod][kpi].append(kpi_df)  # 收集各pod的指标数据
#
#     # 处理追踪数据
#     trace_df = chunk['trace']
#     # 从URL中提取操作名称（去掉查询参数）
#     trace_df['operation'] = trace_df['url'].str.split('?').str[0]
#     # 按父服务、目标服务和操作分组
#     trace_gp = trace_df.groupby(['parent_name', 'service_name', 'operation'])
#     for (src, dst, op), call_df in trace_gp:
#         name = src + '-' + dst + '-' + op  # 生成唯一标识符
#         normal_traces[name].append(call_df)  # 收集追踪数据
#
# # 合并各pod的指标数据
# for pod in normal_metrics.keys():
#     for kpi, kpi_dfs in normal_metrics[pod].items():
#         normal_metrics[pod][kpi] = pd.concat(kpi_dfs)  # 将列表中的DataFrame合并
#
# # 保存处理后的数据
# io_util.save('MicroSS/detector/normal_traces.pkl', normal_traces)
# io_util.save('MicroSS/detector/normal_metrics.pkl', normal_metrics)

############################################################################

# 导入异常检测相关库
import numpy as np
from sklearn.ensemble import IsolationForest  # 孤立森林异常检测算法
from extractor.trace_event_extractor import slide_window  # 滑动窗口函数
from utils import io_util
import time  # 用于计时

# 加载之前保存的正常数据
normal_traces = io_util.load('MicroSS/detector/normal_traces.pkl')
normal_metrics = io_util.load('MicroSS/detector/normal_metrics.pkl')

# 构建指标检测器（基于均值和标准差）
metric_detectors = {}
for pod in tqdm(normal_metrics.keys(), desc="Processing pods"):
    metric_detectors[pod] = {}
    for kpi, dfs in tqdm(normal_metrics[pod].items(), desc=f"Processing KPIs for {pod}", leave=False):
        # 为每个指标存储均值和标准差
        metric_detectors[pod][kpi] = [
            normal_metrics[pod][kpi]['value'].mean(), 
            normal_metrics[pod][kpi]['value'].std()
        ]

# 开始计时
st = time.time()

# 构建追踪检测器（使用孤立森林算法）
trace_detectors = {}
for name, call_dfs in normal_traces.items():
    # 初始化三种检测器：持续时间、500错误、400错误
    trace_detectors[name] = {
        'dur_detector': IsolationForest(random_state=0, n_estimators=5),
        '500_detector': IsolationForest(random_state=0, n_estimators=5),
        '400_detector': IsolationForest(random_state=0, n_estimators=5)
    }
    
    # 准备训练数据
    train_ds, train_500_ep, train_400_ep = [], [], []
    for call_df in call_dfs:
        # 使用滑动窗口提取特征
        _, durs, err_500_ps, err_400_ps = slide_window(call_df, 30 * 1000)
        train_ds.extend(durs)  # 持续时间特征
        train_500_ep.extend(err_500_ps)  # 500错误特征
        train_400_ep.extend(err_400_ps)  # 400错误特征
    
    # 如果没有数据则跳过
    if len(train_ds) == 0:
        continue
    
    # 获取检测器实例
    dur_clf = trace_detectors[name]['dur_detector']
    err_500_clf = trace_detectors[name]['500_detector']
    err_400_clf = trace_detectors[name]['400_detector']
    
    # 训练检测器
    dur_clf.fit(np.array(train_ds).reshape(-1,1))
    err_500_clf.fit(np.array(err_500_ps).reshape(-1,1))
    err_400_clf.fit(np.array(err_400_ps).reshape(-1,1))
    
    # 更新检测器
    trace_detectors[name]['dur_detector'] = dur_clf
    trace_detectors[name]['500_detector'] = err_500_clf
    trace_detectors[name]['400_detector'] = err_400_clf

# 结束计时
ed = time.time()

# 保存训练好的检测器
io_util.save('MicroSS/detector/trace-detector.pkl', trace_detectors)
io_util.save('MicroSS/detector/metric-detector-strict-host.pkl', metric_detectors)

# 打印训练耗时
print(ed-st)