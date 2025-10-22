from collections import defaultdict
import pandas as pd
import os
from tqdm import tqdm
import numpy as np

from extractor.metric_event_extractor import extract_metric_events
from extractor.trace_event_extractor import extract_trace_events
from extractor.log_event_extractor import extract_log_events
from utils import io_util

# 加载故障后的数据
failure_post_data: dict = io_util.load('MicroSS/post-data-10.pkl')
# 加载标签数据，并将第一列设置为索引
label_df = pd.read_csv('MicroSS/gaia.csv', index_col=0)

# 遍历每个故障事件
for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
    # 获取当前故障对应的数据块
    chunk = failure_post_data[idx]
    # 获取trace数据
    trace_df = chunk['trace']
    # 初始化服务列表和影响关系列表
    svcs = []
    influences = []

    # 构建节点到服务的映射关系
    node2svcs = defaultdict(list)
    # 遍历metric目录下的所有文件
    for f in os.listdir('./MicroSS/metric'):
        # 解析文件名获取服务名和主机名
        splits = f.split('_')
        svc, host = splits[0], splits[1]
        # 过滤掉系统服务
        if svc in ['system', 'redis', 'zookeeper', '.DS']:
            continue
        # 如果服务还未添加到该节点的服务列表中，则添加
        if svc not in node2svcs[host]:
            node2svcs[host].append(svc)
    
    # 处理每个节点上的服务关系
    for node, pods in node2svcs.items():
        # print(node)
        # print(pods)
        # print('============================')
        # 将当前节点的服务添加到总服务列表中
        svcs.extend(pods)
        # 为同一节点上的服务创建双向影响关系
        for i in range(len(pods)):
            for j in range(i + 1, len(pods)):
                influences.append([pods[i], pods[j]]) 
                influences.append([pods[j], pods[i]])
    # 对服务列表去重并排序
    svcs = list(set(svcs))
    svcs.sort()
    # print(svcs)
    # print(len(svcs))

    # 捕获服务调用关系
    edges = []
    # 定义调用关系的列名
    edge_columns = ['service_name', 'parent_name']
    # 从trace数据中提取调用关系。dropna(subnet=['parent_name'])：过滤None行。drop_duplicates(subset=edge_columns)：过滤重复行。
    calls = trace_df.dropna(subset=['parent_name']).drop_duplicates(subset=edge_columns)[edge_columns].values.tolist()
    # 将调用关系和影响关系合并
    calls.extend(influences)
    # 对合并后的关系去重    
    calls = pd.DataFrame(calls).drop_duplicates().reset_index(drop=True).values.tolist() # 去重
    # print(calls)
    # print(len(calls))
    
    # 将服务关系转换为索引形式
    for call in calls:
        source, target = call[1], call[0]
        source_idx, target_idx = svcs.index(source), svcs.index(target)
        edges.append([source_idx, target_idx])
    # 将处理结果保存到数据块中
    chunk['nodes'] = svcs
    chunk['edges'] = edges

############################################################################################################################
# 保存节点和边的关系数据
from tqdm import tqdm
edges = {}
nodes = {}
# 遍历所有故障事件
for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
    chunk = failure_post_data[idx]
    # 收集每个故障的边和节点信息
    edges[idx] = chunk['edges']
    nodes[idx] = chunk['nodes']
# 将结果保存为json文件
io_util.save_json('raw/nodes.json', nodes)
io_util.save_json('raw/edges.json', edges)