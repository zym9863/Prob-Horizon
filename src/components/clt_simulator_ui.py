"""
中心极限定理模拟器界面组件
Central Limit Theorem Simulator UI Component
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from scipy import stats

from ..utils.clt_simulator import CLTSimulator


def render_clt_simulator():
    """渲染中心极限定理模拟器界面"""
    
    st.title("🎯 中心极限定理交互式模拟器")
    st.markdown("---")
    
    # 创建模拟器实例
    simulator = CLTSimulator()
    
    # 侧边栏控制面板
    with st.sidebar:
        st.header("📊 模拟参数设置")
        
        # 选择总体分布
        dist_name = st.selectbox(
            "选择总体分布",
            options=simulator.get_available_distributions(),
            help="选择要模拟的总体分布类型"
        )
        
        # 样本大小
        sample_size = st.slider(
            "样本大小 (n)",
            min_value=1,
            max_value=200,
            value=30,
            step=1,
            help="每次抽样的样本数量"
        )
        
        # 抽样次数
        num_samples = st.slider(
            "抽样次数",
            min_value=10,
            max_value=5000,
            value=1000,
            step=10,
            help="进行抽样的总次数"
        )
        
        # 开始模拟按钮
        if st.button("🚀 开始模拟", type="primary"):
            st.session_state.run_simulation = True
        
        # 显示分布描述
        st.markdown("### 📝 分布说明")
        st.info(simulator.get_distribution_description(dist_name))
    
    # 主要内容区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 模拟结果可视化")
        
        # 检查是否需要运行模拟
        if hasattr(st.session_state, 'run_simulation') and st.session_state.run_simulation:
            
            # 显示进度条
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # 运行模拟
                status_text.text("正在进行模拟...")
                progress_bar.progress(25)
                
                sample_means, statistics = simulator.simulate_sampling(
                    dist_name, sample_size, num_samples
                )
                
                progress_bar.progress(50)
                status_text.text("正在生成可视化...")
                
                # 创建可视化
                fig = create_clt_visualization(
                    sample_means, statistics, dist_name, simulator
                )
                
                progress_bar.progress(75)
                
                # 显示图表
                st.plotly_chart(fig, use_container_width=True)
                
                progress_bar.progress(100)
                status_text.text("模拟完成！")
                
                # 清除进度指示器
                progress_bar.empty()
                status_text.empty()
                
                # 存储结果到session state
                st.session_state.last_results = {
                    'sample_means': sample_means,
                    'statistics': statistics,
                    'dist_name': dist_name
                }
                
            except Exception as e:
                st.error(f"模拟过程中出现错误: {str(e)}")
                progress_bar.empty()
                status_text.empty()
            
            # 重置模拟标志
            st.session_state.run_simulation = False
        
        elif hasattr(st.session_state, 'last_results'):
            # 显示上次的结果
            results = st.session_state.last_results
            fig = create_clt_visualization(
                results['sample_means'], 
                results['statistics'], 
                results['dist_name'], 
                simulator
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            # 显示说明
            st.info("👈 请在左侧设置参数并点击'开始模拟'按钮来查看中心极限定理的效果")
    
    with col2:
        st.subheader("📊 统计信息")
        
        if hasattr(st.session_state, 'last_results'):
            display_statistics(st.session_state.last_results['statistics'])
            
            # 正态性检验
            st.subheader("🔍 正态性检验")
            normality_results = simulator.calculate_normality_test(
                st.session_state.last_results['sample_means']
            )
            display_normality_test(normality_results)
        
        else:
            st.info("运行模拟后将显示详细的统计信息")


def create_clt_visualization(sample_means, statistics, dist_name, simulator):
    """创建中心极限定理可视化图表"""
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f"原始{dist_name}分布",
            "样本均值分布",
            "样本均值直方图",
            "Q-Q图（正态性检验）"
        ),
        specs=[[{"type": "scatter"}, {"type": "scatter"}],
               [{"type": "histogram"}, {"type": "scatter"}]]
    )
    
    # 1. 原始分布
    try:
        population_sample = simulator.generate_population_sample(dist_name, 10000)
        fig.add_trace(
            go.Histogram(
                x=population_sample,
                name=f"原始{dist_name}",
                nbinsx=50,
                opacity=0.7,
                marker_color="lightblue"
            ),
            row=1, col=1
        )
    except Exception as e:
        st.warning(f"无法显示原始分布: {str(e)}")
    
    # 2. 样本均值分布（理论正态分布对比）
    x_range = np.linspace(sample_means.min(), sample_means.max(), 100)
    theoretical_normal = stats.norm(
        loc=statistics['theoretical_mean'],
        scale=statistics['theoretical_std_of_means']
    )
    
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=theoretical_normal.pdf(x_range),
            mode='lines',
            name='理论正态分布',
            line=dict(color='red', width=2)
        ),
        row=1, col=2
    )
    
    # 3. 样本均值直方图
    fig.add_trace(
        go.Histogram(
            x=sample_means,
            name="样本均值",
            nbinsx=50,
            opacity=0.7,
            marker_color="lightgreen",
            histnorm='probability density'
        ),
        row=2, col=1
    )
    
    # 添加理论正态分布曲线到直方图
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=theoretical_normal.pdf(x_range),
            mode='lines',
            name='理论正态分布',
            line=dict(color='red', width=2),
            showlegend=False
        ),
        row=2, col=1
    )
    
    # 4. Q-Q图
    try:
        from scipy.stats import probplot
        qq_data = probplot(sample_means, dist=stats.norm, plot=None)
        
        fig.add_trace(
            go.Scatter(
                x=qq_data[0][0],
                y=qq_data[0][1],
                mode='markers',
                name='Q-Q点',
                marker=dict(color='blue', size=4)
            ),
            row=2, col=2
        )
        
        # 添加理论直线
        fig.add_trace(
            go.Scatter(
                x=qq_data[0][0],
                y=qq_data[1][1] + qq_data[1][0] * qq_data[0][0],
                mode='lines',
                name='理论直线',
                line=dict(color='red', width=2),
                showlegend=False
            ),
            row=2, col=2
        )
    except Exception as e:
        st.warning(f"无法生成Q-Q图: {str(e)}")
    
    # 更新布局
    fig.update_layout(
        height=800,
        title_text=f"中心极限定理模拟结果 - {dist_name} (样本大小={statistics['sample_size']}, 抽样次数={statistics['num_samples']})",
        showlegend=True,
        font=dict(family="SimHei, Arial, sans-serif")  # 支持中文字体
    )

    # 更新坐标轴标签为中文
    fig.update_xaxes(title_text="数值", row=1, col=1)
    fig.update_yaxes(title_text="频数", row=1, col=1)
    fig.update_xaxes(title_text="数值", row=1, col=2)
    fig.update_yaxes(title_text="概率密度", row=1, col=2)
    fig.update_xaxes(title_text="样本均值", row=2, col=1)
    fig.update_yaxes(title_text="概率密度", row=2, col=1)
    fig.update_xaxes(title_text="理论分位数", row=2, col=2)
    fig.update_yaxes(title_text="样本分位数", row=2, col=2)
    
    return fig


def display_statistics(statistics):
    """显示统计信息"""
    
    # 样本均值的统计量
    st.metric("样本均值的均值", f"{statistics['sample_mean_mean']:.4f}")
    st.metric("样本均值的标准差", f"{statistics['sample_mean_std']:.4f}")
    
    st.markdown("### 理论值对比")
    
    # 创建对比表格
    comparison_data = {
        "统计量": ["均值", "标准差"],
        "实际值": [
            f"{statistics['sample_mean_mean']:.4f}",
            f"{statistics['sample_mean_std']:.4f}"
        ],
        "理论值": [
            f"{statistics['theoretical_mean']:.4f}",
            f"{statistics['theoretical_std_of_means']:.4f}"
        ],
        "差异": [
            f"{abs(statistics['sample_mean_mean'] - statistics['theoretical_mean']):.4f}",
            f"{abs(statistics['sample_mean_std'] - statistics['theoretical_std_of_means']):.4f}"
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)


def display_normality_test(normality_results):
    """显示正态性检验结果"""
    
    if 'error' in normality_results:
        st.error(f"检验失败: {normality_results['error']}")
        return
    
    # Shapiro-Wilk检验
    st.markdown("**Shapiro-Wilk检验**")
    st.write(f"统计量: {normality_results['shapiro_statistic']:.4f}")
    st.write(f"p值: {normality_results['shapiro_p_value']:.4f}")
    
    if normality_results['shapiro_p_value'] > 0.05:
        st.success("✅ 接受正态分布假设 (p > 0.05)")
    else:
        st.warning("⚠️ 拒绝正态分布假设 (p ≤ 0.05)")
    
    # Kolmogorov-Smirnov检验
    st.markdown("**Kolmogorov-Smirnov检验**")
    st.write(f"统计量: {normality_results['ks_statistic']:.4f}")
    st.write(f"p值: {normality_results['ks_p_value']:.4f}")
    
    if normality_results['ks_p_value'] > 0.05:
        st.success("✅ 接受正态分布假设 (p > 0.05)")
    else:
        st.warning("⚠️ 拒绝正态分布假设 (p ≤ 0.05)")
