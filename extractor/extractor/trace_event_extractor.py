import json
import os
import numpy as np

import pandas as pd
import utils.io_util as io_util
import utils.detect_util as d_util


def slide_window(df, win_size):
    """滑动窗口函数，用于计算时间窗口内的追踪指标
    
    Args:
        df: 包含追踪数据的DataFrame
        win_size: 窗口大小(毫秒)
        
    Returns:
        sts: 窗口开始时间数组
        ds: 窗口平均持续时间数组 
        err_500_ps: 窗口500错误数量数组
        err_400_ps: 窗口400错误数量数组
    """
    sts, ds, err_500_ps, err_400_ps=[], [], [], []
    # df_copy=df.copy()
    # df_copy['slide_duration']=df['duration'].rolling(window=10, min_periods=1).mean()
    
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
        # error_code_n = len(temp_df[~temp_df['status_code'].isin([200, 300])])
        
        # 统计500和400错误数量
        err_500_ps.append(len(temp_df[temp_df['status_code']==500]))
        err_400_ps.append(len(temp_df[temp_df['status_code']==400]))
        
        # 计算窗口平均持续时间
        ds.append(temp_df['duration'].mean())
        i+=win_size
        
    return np.array(sts), np.array(ds), np.array(err_500_ps), np.array(err_400_ps)



def extract_trace_events(df: pd.DataFrame, trace_detector: dict):
    """用孤立森林模型从追踪数据中提取异常事件
    
    Args:
        df: 包含追踪数据的DataFrame
        trace_detector: 预训练的异常检测器字典
        
    Returns:
        排序后的异常事件列表，格式为[源服务,目标服务,操作,异常类型]
    """
    events = []
    # 按时间戳排序
    df.sort_values(by=['timestamp'], inplace=True, ascending=True)
    
    # 从URL中提取操作名称(去掉查询参数)
    df['operation'] = df['url'].str.split('?').str[0]
    
    # 按父服务、目标服务和操作分组
    gp = df.groupby(['parent_name', 'service_name', 'operation'])
    events = []

    # 设置30秒的窗口大小
    win_size = 30 * 1000
    
    # 对每个调用关系进行异常检测
    for (src, dst, op), call_df in gp:
        name = src + '-' + dst +'-' + op
        test_df = call_df
        
        # 使用滑动窗口提取特征
        test_win_sts, test_durations, err_500_ps, err_400_ps = slide_window(test_df, win_size)
        
        if len(test_durations) > 0:
            # 使用孤立森林检测异常
            pd_idx = iforest(trace_detector[name]['dur_detector'], test_durations)
            err_500_idx = iforest(trace_detector[name]['500_detector'], err_500_ps)
            err_400_idx = iforest(trace_detector[name]['400_detector'], err_400_ps)

            # 记录检测到的异常事件
            if pd_idx != -1:
                events.append([test_win_sts[pd_idx], src, dst, op, 'PD'])  # 性能下降事件
            if err_500_idx != -1:
                events.append([test_win_sts[err_500_idx], src, dst, op, '500'])  # 500错误事件
            if err_400_idx != -1:
                events.append([test_win_sts[err_400_idx], src, dst, op, '400'])  # 400错误事件
            
    # 按时间排序并去掉时间戳
    events = sorted(events, key=lambda x: x[0])
    events = [x[1:] for x in events]
    return events


def iforest(detector, test_arr):
    """使用孤立森林模型进行异常检测
    
    Args:
        detector: 预训练的孤立森林模型
        test_arr: 待检测数据数组
        
    Returns:
        异常索引，若无异常返回-1
    """
    labels = detector.predict(test_arr.reshape(-1,1)).tolist()
    try:
        idx = labels.index(-1)  # -1表示异常
    except:
        return -1
    return idx