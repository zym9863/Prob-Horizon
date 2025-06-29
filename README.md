# 🎲 概率视界 - Probability Horizon

一个交互式概率论学习工具，通过可视化和模拟帮助用户理解概率论的核心概念。

## ✨ 主要功能

### 🎯 中心极限定理交互式模拟器
- **多种总体分布**：支持8种不同的概率分布（均匀、正态、指数、泊松、伽马、贝塔、卡方、二项）
- **参数可调**：灵活调整样本大小（1-200）和抽样次数（10-5000）
- **实时可视化**：动态展示原始分布、样本均值分布、直方图和Q-Q图
- **理论对比**：实际统计量与理论值的对比分析
- **正态性检验**：Shapiro-Wilk和Kolmogorov-Smirnov检验

### 🔍 经典概率分布探索器
- **丰富的分布类型**：12种常用概率分布（连续和离散）
- **实时参数调整**：通过滑块实时调整分布参数
- **PDF/PMF可视化**：高质量的概率密度/质量函数图表
- **统计量计算**：均值、方差、标准差、偏度、峰度等
- **分位数信息**：25%、50%、75%分位数和四分位距
- **应用场景**：每种分布的实际应用场景说明

## 🚀 快速开始

### 环境要求
- Python 3.12+
- uv 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/zym9863/prob-horizon.git
cd Prob-Horizon
```

2. **安装依赖**
```bash
uv sync
```

3. **运行应用**
```bash
uv run streamlit run main.py
```

4. **访问应用**
打开浏览器访问 `http://localhost:8501`

## 📖 使用指南

### 中心极限定理模拟器

1. **选择总体分布**：从侧边栏选择一个总体分布
2. **设置参数**：
   - 样本大小：每次抽样的样本数量
   - 抽样次数：进行抽样的总次数
3. **开始模拟**：点击"开始模拟"按钮
4. **观察结果**：
   - 查看样本均值分布是否趋近正态分布
   - 对比实际值与理论值
   - 查看正态性检验结果

### 概率分布探索器

1. **选择分布**：
   - 先选择分布类型（连续/离散）
   - 再选择具体分布
2. **调整参数**：使用滑块调整分布参数
3. **查看结果**：
   - 实时查看PDF/PMF图表
   - 查看统计量和分位数信息
   - 了解实际应用场景

## 🛠️ 技术栈

- **前端框架**：Streamlit
- **数值计算**：NumPy, SciPy
- **数据处理**：Pandas
- **可视化**：Plotly, Matplotlib
- **包管理**：uv

## 📁 项目结构

```
Prob-Horizon/
├── main.py                 # 主应用入口
├── src/
│   ├── components/         # UI组件
│   │   ├── clt_simulator_ui.py
│   │   └── distribution_explorer_ui.py
│   └── utils/             # 核心逻辑
│       ├── clt_simulator.py
│       └── distribution_explorer.py
├── tests/                 # 测试文件
├── pyproject.toml        # 项目配置
└── README.md            # 项目说明
```

## 🎓 教育价值

### 中心极限定理
- **直观理解**：通过可视化直观理解中心极限定理的含义
- **参数影响**：观察样本大小对定理效果的影响
- **分布无关性**：验证定理对不同总体分布的普适性

### 概率分布
- **参数效应**：理解参数变化对分布形状的影响
- **分布特性**：掌握各种分布的统计特性
- **实际应用**：了解不同分布在现实中的应用场景

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 开发环境设置
```bash
# 克隆项目
git clone https://github.com/zym9863/prob-horizon.git
cd Prob-Horizon

# 安装开发依赖
uv add --dev pytest black flake8

# 运行测试
uv run pytest

# 代码格式化
uv run black .
```

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢以下开源项目：
- [Streamlit](https://streamlit.io/) - 快速构建数据应用
- [SciPy](https://scipy.org/) - 科学计算库
- [Plotly](https://plotly.com/) - 交互式可视化
- [NumPy](https://numpy.org/) - 数值计算基础

---

**概率视界** - 让概率论学习更加直观和有趣！ 🎲✨