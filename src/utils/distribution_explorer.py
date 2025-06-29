"""
概率分布探索器核心逻辑
Probability Distribution Explorer Core Logic
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Any, Union
import pandas as pd


class DistributionExplorer:
    """概率分布探索器"""
    
    def __init__(self):
        self.distributions = {
            # 连续分布
            "正态分布": {
                "type": "continuous",
                "func": stats.norm,
                "params": {
                    "loc": {"name": "均值 (μ)", "default": 0, "min": -10, "max": 10, "step": 0.1},
                    "scale": {"name": "标准差 (σ)", "default": 1, "min": 0.1, "max": 5, "step": 0.1}
                },
                "support": "(-∞, +∞)"
            },
            "均匀分布": {
                "type": "continuous",
                "func": stats.uniform,
                "params": {
                    "loc": {"name": "下界 (a)", "default": 0, "min": -5, "max": 5, "step": 0.1},
                    "scale": {"name": "区间长度 (b-a)", "default": 1, "min": 0.1, "max": 10, "step": 0.1}
                },
                "support": "[a, b]"
            },
            "指数分布": {
                "type": "continuous",
                "func": stats.expon,
                "params": {
                    "scale": {"name": "尺度参数 (1/λ)", "default": 1, "min": 0.1, "max": 5, "step": 0.1}
                },
                "support": "[0, +∞)"
            },
            "伽马分布": {
                "type": "continuous",
                "func": stats.gamma,
                "params": {
                    "a": {"name": "形状参数 (α)", "default": 2, "min": 0.1, "max": 10, "step": 0.1},
                    "scale": {"name": "尺度参数 (β)", "default": 1, "min": 0.1, "max": 5, "step": 0.1}
                },
                "support": "[0, +∞)"
            },
            "贝塔分布": {
                "type": "continuous",
                "func": stats.beta,
                "params": {
                    "a": {"name": "形状参数 (α)", "default": 2, "min": 0.1, "max": 10, "step": 0.1},
                    "b": {"name": "形状参数 (β)", "default": 5, "min": 0.1, "max": 10, "step": 0.1}
                },
                "support": "[0, 1]"
            },
            "卡方分布": {
                "type": "continuous",
                "func": stats.chi2,
                "params": {
                    "df": {"name": "自由度 (ν)", "default": 3, "min": 1, "max": 20, "step": 1}
                },
                "support": "[0, +∞)"
            },
            "t分布": {
                "type": "continuous",
                "func": stats.t,
                "params": {
                    "df": {"name": "自由度 (ν)", "default": 5, "min": 1, "max": 30, "step": 1}
                },
                "support": "(-∞, +∞)"
            },
            "F分布": {
                "type": "continuous",
                "func": stats.f,
                "params": {
                    "dfn": {"name": "分子自由度", "default": 5, "min": 1, "max": 20, "step": 1},
                    "dfd": {"name": "分母自由度", "default": 10, "min": 1, "max": 30, "step": 1}
                },
                "support": "[0, +∞)"
            },
            # 离散分布
            "二项分布": {
                "type": "discrete",
                "func": stats.binom,
                "params": {
                    "n": {"name": "试验次数 (n)", "default": 10, "min": 1, "max": 100, "step": 1},
                    "p": {"name": "成功概率 (p)", "default": 0.3, "min": 0.01, "max": 0.99, "step": 0.01}
                },
                "support": "{0, 1, 2, ..., n}"
            },
            "泊松分布": {
                "type": "discrete",
                "func": stats.poisson,
                "params": {
                    "mu": {"name": "强度参数 (λ)", "default": 3, "min": 0.1, "max": 20, "step": 0.1}
                },
                "support": "{0, 1, 2, ...}"
            },
            "几何分布": {
                "type": "discrete",
                "func": stats.geom,
                "params": {
                    "p": {"name": "成功概率 (p)", "default": 0.3, "min": 0.01, "max": 0.99, "step": 0.01}
                },
                "support": "{1, 2, 3, ...}"
            },
            "负二项分布": {
                "type": "discrete",
                "func": stats.nbinom,
                "params": {
                    "n": {"name": "成功次数 (r)", "default": 5, "min": 1, "max": 20, "step": 1},
                    "p": {"name": "成功概率 (p)", "default": 0.3, "min": 0.01, "max": 0.99, "step": 0.01}
                },
                "support": "{0, 1, 2, ...}"
            }
        }
    
    def get_distribution_info(self, dist_name: str, params: Dict[str, float]) -> Dict[str, Any]:
        """获取分布信息"""
        if dist_name not in self.distributions:
            raise ValueError(f"不支持的分布: {dist_name}")
        
        dist_config = self.distributions[dist_name]
        
        # 验证参数
        validated_params = self._validate_params(dist_name, params)
        
        # 创建分布对象
        distribution = dist_config["func"](**validated_params)
        
        # 计算统计量
        try:
            mean = distribution.mean()
            var = distribution.var()
            std = distribution.std()
            
            # 对于连续分布，计算分位数
            if dist_config["type"] == "continuous":
                q25 = distribution.ppf(0.25)
                q50 = distribution.ppf(0.5)  # 中位数
                q75 = distribution.ppf(0.75)
                skewness = distribution.stats(moments='s')
                kurtosis = distribution.stats(moments='k')
            else:
                q25 = q50 = q75 = skewness = kurtosis = None
                
        except Exception as e:
            mean = var = std = q25 = q50 = q75 = skewness = kurtosis = np.nan
        
        return {
            "name": dist_name,
            "type": dist_config["type"],
            "distribution": distribution,
            "params": validated_params,
            "support": dist_config["support"],
            "mean": mean,
            "variance": var,
            "std": std,
            "q25": q25,
            "median": q50,
            "q75": q75,
            "skewness": skewness,
            "kurtosis": kurtosis
        }
    
    def _validate_params(self, dist_name: str, params: Dict[str, float]) -> Dict[str, float]:
        """验证和调整参数"""
        dist_config = self.distributions[dist_name]
        validated = {}
        
        for param_name, param_config in dist_config["params"].items():
            value = params.get(param_name, param_config["default"])
            
            # 确保参数在有效范围内
            min_val = param_config["min"]
            max_val = param_config["max"]
            validated[param_name] = max(min_val, min(max_val, value))
        
        return validated
    
    def calculate_pdf_pmf(self, dist_name: str, params: Dict[str, float], 
                         x_range: Tuple[float, float] = None, 
                         num_points: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """计算PDF或PMF"""
        dist_info = self.get_distribution_info(dist_name, params)
        distribution = dist_info["distribution"]
        dist_type = dist_info["type"]
        
        if dist_type == "continuous":
            if x_range is None:
                # 自动确定范围
                try:
                    x_min = distribution.ppf(0.001)
                    x_max = distribution.ppf(0.999)
                    if np.isinf(x_min):
                        x_min = distribution.mean() - 4 * distribution.std()
                    if np.isinf(x_max):
                        x_max = distribution.mean() + 4 * distribution.std()
                except:
                    x_min, x_max = -5, 5
            else:
                x_min, x_max = x_range
            
            x = np.linspace(x_min, x_max, num_points)
            y = distribution.pdf(x)
            
        else:  # discrete
            if x_range is None:
                # 自动确定范围
                try:
                    x_min = max(0, int(distribution.ppf(0.001)))
                    x_max = int(distribution.ppf(0.999))
                    if x_max - x_min > 100:  # 限制点数
                        x_max = x_min + 100
                except:
                    x_min, x_max = 0, 20
            else:
                x_min, x_max = int(x_range[0]), int(x_range[1])
            
            x = np.arange(x_min, x_max + 1)
            y = distribution.pmf(x)
        
        return x, y
    
    def get_scenario_description(self, dist_name: str, params: Dict[str, float]) -> str:
        """获取实际应用场景描述"""
        scenarios = {
            "正态分布": f"身高分布：平均身高{params.get('loc', 0):.1f}cm，标准差{params.get('scale', 1):.1f}cm的人群身高分布。",
            "均匀分布": f"随机数生成：在[{params.get('loc', 0):.1f}, {params.get('loc', 0) + params.get('scale', 1):.1f}]区间内均匀分布的随机数。",
            "指数分布": f"设备寿命：平均寿命为{params.get('scale', 1):.1f}年的电子设备的寿命分布。",
            "伽马分布": f"等待时间：等待第{params.get('a', 2):.0f}个客户到达的时间分布，平均间隔{params.get('scale', 1):.1f}分钟。",
            "贝塔分布": f"成功率：在{params.get('a', 2):.0f}次成功和{params.get('b', 5):.0f}次失败后，真实成功率的分布。",
            "卡方分布": f"方差检验：{params.get('df', 3):.0f}个独立标准正态变量平方和的分布。",
            "t分布": f"小样本均值：样本量为{params.get('df', 5):.0f}+1的样本均值的标准化分布。",
            "F分布": f"方差比检验：两个独立卡方分布（自由度{params.get('dfn', 5):.0f}和{params.get('dfd', 10):.0f}）比值的分布。",
            "二项分布": f"质量控制：{params.get('n', 10):.0f}个产品中，每个产品合格率为{params.get('p', 0.3):.1%}时的合格产品数量分布。",
            "泊松分布": f"客流统计：平均每小时有{params.get('mu', 3):.1f}位客户到达的商店客流分布。",
            "几何分布": f"首次成功：成功概率为{params.get('p', 0.3):.1%}的试验中，首次成功所需的试验次数分布。",
            "负二项分布": f"重复试验：成功概率为{params.get('p', 0.3):.1%}时，获得{params.get('n', 5):.0f}次成功所需的失败次数分布。"
        }
        return scenarios.get(dist_name, "暂无具体应用场景描述。")
    
    def get_available_distributions(self) -> Dict[str, List[str]]:
        """获取可用的分布列表，按类型分组"""
        continuous = []
        discrete = []
        
        for name, config in self.distributions.items():
            if config["type"] == "continuous":
                continuous.append(name)
            else:
                discrete.append(name)
        
        return {"连续分布": continuous, "离散分布": discrete}
    
    def get_param_config(self, dist_name: str) -> Dict[str, Dict[str, Any]]:
        """获取分布的参数配置"""
        if dist_name not in self.distributions:
            raise ValueError(f"不支持的分布: {dist_name}")
        
        return self.distributions[dist_name]["params"]
