import pandas as pd
from drain.drain_template_extractor import *
from utils import io_util
from tqdm import tqdm  # 用于显示进度条

# 加载预处理后的日志数据和标签数据
data: dict = io_util.load('MicroSS/post-data-10.pkl')  # 加载预处理后的数据字典
label_df = pd.read_csv('MicroSS/gaia.csv', index_col=0)  # 加载标签数据，第一列作为索引

# 收集所有训练集的日志消息
logs = []
for idx, row in tqdm(label_df.iterrows(), total=label_df.shape[0]):
    if row['data_type'] == 'test':  # 跳过测试数据
        continue
    chunk = data[idx]  # 获取当前索引对应的数据块
    logs.extend(chunk['log']['message'].values.tolist())  # 收集日志消息

# 使用Drain算法提取日志模板
miner = extract_templates(
    log_list=logs,  # 传入所有日志消息列表
    save_pth='drain/gaia-drain.pkl'  # 保存训练好的Drain模型路径
)
# 也可以直接加载已训练的模型:
# miner = io_util.load('drain/gaia-drain.pkl')

# 对聚类结果按大小降序排序
sorted_clusters = sorted(miner.drain.clusters, key=lambda it: it.size, reverse=True)

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
