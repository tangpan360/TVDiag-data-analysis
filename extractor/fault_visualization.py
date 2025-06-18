import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import time
from utils import io_util
from utils.time_util import *
import argparse
import warnings
warnings.filterwarnings('ignore')  # 忽略警告信息，使输出更清晰

# 支持中文显示配置
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为SimHei
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号，防止变成方框

# 减少图表四周的空白区域
plt.rcParams['figure.autolayout'] = True  # 自动调整布局
plt.rcParams['axes.xmargin'] = 0.02  # 减少x轴两侧的空白
plt.rcParams['axes.ymargin'] = 0.02  # 减少y轴两侧的空白

def timestamp_to_datetime(timestamp):
    """将时间戳转换为datetime对象，便于绘图
    
    Args:
        timestamp: 毫秒时间戳
        
    Returns:
        datetime: 转换后的datetime对象
    """
    # 将毫秒时间戳转换为秒，然后转为datetime对象
    return datetime.fromtimestamp(timestamp/1000)

def extract_data_around_fault(df, start_time, end_time, time_column='timestamp', window_minutes=40):
    """提取故障前后指定时间窗口的数据
    
    分别提取故障前、故障期间和故障后的数据，然后合并
    
    Args:
        df: 包含时间序列数据的DataFrame
        start_time: 故障开始时间戳（毫秒）
        end_time: 故障结束时间戳（毫秒）
        time_column: DataFrame中表示时间的列名
        window_minutes: 提取故障前后多长时间的数据（分钟）
        
    Returns:
        DataFrame: 包含故障前后数据的数据框，已按时间排序
    """
    # 将分钟转换为毫秒
    window_ms = window_minutes * 60 * 1000
    
    # 提取故障前的数据（故障开始前window_minutes分钟到故障开始）
    before_fault = df[(df[time_column] >= start_time - window_ms) & 
                      (df[time_column] <= start_time)]
    
    # 提取故障后的数据（故障结束到故障结束后window_minutes分钟）
    after_fault = df[(df[time_column] >= end_time) & 
                     (df[time_column] <= end_time + window_ms)]
    
    # 提取故障期间的数据
    during_fault = df[(df[time_column] >= start_time) & 
                      (df[time_column] <= end_time)]
    
    # 合并三部分数据
    # concat会自动保持原有顺序，不需要额外排序
    return pd.concat([before_fault, during_fault, after_fault])

def visualize_metrics(data, fault_info, save_dir='visualization_results'):
    """可视化指标数据，并标记故障时间段
    
    为每个节点的每个指标创建一个可视化图表，
    并用不同颜色的线标记故障开始和结束时间
    
    Args:
        data: 包含各节点各指标数据的嵌套字典，格式为:
             {pod_name: {metric_name: metric_df, ...}, ...}
        fault_info: 包含故障信息的字典，必须包含以下键:
             'st_time': 故障开始时间
             'ed_time': 故障结束时间
             'index': 故障ID
             'anomaly_type': 故障类型
             'instance': 故障实例
        save_dir: 保存可视化结果的目录
    """
    # 从故障信息中提取关键数据
    start_time = fault_info['st_time']
    end_time = fault_info['ed_time']
    fault_index = fault_info['index']
    fault_type = fault_info['anomaly_type']
    fault_instance = fault_info['instance']  # 获取故障实例信息
    
    # 创建按故障类型和索引组织的目录结构
    type_dir = os.path.join(save_dir, fault_type)
    index_dir = os.path.join(type_dir, f"索引{fault_index}")
    
    # 如果目录不存在，则创建
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    
    # 对每个节点的每个指标进行可视化
    for pod, metrics in data.items():
        print(f"正在处理节点 {pod} 的指标...")
        
        # 处理该节点的每个指标
        for metric_name, metric_df in metrics.items():
            # 跳过空数据集
            if len(metric_df) == 0:
                continue
                
            # 创建新图形，减少边距
            fig, ax = plt.subplots(figsize=(15, 5))
            plt.subplots_adjust(left=0.07, right=0.96, top=0.92, bottom=0.15)
            
            # 将时间戳转换为datetime对象便于绘图
            x = metric_df['timestamp'].apply(timestamp_to_datetime)
            y = metric_df['value']
            
            # 绘制指标数据曲线
            plt.plot(x, y, '-o', markersize=2, label=metric_name)
            
            # 将故障开始和结束时间戳转换为datetime对象
            fault_start = timestamp_to_datetime(start_time)
            fault_end = timestamp_to_datetime(end_time)
            
            # 用红色竖线标记故障开始时间
            plt.axvline(x=fault_start, color='red', linestyle='--', linewidth=2, label='故障开始')
            # 用蓝色竖线标记故障结束时间
            plt.axvline(x=fault_end, color='blue', linestyle='--', linewidth=2, label='故障结束')
            
            # 用红色半透明区域标记故障持续时间段
            plt.axvspan(fault_start, fault_end, alpha=0.1, color='red')
            
            # 设置x轴日期格式
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.gcf().autofmt_xdate(rotation=15)  # 减小日期标签旋转角度
            
            # 设置图表标题和坐标轴标签，添加故障实例信息
            plt.title(f'故障{fault_index} ({fault_type}) - 故障实例: {fault_instance} - {pod} - {metric_name}', pad=8)
            plt.xlabel('时间', labelpad=5)
            plt.ylabel('值', labelpad=5)
            
            # 将图例放在右上角，避免与故障实例信息重叠
            plt.legend(loc='upper right', fontsize=9, framealpha=0.7)
            
            plt.grid(True, alpha=0.3)  # 显示网格线，降低透明度
            
            # 添加故障实例信息的文本注解（左上角）
            plt.annotate(f'故障实例: {fault_instance}', 
                         xy=(0.02, 0.95), 
                         xycoords='axes fraction',
                         bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.3),
                         fontsize=9)
            
            # 保存图片到对应的子目录，使用紧凑布局
            save_path = os.path.join(index_dir, f"{pod}_{metric_name}.png")
            plt.savefig(save_path, bbox_inches='tight', dpi=120)
            plt.close(fig)  # 关闭图形，释放内存
            
            print(f"  - 已保存 {metric_name} 的可视化结果")

