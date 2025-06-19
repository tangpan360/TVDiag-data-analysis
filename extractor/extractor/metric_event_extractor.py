import json
import os
import pandas as pd


def extract_metric_events(pod_host: str, kpi_dic: dict, metric_detector: dict):
    """从不同的指标数据框中提取异常事件(使用3-sigma方法)
    
    参数:
        pod_host (str): 格式为"pod_host"的字符串，表示pod名称和主机名
        kpi_dic (dict): 包含多个KPI指标的字典，key为指标名，value为DataFrame
        metric_detector (dict): 每个KPI指标的检测器，包含均值和标准差
        
    返回:
        list: 排序后的异常事件列表，每个事件格式为[pod, host, kpi, direction]
    """
    events = []
    # 遍历每个KPI指标
    for kpi, df in kpi_dic.items():
        # 处理缺失值，用0填充
        df.fillna(0, inplace=True)
        # 按时间戳升序排序
        df.sort_values(by=['timestamp'], inplace=True, ascending=True)

        times = df['timestamp'].values
        # 跳过空数据
        if len(df) == 0:
            continue
            
        # 使用3-sigma方法检测异常
        ab_idx, ab_direction = k_sigma(
            detector=metric_detector[kpi],  # 当前KPI的检测器
            test_arr=df['value'].values,    # 当前KPI的值数组
            k=3,                            # 3倍标准差阈值
        )
        
        # 如果检测到异常
        if ab_idx != -1:
            ab_t = times[ab_idx]  # 异常时间点
            # 解析pod和host名称
            splits = pod_host.split('_')
            pod, host = splits[0], splits[1]
            # 记录异常事件[时间, pod, host, 指标名, 异常方向]
            events.append([ab_t, pod, host, kpi, ab_direction])
            
    # 按时间戳排序所有事件
    sorted_events = sorted(events, key=lambda e: e[0])
    # 移除时间戳，只保留[pod, host, kpi, direction]
    sorted_events = [e[1:] for e in sorted_events]
    return sorted_events


def k_sigma(detector, test_arr, k=3):
    """使用k-sigma方法检测异常值
    
    参数:
        detector (tuple): 包含(均值, 标准差)的元组
        test_arr (array): 待检测的数值数组
        k (int): 标准差倍数阈值，默认为3
        
    返回:
        tuple: (异常索引, 异常方向) 或 (-1, None)表示无异常
    """
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
