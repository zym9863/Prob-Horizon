"""
概率分布探索器界面组件
Probability Distribution Explorer UI Component
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from scipy import stats

from ..utils.distribution_explorer import DistributionExplorer


def render_distribution_explorer():
    """渲染概率分布探索器界面"""
    
    st.title("🔍 经典概率分布探索器")
    st.markdown("---")
    
    # 创建探索器实例
    explorer = DistributionExplorer()
    
    # 获取可用分布
    available_distributions = explorer.get_available_distributions()
    
    # 侧边栏控制面板
    with st.sidebar:
        st.header("🎛️ 分布参数设置")
        
        # 分布类型选择
        dist_type = st.selectbox(
            "分布类型",
            options=list(available_distributions.keys()),
            help="选择连续分布或离散分布"
        )
        
        # 具体分布选择
        dist_name = st.selectbox(
            "选择分布",
            options=available_distributions[dist_type],
            help="选择要探索的具体分布"
        )
        
        # 动态参数控制
        st.markdown("### 📊 参数调整")
        params = {}
        param_configs = explorer.get_param_config(dist_name)
        
        for param_name, config in param_configs.items():
            if config["step"] == 1:  # 整数参数
                params[param_name] = st.slider(
                    config["name"],
                    min_value=int(config["min"]),
                    max_value=int(config["max"]),
                    value=int(config["default"]),
                    step=int(config["step"])
                )
            else:  # 浮点数参数
                params[param_name] = st.slider(
                    config["name"],
                    min_value=float(config["min"]),
                    max_value=float(config["max"]),
                    value=float(config["default"]),
                    step=float(config["step"])
                )
        
        # 图表设置
        st.markdown("### 🎨 图表设置")
        
        # 自定义x轴范围
        custom_range = st.checkbox("自定义显示范围", value=False)
        x_range = None
        if custom_range:
            col1, col2 = st.columns(2)
            with col1:
                x_min = st.number_input("最小值", value=0.0)
            with col2:
                x_max = st.number_input("最大值", value=10.0)
            x_range = (x_min, x_max)
        
        # 显示样本
        show_sample = st.checkbox("显示随机样本", value=False)
        if show_sample:
            sample_size = st.slider("样本大小", 10, 1000, 100)
    
    # 主要内容区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 分布可视化")
        
        try:
            # 获取分布信息
            dist_info = explorer.get_distribution_info(dist_name, params)
            
            # 计算PDF/PMF
            x, y = explorer.calculate_pdf_pmf(dist_name, params, x_range)
            
            # 创建可视化
            fig = create_distribution_plot(
                x, y, dist_info, show_sample, 
                sample_size if show_sample else None
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示应用场景
            st.subheader("🌟 实际应用场景")
            scenario = explorer.get_scenario_description(dist_name, params)
            st.info(scenario)
            
        except Exception as e:
            st.error(f"生成图表时出现错误: {str(e)}")
    
    with col2:
        st.subheader("📊 分布信息")
        
        try:
            # 显示分布信息
            display_distribution_info(dist_info)
            
            # 显示统计量
            st.subheader("📈 统计量")
            display_statistics_info(dist_info)
            
            # 显示分位数（仅连续分布）
            if dist_info["type"] == "continuous":
                st.subheader("📏 分位数")
                display_quantiles(dist_info)
            
        except Exception as e:
            st.error(f"显示信息时出现错误: {str(e)}")


def create_distribution_plot(x, y, dist_info, show_sample=False, sample_size=None):
    """创建分布图表"""
    
    fig = go.Figure()
    
    # 主分布图
    if dist_info["type"] == "continuous":
        # 连续分布 - 线图
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='lines',
                name=f'{dist_info["name"]} PDF',
                line=dict(color='blue', width=3),
                fill='tonexty',
                fillcolor='rgba(0, 100, 255, 0.2)'
            )
        )
        
        # 添加均值线
        if not np.isnan(dist_info["mean"]):
            fig.add_vline(
                x=dist_info["mean"],
                line_dash="dash",
                line_color="red",
                annotation_text=f"均值: {dist_info['mean']:.3f}"
            )
    
    else:
        # 离散分布 - 柱状图
        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                name=f'{dist_info["name"]} PMF',
                marker_color='lightblue',
                opacity=0.8
            )
        )
    
    # 添加随机样本
    if show_sample and sample_size:
        try:
            samples = dist_info["distribution"].rvs(size=sample_size)
            
            # 在x轴上显示样本点
            fig.add_trace(
                go.Scatter(
                    x=samples,
                    y=np.zeros(len(samples)),
                    mode='markers',
                    name=f'随机样本 (n={sample_size})',
                    marker=dict(
                        color='red',
                        size=4,
                        opacity=0.6,
                        symbol='circle'
                    ),
                    yaxis='y2'
                )
            )
            
            # 设置第二个y轴
            fig.update_layout(
                yaxis2=dict(
                    overlaying='y',
                    side='right',
                    showgrid=False,
                    showticklabels=False
                )
            )
            
        except Exception as e:
            st.warning(f"无法生成随机样本: {str(e)}")
    
    # 更新布局
    if dist_info["type"] == "continuous":
        type_text = "连续分布"
        y_title = "概率密度"
    else:
        type_text = "离散分布"
        y_title = "概率质量"

    title = f"{dist_info['name']} ({type_text})"

    fig.update_layout(
        title=title,
        xaxis_title="数值",
        yaxis_title=y_title,
        hovermode='x unified',
        height=500,
        showlegend=True,
        font=dict(family="SimHei, Arial, sans-serif")  # 支持中文字体
    )
    
    return fig


def display_distribution_info(dist_info):
    """显示分布基本信息"""
    
    st.markdown(f"**分布名称:** {dist_info['name']}")
    st.markdown(f"**分布类型:** {dist_info['type']}")
    st.markdown(f"**支撑集:** {dist_info['support']}")
    
    # 显示参数
    st.markdown("**当前参数:**")
    for param, value in dist_info["params"].items():
        if isinstance(value, float):
            st.write(f"• {param} = {value:.3f}")
        else:
            st.write(f"• {param} = {value}")


def display_statistics_info(dist_info):
    """显示统计量信息"""
    
    # 基本统计量
    if not np.isnan(dist_info["mean"]):
        st.metric("均值 (E[X])", f"{dist_info['mean']:.4f}")
    else:
        st.metric("均值 (E[X])", "未定义")
    
    if not np.isnan(dist_info["variance"]):
        st.metric("方差 (Var[X])", f"{dist_info['variance']:.4f}")
    else:
        st.metric("方差 (Var[X])", "未定义")
    
    if not np.isnan(dist_info["std"]):
        st.metric("标准差 (σ)", f"{dist_info['std']:.4f}")
    else:
        st.metric("标准差 (σ)", "未定义")
    
    # 高阶矩（仅连续分布）
    if dist_info["type"] == "continuous":
        if dist_info["skewness"] is not None and not np.isnan(dist_info["skewness"]):
            st.metric("偏度", f"{dist_info['skewness']:.4f}")
        
        if dist_info["kurtosis"] is not None and not np.isnan(dist_info["kurtosis"]):
            st.metric("峰度", f"{dist_info['kurtosis']:.4f}")


def display_quantiles(dist_info):
    """显示分位数信息（仅连续分布）"""
    
    quantiles_data = {
        "分位数": ["25%", "50% (中位数)", "75%"],
        "值": []
    }
    
    for q in [dist_info["q25"], dist_info["median"], dist_info["q75"]]:
        if q is not None and not np.isnan(q):
            quantiles_data["值"].append(f"{q:.4f}")
        else:
            quantiles_data["值"].append("未定义")
    
    df = pd.DataFrame(quantiles_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 四分位距
    if (dist_info["q75"] is not None and dist_info["q25"] is not None and 
        not np.isnan(dist_info["q75"]) and not np.isnan(dist_info["q25"])):
        iqr = dist_info["q75"] - dist_info["q25"]
        st.metric("四分位距 (IQR)", f"{iqr:.4f}")


def create_comparison_plot(distributions_data):
    """创建多个分布的对比图（可选功能）"""
    
    fig = go.Figure()
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, (name, x, y) in enumerate(distributions_data):
        color = colors[i % len(colors)]
        
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='lines',
                name=name,
                line=dict(color=color, width=2)
            )
        )
    
    fig.update_layout(
        title="分布对比",
        xaxis_title="x",
        yaxis_title="概率密度/质量",
        hovermode='x unified',
        height=500
    )
    
    return fig
