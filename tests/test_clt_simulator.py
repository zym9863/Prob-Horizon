"""
中心极限定理模拟器测试
"""

import pytest
import numpy as np
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.clt_simulator import CLTSimulator


class TestCLTSimulator:
    """中心极限定理模拟器测试类"""
    
    def setup_method(self):
        """测试前的设置"""
        self.simulator = CLTSimulator()
    
    def test_get_available_distributions(self):
        """测试获取可用分布列表"""
        distributions = self.simulator.get_available_distributions()
        
        assert isinstance(distributions, list)
        assert len(distributions) > 0
        assert "正态分布" in distributions
        assert "均匀分布" in distributions
    
    def test_get_distribution_info(self):
        """测试获取分布信息"""
        dist_info = self.simulator.get_distribution_info("正态分布")
        
        assert dist_info["name"] == "正态分布"
        assert "distribution" in dist_info
        assert "theoretical_mean" in dist_info
        assert "theoretical_var" in dist_info
        assert "theoretical_std" in dist_info
    
    def test_generate_population_sample(self):
        """测试生成总体样本"""
        sample = self.simulator.generate_population_sample("正态分布", size=1000)
        
        assert isinstance(sample, np.ndarray)
        assert len(sample) == 1000
        assert np.isfinite(sample).all()
    
    def test_simulate_sampling(self):
        """测试模拟抽样过程"""
        sample_means, statistics = self.simulator.simulate_sampling(
            "正态分布", sample_size=30, num_samples=100
        )
        
        # 检查返回值
        assert isinstance(sample_means, np.ndarray)
        assert isinstance(statistics, dict)
        assert len(sample_means) == 100
        
        # 检查统计信息
        required_keys = [
            "sample_mean_mean", "sample_mean_var", "sample_mean_std",
            "theoretical_mean", "theoretical_std_of_means",
            "sample_size", "num_samples"
        ]
        for key in required_keys:
            assert key in statistics
        
        # 检查数值合理性
        assert statistics["sample_size"] == 30
        assert statistics["num_samples"] == 100
        assert np.isfinite(statistics["sample_mean_mean"])
        assert np.isfinite(statistics["sample_mean_std"])
    
    def test_calculate_normality_test(self):
        """测试正态性检验"""
        # 生成正态分布样本
        sample_means = np.random.normal(0, 1, 100)
        
        results = self.simulator.calculate_normality_test(sample_means)
        
        assert isinstance(results, dict)
        assert "shapiro_statistic" in results
        assert "shapiro_p_value" in results
        assert "ks_statistic" in results
        assert "ks_p_value" in results
    
    def test_get_distribution_description(self):
        """测试获取分布描述"""
        description = self.simulator.get_distribution_description("正态分布")
        
        assert isinstance(description, str)
        assert len(description) > 0
        assert "正态分布" in description or "钟形" in description
    
    def test_different_distributions(self):
        """测试不同分布的模拟"""
        distributions_to_test = ["均匀分布", "指数分布", "泊松分布"]
        
        for dist_name in distributions_to_test:
            try:
                sample_means, statistics = self.simulator.simulate_sampling(
                    dist_name, sample_size=20, num_samples=50
                )
                
                assert len(sample_means) == 50
                assert statistics["sample_size"] == 20
                assert statistics["num_samples"] == 50
                
            except Exception as e:
                pytest.fail(f"分布 {dist_name} 测试失败: {str(e)}")
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 最小样本大小
        sample_means, statistics = self.simulator.simulate_sampling(
            "正态分布", sample_size=1, num_samples=10
        )
        assert len(sample_means) == 10
        
        # 大样本大小
        sample_means, statistics = self.simulator.simulate_sampling(
            "正态分布", sample_size=100, num_samples=10
        )
        assert len(sample_means) == 10
    
    def test_invalid_distribution(self):
        """测试无效分布名称"""
        with pytest.raises(ValueError):
            self.simulator.get_distribution_info("不存在的分布")


if __name__ == "__main__":
    pytest.main([__file__])
