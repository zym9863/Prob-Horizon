"""
概率视界 - Probability Horizon
一个交互式概率论学习工具

主要功能：
1. 中心极限定理交互式模拟器
2. 经典概率分布探索器
"""

import streamlit as st
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.components.clt_simulator_ui import render_clt_simulator
from src.components.distribution_explorer_ui import render_distribution_explorer


def main():
    """主应用入口"""

    # 页面配置
    st.set_page_config(
        page_title="概率视界 - Probability Horizon",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 自定义CSS样式
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #333; /* 设置文字颜色以保证对比度 */
    }

    .stSelectbox > div > div {
        background-color: #f0f2f6;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

    # 主标题
    st.markdown("""
    <div class="main-header">
        <h1>🎲 概率视界 - Probability Horizon</h1>
        <p>交互式概率论学习工具</p>
    </div>
    """, unsafe_allow_html=True)

    # 导航菜单
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/667eea/ffffff?text=概率视界",
                caption="Probability Horizon")

        st.markdown("---")

        page = st.selectbox(
            "🧭 选择功能模块",
            options=[
                "🏠 首页",
                "🎯 中心极限定理模拟器",
                "🔍 概率分布探索器"
            ],
            index=0
        )

        st.markdown("---")

        # 关于信息
        with st.expander("ℹ️ 关于概率视界"):
            st.markdown("""
            **概率视界**是一个交互式概率论学习工具，旨在通过可视化和模拟帮助用户理解概率论的核心概念。

            **主要功能：**
            - 🎯 中心极限定理交互式模拟
            - 🔍 经典概率分布探索

            **技术栈：**
            - Python + Streamlit
            - NumPy + SciPy
            - Plotly + Matplotlib
            """)

    # 根据选择显示不同页面
    if page == "🏠 首页":
        render_home_page()
    elif page == "🎯 中心极限定理模拟器":
        render_clt_simulator()
    elif page == "🔍 概率分布探索器":
        render_distribution_explorer()


def render_home_page():
    """渲染首页"""

    st.markdown("## 🌟 欢迎使用概率视界")

    # 功能介绍
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 中心极限定理模拟器</h3>
            <p>通过交互式模拟直观理解中心极限定理：</p>
            <ul>
                <li>选择不同的总体分布</li>
                <li>调整样本大小和抽样次数</li>
                <li>观察样本均值分布的变化</li>
                <li>对比理论值与实际值</li>
                <li>进行正态性检验</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 概率分布探索器</h3>
            <p>深入探索经典概率分布的特性：</p>
            <ul>
                <li>12种常用概率分布</li>
                <li>实时参数调整</li>
                <li>PDF/PMF可视化</li>
                <li>统计量计算</li>
                <li>实际应用场景说明</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # 快速开始
    st.markdown("## 🚀 快速开始")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎯 开始模拟中心极限定理", type="primary", use_container_width=True):
            st.session_state.page = "🎯 中心极限定理模拟器"
            st.rerun()

    with col2:
        if st.button("🔍 探索概率分布", type="primary", use_container_width=True):
            st.session_state.page = "🔍 概率分布探索器"
            st.rerun()

    with col3:
        if st.button("📚 查看使用说明", use_container_width=True):
            show_instructions()

    # 最新更新
    st.markdown("## 📈 功能特色")

    features = [
        "🎨 **美观的界面设计** - 现代化的用户界面，提供良好的用户体验",
        "⚡ **实时交互** - 参数调整后立即更新图表和统计信息",
        "📊 **丰富的可视化** - 多种图表类型，全面展示分布特性",
        "🔬 **科学严谨** - 基于SciPy库，确保计算结果的准确性",
        "🌐 **中文界面** - 完全中文化的界面，便于中文用户使用",
        "📱 **响应式设计** - 适配不同屏幕尺寸，支持移动设备访问"
    ]

    for feature in features:
        st.markdown(feature)


def show_instructions():
    """显示使用说明"""

    with st.expander("📚 详细使用说明", expanded=True):
        st.markdown("""
        ### 🎯 中心极限定理模拟器使用方法

        1. **选择总体分布**：从8种不同的分布中选择一个作为总体分布
        2. **设置样本大小**：调整每次抽样的样本数量（1-200）
        3. **设置抽样次数**：调整进行抽样的总次数（10-5000）
        4. **开始模拟**：点击"开始模拟"按钮运行模拟
        5. **查看结果**：观察样本均值分布是否趋近正态分布

        ### 🔍 概率分布探索器使用方法

        1. **选择分布类型**：连续分布或离散分布
        2. **选择具体分布**：从可用分布列表中选择
        3. **调整参数**：使用滑块调整分布参数
        4. **查看图表**：实时查看PDF/PMF图表
        5. **查看统计信息**：右侧面板显示详细的统计量

        ### 💡 学习建议

        - 先从简单的分布开始探索，如均匀分布、正态分布
        - 观察参数变化对分布形状的影响
        - 在中心极限定理模拟中，尝试不同的非正态分布
        - 注意样本大小对中心极限定理效果的影响
        """)


if __name__ == "__main__":
    main()