def process_metric_data(metric_data, fault_info):
    """处理指标数据，提取故障前后指定时间窗口的数据
    
    Args:
        metric_data: 原始指标数据字典，格式为:
                    {pod_name: {metric_name: metric_df, ...}, ...}
        fault_info: 包含故障信息的字典，必须包含:
                    'st_time': 故障开始时间
                    'ed_time': 故障结束时间
        
    Returns:
        dict: 处理后的数据字典，包含故障前后数据，与输入格式相同
    """
    # 获取故障的开始和结束时间
    start_time = fault_info['st_time']
    end_time = fault_info['ed_time']
    
    # 初始化结果字典
    processed_data = {}
    
    # 对每个节点的指标数据进行处理
    for pod, metrics in metric_data.items():
        processed_data[pod] = {}
        
        # 处理该节点的每个指标
        for metric_name, metric_df in metrics.items():
            # 提取故障前后40分钟的数据
            around_fault_df = extract_data_around_fault(
                metric_df, 
                start_time, 
                end_time
            )
            
            # 只保存非空的数据集
            if len(around_fault_df) > 0:
                processed_data[pod][metric_name] = around_fault_df
    
    return processed_data

def extract_anomaly_type(message):
    """根据消息内容提取故障类型
    
    Args:
        message: 故障消息内容
        
    Returns:
        str: 识别的故障类型
    """
    anomaly_types = {
        'login failure': ['QR code expired', 'login failure'],
        'memory_anomalies': ['memory_anomalies', 'high memory'],
        'file moving program': ['file moving'],
        'normal memory freed label': ['memory freed'],
        'access permission denied exception': ['permission denied', 'access permission']
    }
    
    # 逐一检查消息是否包含各类型的关键词
    for anomaly_type, keywords in anomaly_types.items():
        for keyword in keywords:
            if keyword.lower() in message.lower():
                return anomaly_type
    
    # 默认返回未知类型
    return "unknown"

def prepare_label_data(label_path):
    """准备标签数据，添加故障类型列
    
    Args:
        label_path: 标签数据文件路径
        
    Returns:
        DataFrame: 处理后的标签数据
    """
    # 读取故障标签数据
    print("正在读取故障标签数据...")
    label_df = pd.read_csv(label_path)
    
    # 将时间字符串转换为时间戳（毫秒）
    label_df['st_time'] = label_df['st_time'].apply(lambda x: time2stamp(str(x).split('.')[0]))
    label_df['ed_time'] = label_df['ed_time'].apply(lambda x: time2stamp(str(x).split('.')[0]))
    
    # 根据消息内容提取故障类型
    label_df['anomaly_type'] = label_df['message'].apply(extract_anomaly_type)
    
    return label_df

