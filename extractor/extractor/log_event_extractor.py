import pandas as pd
from tqdm import tqdm

from drain.drain_template_extractor import *


def processing_feature(svc: str, log: str, miner: drain3.TemplateMiner) -> dict:
    """处理单条日志，提取服务名和模板ID
    
    Args:
        svc (str): 服务名称
        log (str): 日志消息内容
        miner (drain3.TemplateMiner): Drain日志模板挖掘器
        
    Returns:
        dict: 包含服务名、模板ID和计数字典
    """
    # 使用Drain匹配日志模板
    cluster = miner.match(log)
    # 如果没有匹配到模板，ID设为-1
    if cluster is None:
        eventId = -1
    else:
        eventId = cluster.cluster_id
    res = {'service':svc,'id':eventId, 'count':1}
    return res

def extract_log_events(log_df: pd.DataFrame, miner: drain3.TemplateMiner, low_freq_p: float) -> list:
    """从日志数据中提取异常事件
    
    异常事件包括：
    1. 低频日志模板（出现频率低于low_freq_p）
    2. 包含错误关键词的日志模板（error/fail/exception）
    
    Args:
        log_df (pd.DataFrame): 包含timestamp, service, message的日志DataFrame
        miner (drain3.TemplateMiner): 预训练的Drain模板挖掘器
        low_freq_p (float): 低频模板的百分比阈值
        
    Returns:
        list: 异常事件列表，每个事件格式为[服务名, 模板ID]
    """
    # 按模板出现频率升序排序（低频在前）
    sorted_clusters = sorted(miner.drain.clusters, key=lambda it: it.size, reverse=False)
    
    # 错误日志关键词
    err_keywords = ['error', 'fail', 'exception']
    # 要选择的异常事件ID列表（初始包含未匹配的-1）
    select_events = ['-1']
    
    # 筛选异常模板
    for idx, c in enumerate(sorted_clusters):
        # 选择前low_freq_p百分比的低频模板
        if idx < int(low_freq_p * len(sorted_clusters)):
            select_events.append(c.cluster_id)
            continue
        # 选择包含错误关键词的模板
        for keyword in err_keywords:
            if keyword in c.get_template().lower():
                select_events.append(c.cluster_id)
                break

    # 按时间戳排序日志
    log_df.sort_values(by=['timestamp'], ascending=True, inplace=True)
    logs = log_df['message'].values
    svcs = log_df['service'].values

    # 处理每条日志，提取模板ID
    events_dict = {'service': [], 'id': [], 'count': []}
    for i, log in tqdm(enumerate(logs)):
        res = processing_feature(svcs[i], log, miner)
        events_dict['service'].append(res['service'])
        events_dict['id'].append(res['id'])
        events_dict['count'].append(res['count'])
    
    # 转换为DataFrame并筛选异常事件
    event_df = pd.DataFrame(events_dict)
    event_df = event_df[event_df['id'].isin(select_events)]
    
    # 按模板ID和服务名分组
    event_gp = event_df.groupby(['id', 'service'])
    # 生成最终事件列表[服务名, 模板ID]
    events = [[svc, str(event_id)] for (event_id, svc), _ in event_gp]

    return events
