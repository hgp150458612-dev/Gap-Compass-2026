import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- 页面配置 ---
st.set_page_config(page_title="Gap-Compass 2.0", layout="wide", page_icon="🌐")

# --- 模拟全球数据库 (2026 实时快照逻辑) ---
@st.cache_data
def get_global_data():
    return {
        "中国": {"innovation": 88, "aging": 15.4, "gdp_growth": 4.5, "position": "核心节点", "color": "red"},
        "越南": {"innovation": 42, "aging": 8.2, "gdp_growth": 6.5, "position": "新兴节点", "color": "yellow"},
        "德国": {"innovation": 91, "aging": 22.1, "gdp_growth": 0.5, "position": "传统节点", "color": "blue"},
        "美国": {"innovation": 96, "aging": 17.0, "gdp_growth": 2.1, "position": "主导节点", "color": "green"}
    }

data_db = get_global_data()

# --- 侧边栏：用户输入界面 ---
st.sidebar.title("🛡️ 决策参数输入")
st.sidebar.markdown("---")

# 1. 选择目标对象
target = st.sidebar.selectbox("选择分析主体 (国别/地区)", list(data_db.keys()))
base_info = data_db[target]

# 2. 关系因子与权重 (老板提出的维度)
st.sidebar.subheader("🔗 关系与排名分析")
rel_status = st.sidebar.slider("外部伙伴关系强度 (-1到1)", -1.0, 1.0, 0.2)
market_rank = st.sidebar.slider("行业/地缘排名百分比", 0, 100, 70)

# 3. 时间节点预测
st.sidebar.subheader("📅 预测时间尺度")
time_horizon = st.sidebar.select_slider("预测跨度 (年)", options=[1, 3, 5, 10])

# --- 主界面逻辑 ---
st.title(f"🌐 Gap-Compass: {target} 国运演化推演")
st.info(f"当前节点位置：{base_info['position']} | 创新指数：{base_info['innovation']} | 老龄化率：{base_info['aging']}%")

# --- 核心算法：马尔可夫多维演化 ---
# 融合用户输入的参数
tech_factor = base_info['innovation'] / 100
org_factor = (30 - base_info['aging']) / 30
press_factor = (1 - rel_status) * (market_rank / 100)

# 状态转移计算
p_s1 = min(0.9, (press_factor * 0.8 - tech_factor * 0.2)) # 坍塌概率
p_s5 = max(0.05, (tech_factor * 0.7 + org_factor * 0.3) - press_factor * 0.4) # 跃迁概率
p_s3 = 1.0 - p_s1 - p_s5

# --- 结果展示：可视化 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 状态分布预测")
    labels = ['S1:风险坍塌', 'S3:僵持平衡', 'S5:向上跃迁']
    values = [p_s1, p_s3, p_s5]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=['#ff4b4b', '#f0f2f6', '#00c0f2'])])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 演化路径趋势")
    # 模拟随时间推移的熵增或熵减
    time_series = []
    current = np.array([p_s1, p_s3, p_s5])
    for t in range(time_horizon):
        time_series.append(current)
        # 模拟扰动
        current = current * (1 + np.random.normal(0, 0.05, 3))
        current = current / current.sum()
    
    chart_data = pd.DataFrame(time_series, columns=labels)
    st.line_chart(chart_data)

# --- 战略建议板块 ---
st.markdown("---")
st.subheader("💡 Creative Gap Lab 深度策略建议")

if p_s1 > 0.4:
    st.error(f"⚠️ 预警：{target} 在该时间节点的系统脆弱性极高。高排名 ({market_rank}%) 带来了过度的‘仇恨值’。")
    st.write("**建议：** 立即降低系统暴露度，通过关系修复 (提高关系强度) 来换取喘息空间。")
elif p_s5 > 0.4:
    st.success(f"🚀 机会：{target} 正处于跃迁窗口期。")
    st.write("**建议：** 集中资源突破最后 10% 的技术 Gap，利用高创新指数实现对旧秩序的降维打击。")
else:
    st.warning("🌀 结论：系统处于高熵震荡态。")
    st.write("**建议：** 维持现状，‘翻好稻谷’，等待外部压力项的突发性减弱。")

st.caption(f"基于科技安全治理体系马尔可夫模型 | 数据节点：2026.01.16 | Creative Gap Lab")