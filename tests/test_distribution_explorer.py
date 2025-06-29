"""
概率分布探索器测试
"""

import pytest
import numpy as np
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.distribution_explorer import DistributionExplorer


class TestDistributionExplorer:
    """概率分布探索器测试类"""
    
    def setup_method(self):
        """测试前的设置"""
        self.explorer = DistributionExplorer()
    
    def test_get_available_distributions(self):
        """测试获取可用分布列表"""
        distributions = self.explorer.get_available_distributions()
        
        assert isinstance(distributions, dict)
        assert "连续分布" in distributions
        assert "离散分布" in distributions
        assert len(distributions["连续分布"]) > 0
        assert len(distributions["离散分布"]) > 0
        assert "正态分布" in distributions["连续分布"]
        assert "二项分布" in distributions["离散分布"]
    
    def test_get_param_config(self):
        """测试获取参数配置"""
        config = self.explorer.get_param_config("正态分布")
        
        assert isinstance(config, dict)
        assert "loc" in config
        assert "scale" in config
        
        # 检查参数配置结构
        for param_name, param_config in config.items():
            assert "name" in param_config
            assert "default" in param_config
            assert "min" in param_config
            assert "max" in param_config
            assert "step" in param_config
    
    def test_get_distribution_info_continuous(self):
        """测试获取连续分布信息"""
        params = {"loc": 0, "scale": 1}
        dist_info = self.explorer.get_distribution_info("正态分布", params)
        
        assert dist_info["name"] == "正态分布"
        assert dist_info["type"] == "continuous"
        assert "distribution" in dist_info
        assert "params" in dist_info
        assert "mean" in dist_info
        assert "variance" in dist_info
        assert "std" in dist_info
        
        # 检查正态分布的理论值
        assert abs(dist_info["mean"] - 0) < 1e-10
        assert abs(dist_info["variance"] - 1) < 1e-10
        assert abs(dist_info["std"] - 1) < 1e-10
    
    def test_get_distribution_info_discrete(self):
        """测试获取离散分布信息"""
        params = {"n": 10, "p": 0.5}
        dist_info = self.explorer.get_distribution_info("二项分布", params)
        
        assert dist_info["name"] == "二项分布"
        assert dist_info["type"] == "discrete"
        assert "distribution" in dist_info
        
        # 检查二项分布的理论值
        expected_mean = 10 * 0.5
        expected_var = 10 * 0.5 * 0.5
        assert abs(dist_info["mean"] - expected_mean) < 1e-10
        assert abs(dist_info["variance"] - expected_var) < 1e-10
    
    def test_validate_params(self):
        """测试参数验证"""
        # 测试正常参数
        params = {"loc": 0, "scale": 1}
        validated = self.explorer._validate_params("正态分布", params)
        assert validated["loc"] == 0
        assert validated["scale"] == 1
        
        # 测试超出范围的参数
        params = {"loc": 100, "scale": -1}  # scale不能为负
        validated = self.explorer._validate_params("正态分布", params)
        assert validated["loc"] <= 10  # 应该被限制在最大值
        assert validated["scale"] >= 0.1  # 应该被限制在最小值
    
    def test_calculate_pdf_pmf_continuous(self):
        """测试连续分布的PDF计算"""
        params = {"loc": 0, "scale": 1}
        x, y = self.explorer.calculate_pdf_pmf("正态分布", params)
        
        assert isinstance(x, np.ndarray)
        assert isinstance(y, np.ndarray)
        assert len(x) == len(y)
        assert len(x) > 0
        assert np.all(y >= 0)  # PDF值应该非负
        assert np.isfinite(x).all()
        assert np.isfinite(y).all()
    
    def test_calculate_pdf_pmf_discrete(self):
        """测试离散分布的PMF计算"""
        params = {"n": 10, "p": 0.5}
        x, y = self.explorer.calculate_pdf_pmf("二项分布", params)
        
        assert isinstance(x, np.ndarray)
        assert isinstance(y, np.ndarray)
        assert len(x) == len(y)
        assert len(x) > 0
        assert np.all(y >= 0)  # PMF值应该非负
        assert np.all(y <= 1)  # PMF值应该不超过1
        assert np.isfinite(x).all()
        assert np.isfinite(y).all()
        
        # 检查PMF总和接近1（对于有限支撑集）
        if len(x) < 100:  # 只对小的支撑集检查
            assert abs(np.sum(y) - 1.0) < 0.1
    
    def test_get_scenario_description(self):
        """测试获取应用场景描述"""
        params = {"loc": 0, "scale": 1}
        description = self.explorer.get_scenario_description("正态分布", params)
        
        assert isinstance(description, str)
        assert len(description) > 0
    
    def test_custom_range(self):
        """测试自定义范围"""
        params = {"loc": 0, "scale": 1}
        x_range = (-2, 2)
        x, y = self.explorer.calculate_pdf_pmf("正态分布", params, x_range)
        
        assert x.min() >= -2
        assert x.max() <= 2
    
    def test_multiple_distributions(self):
        """测试多种分布"""
        test_cases = [
            ("正态分布", {"loc": 0, "scale": 1}),
            ("均匀分布", {"loc": 0, "scale": 1}),
            ("指数分布", {"scale": 1}),
            ("二项分布", {"n": 10, "p": 0.5}),
            ("泊松分布", {"mu": 3}),
        ]
        
        for dist_name, params in test_cases:
            try:
                dist_info = self.explorer.get_distribution_info(dist_name, params)
                x, y = self.explorer.calculate_pdf_pmf(dist_name, params)
                
                assert dist_info["name"] == dist_name
                assert len(x) > 0
                assert len(y) > 0
                assert np.all(y >= 0)
                
            except Exception as e:
                pytest.fail(f"分布 {dist_name} 测试失败: {str(e)}")
    
    def test_invalid_distribution(self):
        """测试无效分布名称"""
        with pytest.raises(ValueError):
            self.explorer.get_distribution_info("不存在的分布", {})
        
        with pytest.raises(ValueError):
            self.explorer.get_param_config("不存在的分布")
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 极小参数值
        params = {"loc": 0, "scale": 0.1}
        dist_info = self.explorer.get_distribution_info("正态分布", params)
        assert dist_info["std"] == 0.1
        
        # 极大参数值
        params = {"loc": 0, "scale": 5}
        dist_info = self.explorer.get_distribution_info("正态分布", params)
        assert dist_info["std"] == 5


if __name__ == "__main__":
    pytest.main([__file__])
