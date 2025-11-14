# pages/2_帕金森症候群诊断.py
import streamlit as st
import pandas as pd
import numpy as np
from updrs_dia import assess_updrs_parkinson
from components.patient_info_sidebar import display_patient_info_summary

def main():
    # 显示侧边栏
    from components.current_patient_sidebar import display_current_patient_sidebar
    display_current_patient_sidebar()
    
    st.header("帕金森症候群诊断")
    
    # 创建两列布局，左侧为诊断功能，右侧显示患者信息
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("""
        Unified Parkinson's Disease Rating Scale (UPDRS) 是评估帕金森病严重程度的标准化工具。
        请上传包含UPDRS评分数据的**CSV**文件或者**手动录入**。如采用上传csv文件的方式，请确保您的CSV文件包含以下两列：**第一列**:：UPDRS-III检测项目名称，**第二列**：对应的评分值 (0-4分)
        """)
        
        # 可编辑表格界面
        st.subheader("1. UPDRS-III评分表格填充")
        uploaded_file = st.file_uploader("###### **选择UPDRS量表CSV文件或直接编辑评分表**", type="csv")
        
        # 标准的UPDRS-III检测项目
        standard_updrs_items = [
            "3.1 言语表达", "3.2 面部表情", "3.3 强直（颈+四肢）","3.4 手指叩击（右）", "3.5 手指叩击（左）", 
            "3.6 手掌握合（右）", "3.7 手掌握合（左）","3.8 前臂旋前-旋后（右）", "3.9 前臂旋前-旋后（左）", 
            "3.10 脚趾叩击（右）","3.11 脚趾叩击（左）", "3.12 足跟点地（右）", "3.13 足跟点地（左）", 
            "3.14 后拉试验", "3.15 静止性震颤（多部位）", "3.16 姿势性震颤（上肢）","3.17 运动灵活性（手指-足快速轮替）",
            "3.18 步态&冻结观察",
        ]
        
        # 初始化数据框
        if 'updrs_data' not in st.session_state:
            st.session_state.updrs_data = pd.DataFrame({
                '检测项目': standard_updrs_items,
                '评分': [0] * len(standard_updrs_items)
            })
        
        if uploaded_file is not None:
            try:
                # 读取CSV文件
                df = pd.read_csv(uploaded_file)
                
                # 检查并映射数据
                if len(df.columns) >= 2:
                    # 假设第一列是项目名称，第二列是评分
                    df_mapped = pd.DataFrame({
                        '检测项目': df.iloc[:, 0],
                        '评分': pd.to_numeric(df.iloc[:, 1], errors='coerce').fillna(0).astype(int)
                    })
                    
                    # 更新session state中的数据
                    st.session_state.updrs_data = df_mapped
                    st.success("文件上传成功！CSV数据已自动映射到评分表格中")
                else:
                    st.warning("CSV文件需要至少包含两列数据")
                
                # 显示数据基本信息
                st.subheader("数据信息")
                col1, col2= st.columns(2)
                
                with col1:
                    st.metric("检测项个数", len(df))
                with col2:
                    st.metric("缺失值数量", df.isnull().sum().sum())
                    
            except Exception as e:
                st.error(f"文件读取错误: {str(e)}")
        
        # 显示可编辑数据表格
        st.markdown("**请在下方表格中编辑UPDRS-III评分：**")
        
        # 创建可编辑的数据框
        edited_df = st.data_editor(
            st.session_state.updrs_data,
            use_container_width=True,
            num_rows="fixed",
            hide_index=True, 
            column_config={
                "检测项目": st.column_config.TextColumn(
                    "检测项目",
                    width="medium",
                    disabled=True  # 项目名称不可编辑
                ),
                "评分": st.column_config.NumberColumn(
                    "评分 (0-4分)",
                    min_value=0,
                    max_value=4,
                    step=1,
                    required=True
                )
            }
        )
        
        # 更新session state中的数据
        st.session_state.updrs_data = edited_df
            
        # 添加UPDRS帕金森评估按钮
        st.subheader("")
        st.subheader("2. 帕金森综合症诊断")
        if st.button("点击按钮进行AI诊断", type="primary"):
            with st.spinner("AI评估中..."):
                # 调用DeepSeek进行UPDRS评估
                parkinson_result = assess_updrs_parkinson(st.session_state.updrs_data)
                
                # 保存评估结果到session state
                st.session_state.parkinson_assessment = parkinson_result
                
                # 显示评估结果
                if parkinson_result['has_parkinson']:
                    st.error("🟡 疑似帕金森综合症")
                    st.info("可以继续进行绝对排除标准的鉴别诊断。")
                else:
                    st.success("🔵 非帕金森综合症")
                    st.warning("建议移交至其他科室进行进一步评估。")
                
                # 显示详细评估
                st.write("**详细评估:**")
                st.info(parkinson_result['assessment'])
                
                # 显示关键指标 - 确保parkinson_result已经定义
                col1, col2, col3 = st.columns(3)
                with col1:
                    status = "✅ 符合" if parkinson_result['core_standard_met'] else "❌ 不符合"
                    st.markdown(f"<h6 style='text-align: center;'>核心标准(运动迟缓)</h6>", unsafe_allow_html=True)
                    st.markdown(f"<h6 style='text-align: center;'>{status}</h6>", unsafe_allow_html=True)
                with col2:
                    status = "✅ 符合" if parkinson_result['rigidity_standard_met'] else "❌ 不符合"
                    st.markdown(f"<h6 style='text-align: center;'>肌强直标准</h6>", unsafe_allow_html=True)
                    st.markdown(f"<h6 style='text-align: center;'>{status}</h6>", unsafe_allow_html=True)
                with col3:
                    status = "✅ 符合" if parkinson_result['tremor_standard_met'] else "❌ 不符合"
                    st.markdown(f"<h6 style='text-align: center;'>静止性震颤</h6>", unsafe_allow_html=True)
                    st.markdown(f"<h6 style='text-align: center;'>{status}</h6>", unsafe_allow_html=True)

        # 简单的UPDRS评分分析
        st.subheader("")
        st.subheader("3. UPDRS-III评分分析")
        # 显示当前总分
        total_score = edited_df['评分'].sum()
        st.metric("##### **UPDRS-III总分**", total_score)
        
        if len(edited_df) > 0:
            scores = edited_df['评分']
            
            col1, col2, col3, col4, col0 = st.columns(5)
            with col1:
                count_1 = (scores == 1).sum()
                st.metric("##### **1分项目**", count_1)
            with col2:
                count_2 = (scores == 2).sum()
                st.metric("##### **2分项目**", count_2)
            with col3:
                count_3 = (scores == 3).sum()
                st.metric("##### **3分项目**", count_3)
            with col4:
                count_4 = (scores == 4).sum()
                st.metric("##### **4分项目**", count_4)
            with col0:
                count_0 = (scores == 0).sum()
                st.metric("##### **0分项目**", count_0)
            
            # 简单的评分分布
            st.bar_chart(scores.value_counts().sort_index())
            
            
            # 将评估结果保存到session state，以便在右侧显示
            st.session_state.severity_assessment = {
                'total_score': total_score,
            }

    with col_right:
        display_patient_info_summary()

if __name__ == "__main__":
    main()