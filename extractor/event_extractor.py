from collections import defaultdict
import pandas as pd
import time
from tqdm import tqdm
import numpy as np

# 导入各类型事件提取器
from extractor.metric_event_extractor import extract_metric_events
from extractor.trace_event_extractor import extract_trace_events
from extractor.log_event_extractor import extract_log_events
from utils import io_util

# 加载预处理后的监控数据和标签数据
data: dict = io_util.load('MicroSS/post-data-10.pkl')  # 加载预处理后的监控数据
label_df = pd.read_csv('MicroSS/gaia.csv', index_col=0)  # 加载标签数据，第一列作为索引

# 加载预训练好的异常检测器
metric_detectors = io_util.load('MicroSS/detector/metric-detector-strict-host.pkl')  # 指标异常检测器
trace_detectors = io_util.load('MicroSS/detector/trace-detector.pkl')  # 追踪异常检测器

# 初始化存储各类事件和耗时的字典
metric_events_dic = defaultdict(list)  # 存储各时间点的指标异常事件
trace_events_dic = defaultdict(list)    # 存储各时间点的追踪异常事件
log_events_dic = defaultdict(list)     # 存储各时间点的日志异常事件
metric_costs, trace_costs, log_costs = [], [], []  # 存储各类事件提取耗时

# 遍历所有时间点的数据
for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
    chunk = data[idx]  # 获取当前时间点的数据块
    
    # 1. 提取指标异常事件
    st = time.time()
    metric_events = []
    # 遍历每个pod-host组合的指标数据
    for pod_host, kpi_dic in chunk['metric'].items():
        # 使用3-sigma方法检测异常指标
        kpi_events = extract_metric_events(pod_host, kpi_dic, metric_detectors[pod_host])
        metric_events.extend(kpi_events)
    metric_costs.append(time.time()-st)  # 记录耗时
    metric_events_dic[idx] = metric_events  # 存储当前时间点的指标异常
    
    # 2. 提取追踪异常事件
    st = time.time()
    # 使用孤立森林检测追踪异常(性能下降、500/400错误)
    trace_events = extract_trace_events(chunk['trace'], trace_detectors)
    trace_events_dic[idx] = trace_events
    trace_costs.append(time.time()-st)
    
    # 3. 提取日志异常事件
    st = time.time()
    miner = io_util.load('./drain/gaia-drain.pkl')  # 加载预训练的Drain日志模板挖掘器
    log_df = chunk['log']  # 获取当前时间点的日志数据
    # 检测低频日志模板和错误日志(阈值设为0.5)
    log_events = extract_log_events(log_df, miner, 0.5)
    log_events_dic[idx] = log_events
    log_costs.append(time.time()-st)

# 计算各类事件的平均提取耗时
metric_time = np.mean(metric_costs)
trace_time = np.mean(trace_costs)
log_time = np.mean(log_costs)
print(f'the time cost of extract metric events is {metric_time}')
print(f'the time cost of extract trace events is {trace_time}')
print(f'the time cost of extract log events is {log_time}')
# the time cost of extract metric events is 0.18307018280029297
# the time cost of extract trace events is 0.23339865726162023
# the time cost of extract log events is 0.6638196256618483

# 创建存储目录(如果不存在)
import os
os.makedirs('events/log', exist_ok=True)    # 日志事件目录
os.makedirs('events/metric', exist_ok=True) # 指标事件目录
os.makedirs('events/trace', exist_ok=True)  # 追踪事件目录

# 保存各类异常事件数据
io_util.save_json('events/log/log.json', log_events_dic)      # 保存日志异常
io_util.save_json('events/metric/metric.json', metric_events_dic)  # 保存指标异常
io_util.save_json('events/trace/trace.json', trace_events_dic)    # 保存追踪异常