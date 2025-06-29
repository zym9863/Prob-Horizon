"""
中心极限定理模拟器核心逻辑
Central Limit Theorem Simulator Core Logic
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Any
import pandas as pd


class CLTSimulator:
    """中心极限定理模拟器"""
    
    def __init__(self):
        self.distributions = {
            "均匀分布": {"func": stats.uniform, "params": {"loc": 0, "scale": 1}},
            "正态分布": {"func": stats.norm, "params": {"loc": 0, "scale": 1}},
            "指数分布": {"func": stats.expon, "params": {"scale": 1}},
            "泊松分布": {"func": stats.poisson, "params": {"mu": 3}},
            "伽马分布": {"func": stats.gamma, "params": {"a": 2, "scale": 1}},
            "贝塔分布": {"func": stats.beta, "params": {"a": 2, "b": 5}},
            "卡方分布": {"func": stats.chi2, "params": {"df": 3}},
            "二项分布": {"func": stats.binom, "params": {"n": 10, "p": 0.3}}
        }
    
    def get_distribution_info(self, dist_name: str) -> Dict[str, Any]:
        """获取分布信息"""
        if dist_name not in self.distributions:
            raise ValueError(f"不支持的分布: {dist_name}")
        
        dist_info = self.distributions[dist_name]
        dist = dist_info["func"](**dist_info["params"])
        
        # 计算理论统计量
        try:
            mean = dist.mean()
            var = dist.var()
            std = dist.std()
        except:
            # 对于某些分布，可能需要特殊处理
            mean = np.nan
            var = np.nan
            std = np.nan
        
        return {
            "name": dist_name,
            "distribution": dist,
            "params": dist_info["params"],
            "theoretical_mean": mean,
            "theoretical_var": var,
            "theoretical_std": std
        }
    
    def generate_population_sample(self, dist_name: str, size: int = 10000) -> np.ndarray:
        """生成总体样本"""
        dist_info = self.get_distribution_info(dist_name)
        return dist_info["distribution"].rvs(size=size)
    
    def simulate_sampling(self, dist_name: str, sample_size: int, 
                         num_samples: int) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        模拟抽样过程
        
        Args:
            dist_name: 分布名称
            sample_size: 每次抽样的样本大小
            num_samples: 抽样次数
            
        Returns:
            sample_means: 样本均值数组
            statistics: 统计信息字典
        """
        dist_info = self.get_distribution_info(dist_name)
        distribution = dist_info["distribution"]
        
        # 进行多次抽样
        sample_means = []
        for _ in range(num_samples):
            sample = distribution.rvs(size=sample_size)
            sample_means.append(np.mean(sample))
        
        sample_means = np.array(sample_means)
        
        # 计算样本均值的统计量
        sample_mean_mean = np.mean(sample_means)
        sample_mean_var = np.var(sample_means, ddof=1)
        sample_mean_std = np.std(sample_means, ddof=1)
        
        # 理论值（根据中心极限定理）
        theoretical_mean = dist_info["theoretical_mean"]
        theoretical_std_of_means = dist_info["theoretical_std"] / np.sqrt(sample_size)
        
        statistics = {
            "sample_mean_mean": sample_mean_mean,
            "sample_mean_var": sample_mean_var,
            "sample_mean_std": sample_mean_std,
            "theoretical_mean": theoretical_mean,
            "theoretical_std_of_means": theoretical_std_of_means,
            "sample_size": sample_size,
            "num_samples": num_samples
        }
        
        return sample_means, statistics
    
    def calculate_normality_test(self, sample_means: np.ndarray) -> Dict[str, float]:
        """计算正态性检验"""
        try:
            # Shapiro-Wilk检验
            shapiro_stat, shapiro_p = stats.shapiro(sample_means)
            
            # Kolmogorov-Smirnov检验
            ks_stat, ks_p = stats.kstest(sample_means, 'norm', 
                                        args=(np.mean(sample_means), np.std(sample_means)))
            
            return {
                "shapiro_statistic": shapiro_stat,
                "shapiro_p_value": shapiro_p,
                "ks_statistic": ks_stat,
                "ks_p_value": ks_p
            }
        except Exception as e:
            return {
                "shapiro_statistic": np.nan,
                "shapiro_p_value": np.nan,
                "ks_statistic": np.nan,
                "ks_p_value": np.nan,
                "error": str(e)
            }
    
    def get_distribution_description(self, dist_name: str) -> str:
        """获取分布的中文描述"""
        descriptions = {
            "均匀分布": "在固定区间内每个值出现的概率相等，如掷骰子的结果。",
            "正态分布": "钟形分布，许多自然现象都遵循正态分布，如身高、体重等。",
            "指数分布": "描述事件发生的时间间隔，如客户到达时间、设备故障间隔等。",
            "泊松分布": "描述固定时间或空间内事件发生的次数，如每小时接到的电话数。",
            "伽马分布": "连续概率分布，常用于描述等待时间，如等待第k个事件发生的时间。",
            "贝塔分布": "定义在[0,1]区间的连续分布，常用于描述概率或比例。",
            "卡方分布": "统计学中重要的分布，常用于假设检验和置信区间估计。",
            "二项分布": "描述n次独立试验中成功次数的分布，如抛硬币正面朝上的次数。"
        }
        return descriptions.get(dist_name, "暂无描述")
    
    def get_available_distributions(self) -> List[str]:
        """获取可用的分布列表"""
        return list(self.distributions.keys())