def main(args):
    """主函数，处理所有故障的指标数据并生成可视化结果"""
    # 准备标签数据
    label_df = prepare_label_data(args.label_path)
    
    # 筛选故障类型
    if args.anomaly_types:
        selected_types = args.anomaly_types.split(',')
        label_df = label_df[label_df['anomaly_type'].isin(selected_types)]
        print(f"已筛选故障类型: {selected_types}")
    
    # 筛选故障索引
    if args.indices:
        selected_indices = [int(idx) for idx in args.indices.split(',')]
        label_df = label_df[label_df['index'].isin(selected_indices)]
        print(f"已筛选故障索引: {selected_indices}")
    
    # 每种类型最多处理n个样本
    if args.num_per_type > 0:
        print(f"每种故障类型最多处理 {args.num_per_type} 个样本")
        # 按类型分组并限制每组数量
        sample_dfs = []
        for anomaly_type, group in label_df.groupby('anomaly_type'):
            sample_dfs.append(group.head(args.num_per_type))
        
        label_df = pd.concat(sample_dfs)
    
    # 检查是否还有故障需要处理
    if len(label_df) == 0:
        print("筛选后没有符合条件的故障，请调整筛选条件")
        return
    
    print(f"筛选后将处理 {len(label_df)} 个故障")
    
    # 确保主保存目录存在
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    
    # 读取指标数据
    print("正在读取指标数据...")
    metric_data = {}
    
    try:
        # 尝试从缓存文件加载指标数据，加快处理速度
        metric_data = io_util.load("MicroSS/processed_metric_data.pkl")
        print("成功从缓存文件加载指标数据")
    except:
        # 如果缓存文件不存在，从原始文件读取
        print("未找到缓存的指标数据，从原始文件读取...")
        
        # 定义需要处理的服务和对应的pod
        svcs = ['dbservice', 'mobservice', 'logservice', 'webservice', 'redisservice']
        pod_names = []
        for svc in svcs:
            pod1 = svc+'1'
            pod2 = svc+'2'
            pod_names.extend([pod1, pod2])
        
        # 遍历指标文件目录
        for f in os.listdir("MicroSS/metric"):
            # 解析文件名，获取pod、主机和指标信息
            splits = f.split('_')
            cur_pod, cur_host = splits[0], splits[1]
            
            # 跳过不需要处理的pod或重复文件
            if (cur_pod not in pod_names) or ('2021-07-15_2021-07-31' in f):
                continue
            
            # 提取指标名称
            metric_name = '_'.join(splits[2:-2])
            
            # 读取第一部分数据
            df1 = pd.read_csv(f'MicroSS/metric/{f}')
            
            # 构造第二部分数据的文件名
            next_name = f.replace(
                "2021-07-01_2021-07-15",
                "2021-07-15_2021-07-31"
            )
            
            # 尝试读取第二部分数据并合并
            try:
                df2 = pd.read_csv(f'MicroSS/metric/{next_name}')
                combined_df = pd.concat([df1, df2])
            except:
                # 如果第二部分不存在，只使用第一部分
                combined_df = df1
                print(f"警告：未找到文件 {next_name}")
            
            # 将数据保存到嵌套字典中
            key = cur_pod + '_' + cur_host
            if key not in metric_data:
                metric_data[key] = {}
            
            metric_data[key][metric_name] = combined_df
        
        # 缓存处理后的数据，避免下次重复处理
        io_util.save("MicroSS/processed_metric_data.pkl", metric_data)
    
    # 处理每个故障
    for _, fault in label_df.iterrows():
        # 创建包含当前故障信息的字典
        fault_info = {
            'index': fault['index'],
            'anomaly_type': fault['anomaly_type'],
            'st_time': fault['st_time'],
            'ed_time': fault['ed_time'],
            'instance': fault['instance']  # 添加故障实例信息
        }
        
        print(f"\n正在处理故障 {fault_info['index']} ({fault_info['anomaly_type']}) - 实例: {fault_info['instance']}...")
        
        # 提取故障前后40分钟的数据
        around_fault_data = process_metric_data(metric_data, fault_info)
        
        # 可视化数据
        visualize_metrics(around_fault_data, fault_info, args.save_dir)
        
        print(f"故障 {fault_info['index']} 的可视化处理完成")

def parse_args():
    """解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='故障数据可视化工具')
    
    parser.add_argument('--label_path', type=str, default="MicroSS/gaia.csv",
                        help='故障标签文件路径')
    parser.add_argument('--save_dir', type=str, default="visualization_results",
                        help='可视化结果保存目录')
    parser.add_argument('--anomaly_types', type=str, default="",
                        help='需要处理的故障类型，多个类型用逗号分隔，例如：login failure,memory_anomalies')
    parser.add_argument('--indices', type=str, default="",
                        help='需要处理的故障索引，多个索引用逗号分隔，例如：0,1,5')
    parser.add_argument('--num_per_type', type=int, default=1,
                        help='每种故障类型最多处理的样本数量，0表示处理所有')
    
    return parser.parse_args()

if __name__ == '__main__':
    # 解析命令行参数
    args = parse_args()
    
    # 记录开始时间，用于计算总处理时间
    start_time = time.time()
    
    # 执行主函数
    main(args)
    
    # 计算并打印总处理时间
    end_time = time.time()
    print(f"\n全部处理完成，总用时: {end_time - start_time:.2f}秒") 