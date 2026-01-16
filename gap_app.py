import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# --- 1. 实验室核心配置（防御 removeChild 报错） ---
st.set_page_config(
    page_title="Creative Gap Lab 2026",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入 CSS 补丁：禁止浏览器翻译干扰 DOM，设置深色实验室主题
st.markdown(
    """
    <style>
        /* 禁止翻译插件 */
        .main, .stApp { unicode-bidi: isolate; }
        html[lang] { content: "en"; }
        
        /* 2026 科技美学自定义 */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #e0e0e0;
        }
        .stMetric {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0, 255, 255, 0.2);
        }
    </style>
    <script>
        document.documentElement.className += ' notranslate';
        document.querySelector('meta[name="google"]').setAttribute("content", "notranslate");
    </script>
    """,
    unsafe_allow_html=True
)

# --- 2. 数据载入引擎 ---
@st.cache_data
def load_full_database():
    file_path = "Global_Sovereign_2026_Final.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # 如果文件还没生成，给一个友好的提示
        st.error(f"❌ 未找到数据库文件: {file_path}。请先运行生成器脚本！")
        return None

df = load_full_database()

# --- 3. 侧边栏：决策者筛选 ---
st.sidebar.title("🧪 Creative Gap Lab")
st.sidebar.markdown("---")

if df is not None:
    # 国家搜索与选择
    all_countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("🎯 选择目标主权节点", all_countries, index=all_countries.index("China") if "China" in all_countries else 0)
    
    # 提取当前国家原始数据
    c_data = df[df['Country'] == selected_country].iloc[0]
    
    st.sidebar.subheader("🎚️ 实时干扰因子 (Interference)")
    # 我们为四个大维度各选一个核心滑块作为交互演示
    mod_power = st.sidebar.slider("创新权力影响 (Innovation)", 0.0, 10.0, float(c_data['Power_Innovation']))
    mod_gov = st.sidebar.slider("治理效能干预 (Governance)", 0.0, 10.0, float(c_data['Gov_Governance']))
    mod_inter = st.sidebar.slider("外部互动频率 (Interaction)", 0.0, 10.0, float(c_data['Inter_Trade']))

# --- 4. 主界面：马尔可夫博弈演化 ---
st.title(f"🌐 {selected_country if df is not None else 'Global'} 风险博弈罗盘")

if df is not None:
    # 模拟 3.0 版本的计算逻辑：基于 21 个维度的加权
    # 基础位势能
    base_potential = (mod_power * 0.4 + mod_gov * 0.4 + mod_inter * 0.2)
    
    # 状态概率生成 (基于马尔可夫 5 状态模型简易模拟)
    # S1:坍塌, S2:震荡, S3:平稳, S4:上升, S5:跃迁
    probs = [
        max(0.05, (10 - base_potential) * 0.08), # S1
        0.15,                                    # S2
        max(0.1, 0.4 - base_potential * 0.02),   # S3
        0.25,                                    # S4
        min(0.45, base_potential * 0.05 + 0.1)   # S5
    ]
    # 归一化
    probs = np.array(probs) / sum(probs)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 状态转移概率分布")
        labels = ['S1: 熵增坍塌', 'S2: 存量震荡', 'S3: 系统平稳', 'S4: 势能上升', 'S5: 跨越跃迁']
        fig = go.Figure(data=[go.Pie(labels=labels, values=probs, hole=.4, marker_colors=['#ff4b4b', '#ffa500', '#f0f2f6', '#00ffcc', '#0080ff'])])
        fig.update_layout(template="plotly_dark", margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📜 决策建议 (2026 AI 推演)")
        if probs[4] > 0.3:
            st.success(f"**检测到跃迁信号**：{selected_country} 目前处于创新红利窗口。建议增加全球归国人才权重，强化非对称贸易链。")
        elif probs[0] > 0.2:
            st.error(f"**风险预警**：系统不稳定性剧增。建议缩减外部敞口，激活“领土/资源”底座的防御机制。")
        else:
            st.info(f"**平稳态势**：建议保持当前治理带宽，持续优化人口技能水平。")

    # 展示完整 21 个维度的实时数据快照
    with st.expander("🔍 查看该国家 21 个维度的原始测量值"):
        st.table(df[df['Country'] == selected_country].T)

else:
    st.warning("👈 请先确保数据文件已生成并在侧边栏操作。")

# --- 5. 底部页脚 ---
st.markdown("---")
st.caption("© 2026 Creative Gap Lab | 互联、断裂与跃迁的数字孪生系统")