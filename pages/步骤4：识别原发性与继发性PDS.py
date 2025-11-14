# pages/4_原发型与继发型辨别.py
import streamlit as st
import pandas as pd
import io
from components.patient_info_sidebar import display_patient_info_summary
from ai_blood_analysis import blood_analyzer

def create_default_lab_data():
    """创建默认的血检数据表格"""
    default_data = {
        '项目': ['传染病筛查', '传染病筛查', '肝功能', '肝功能', '肝功能', '肾功能', '肾功能', 
                '电解质', '电解质', '电解质', '电解质', '甲状腺功能', '甲状腺功能', '甲状腺功能', '甲状旁腺功能'],
        '名称': ['梅毒抗体', 'HIV抗体', '谷丙转氨酶(ALT)', '谷草转氨酶(AST)', '总胆红素(TBIL)', 
                '肌酐(Cr)', '尿素氮(BUN)', '钠(Na)', '钾(K)', '氯(Cl)', '钙(Ca)', 
                '游离T3(FT3)', '游离T4(FT4)', '促甲状腺激素(TSH)', '甲状旁腺激素(PTH)'],
        '结果': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        '单位': ['阴性/阳性', '阴性/阳性', 'U/L', 'U/L', 'umol/L', 'umol/L', 'mmol/L', 
                'mmol/L', 'mmol/L', 'mmol/L', 'mmol/L', 'pmol/L', 'pmol/L', 'mIU/L', 'pg/mL'],
        '参考值': ['阴性', '阴性', '0-40', '0-40', '3.4-20.5', '44-133', '2.5-7.1', 
                 '135-145', '3.5-5.5', '96-106', '2.1-2.7', '3.5-6.5', '11.5-22.7', '0.3-5.0', '15-65']
    }
    return pd.DataFrame(default_data)

def validate_uploaded_csv(df):
    """验证上传的CSV文件格式"""
    required_columns = ['项目', '名称', '结果', '单位', '参考值']
    
    # 检查是否包含所有必需列
    if not all(col in df.columns for col in required_columns):
        return False, f"CSV文件必须包含以下列: {', '.join(required_columns)}"
    
    # 检查关键检测项目是否存在
    required_items = ['梅毒', 'HIV', '肝功能', '肾功能', '电解质', '甲状腺功能', '甲状旁腺']
    existing_names = df['名称'].astype(str).values
    
    missing_items = []
    for item in required_items:
        # 检查名称中是否包含关键词
        if not any(item in name for name in existing_names):
            missing_items.append(item)
    
    if missing_items:
        return False, f"缺少以下关键检测项目: {', '.join(missing_items)}"
    
    return True, "文件格式正确"

def get_final_diagnosis(selected_conditions):
    """根据选择的病因确定最终诊断"""
    if "无" in selected_conditions:
        return "疑似帕金森综合征"
    elif any(cond in selected_conditions for cond in ["梅毒", "HIV"]):
        return "感染性帕金森综合征（继发性）"
    elif any(cond in selected_conditions for cond in ["电解质紊乱", "甲状腺功能亢进", "甲状旁腺功能异常", "肝豆状核变性"]):
        return "内分泌或代谢所致的帕金森综合征（继发性）"
    else:
        return "待进一步确认"

def get_diagnosis_type_from_conditions(selected_conditions):
    """根据选择的病因确定诊断类型"""
    if "无" in selected_conditions:
        return "原发性帕金森综合征"
    else:
        return "继发性帕金森综合征"

def setup_deepseek_client():
    """设置DeepSeek客户端"""
    try:
        from deepseek_client import deepseek_client
        # 设置API密钥（在实际应用中应该从环境变量获取）
        # deepseek_client.api_key = "your_api_key_here"
        blood_analyzer.deepseek_client = deepseek_client
        return True
    except ImportError:
        st.warning("DeepSeek客户端未找到，将使用基于规则的分析方法。")
        return False

def update_diagnosis_based_on_imaging():
    """根据影像学检查结果更新诊断标签"""
    # 检查CT和MRI是否有异常发现
    ct_has_abnormal = any(finding in st.session_state.ct_data['findings'] 
                         for finding in ["正常压力性脑积水", "Fahr病"])
    mri_has_abnormal = any(finding in st.session_state.mri_data['findings'] 
                          for finding in ["脑炎", "正常压力性脑积水", "血管性帕金森综合征"])
    
    # 如果CT或MRI有异常发现，更新为继发性帕金森综合征
    if ct_has_abnormal or mri_has_abnormal:
        st.session_state.patient_info['diagnosis_tag'] = '继发性帕金森综合征'
        return "继发性帕金森综合征"
    else:
        # 如果没有异常发现，保持原诊断标签
        current_tag = st.session_state.patient_info.get('diagnosis_tag', '疑似帕金森综合征')
        return current_tag

def main():
    # 显示侧边栏
    from components.current_patient_sidebar import display_current_patient_sidebar
    display_current_patient_sidebar()
    
    st.header("原发型与继发型帕金森病辨别")
    
    # 检查患者信息是否已录入
    if not st.session_state.patient_info['name']:
        st.warning("请先在'患者基本信息录入'页面填写患者信息")
        return
    
    # 初始化session state
    if 'lab_data' not in st.session_state:
        st.session_state.lab_data = create_default_lab_data()
    if 'ct_data' not in st.session_state:
        st.session_state.ct_data = {'image': None, 'conclusion': '', 'findings': []}
    if 'mri_data' not in st.session_state:
        st.session_state.mri_data = {'image': None, 'conclusion': '', 'findings': []}
    if 'ai_analysis_result' not in st.session_state:
        st.session_state.ai_analysis_result = None
    if 'selected_conditions' not in st.session_state:
        st.session_state.selected_conditions = []
    
    # 设置DeepSeek客户端
    if blood_analyzer.deepseek_client is None:
        setup_deepseek_client()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 1. 常规血检数据上传
        st.subheader("1. 常规血检数据")
        
        # 创建默认模板的CSV
        template_df = create_default_lab_data()
        csv_buffer = io.StringIO()
        template_df.to_csv(csv_buffer, index=False)
        csv_str = csv_buffer.getvalue()
        
        st.download_button(
            label="下载CSV模板",
            data=csv_str,
            file_name="血检数据模板.csv",
            mime="text/csv",
            help="下载包含所有必需项目的CSV模板文件"
        )
        
        # 文件上传部分
        uploaded_file = st.file_uploader("上传血检CSV文件", type=['csv'], 
                                    help="请上传包含项目、名称、结果、单位、参考值的CSV文件")
        
        if uploaded_file is not None:
            try:
                # 读取CSV文件
                df = pd.read_csv(uploaded_file)
                st.session_state.lab_data = df
                st.success("CSV文件上传成功！数据已加载到下方表格中。")
                    
            except Exception as e:
                st.error(f"文件读取错误: {str(e)}")
                st.info("请确保CSV文件格式正确，包含以下列: 项目, 名称, 结果, 单位, 参考值")
        
        # 创建标题和重置按钮的布局
        header_col1, header_col2 = st.columns([1, 1])
        
        with header_col1:
            st.write("**血检数据编辑:**")
        
        with header_col2:
            # 将重置按钮放在右侧
            if st.button("重置为默认数据", use_container_width=True):
                st.session_state.lab_data = create_default_lab_data()
                st.session_state.ai_analysis_result = None
                st.session_state.selected_conditions = []
                st.session_state.ct_data = {'image': None, 'conclusion': '', 'findings': []}
                st.session_state.mri_data = {'image': None, 'conclusion': '', 'findings': []}
                st.rerun()
        
        # 使用data_editor创建可编辑表格
        edited_df = st.data_editor(
            st.session_state.lab_data,
            column_config={
                "项目": st.column_config.TextColumn("项目", disabled=True),
                "名称": st.column_config.TextColumn("名称", disabled=True),
                "结果": st.column_config.TextColumn("结果"),
                "单位": st.column_config.TextColumn("单位", disabled=True),
                "参考值": st.column_config.TextColumn("参考值", disabled=True)
            },
            use_container_width=True,
            num_rows="fixed",
            key="lab_data_editor"
        )
        
        # 更新session state中的数据
        st.session_state.lab_data = edited_df
        
        # 检查是否有未填写的结果
        missing_results = edited_df[edited_df['结果'].isna() | (edited_df['结果'].astype(str) == '')]
        
        # 检查关键项目是否存在
        required_key_items = ['梅毒', 'HIV']
        existing_names = edited_df['名称'].astype(str).values
        missing_key_items = [item for item in required_key_items if not any(item in name for name in existing_names)]
        
        if len(missing_results) > 0:
            st.warning(f"还有 {len(missing_results)} 个项目的结果未填写")
            if st.checkbox("显示未完成项目"):
                st.dataframe(missing_results[['项目', '名称']], use_container_width=True)
        
        if missing_key_items:
            st.error(f"❌ 缺少关键检测项目: {', '.join(missing_key_items)}")
        elif len(missing_results) == 0:
            st.success("✅ 所有血检项目已完成填写且关键项目齐全")
            
            # 添加AI分析按钮
            if st.button("AI分析血检数据", type="primary", use_container_width=True):
                with st.spinner("AI正在分析血检数据..."):
                    analysis_result = blood_analyzer.analyze_blood_tests(edited_df)
                    st.session_state.ai_analysis_result = analysis_result
                    # 根据AI建议设置初始选择
                    st.session_state.selected_conditions = analysis_result.get('suggested_conditions', [])
        
        # 在page4的AI分析结果部分，添加诊断标签更新逻辑
        if st.session_state.ai_analysis_result:
            
            result = st.session_state.ai_analysis_result
            abnormal_items = result['abnormal_items']
            reasoning = result['reasoning']
            
            st.info(f"**分析推理**: {reasoning}")
            
            # 条件选择框
            st.markdown("##### 病因确认（医生校正）")
            st.write("请根据AI分析结果和临床判断，确认以下病因：")
            
            # 所有可能的条件
            all_conditions = ["梅毒", "HIV", "电解质紊乱", "甲状腺功能亢进", "甲状旁腺功能异常", "肝豆状核变性", "无"]
            
            # 创建选择框
            selected_conditions = []
            cols = st.columns(3)
            
            for i, condition in enumerate(all_conditions):
                with cols[i % 3]:
                    is_selected = st.checkbox(
                        condition, 
                        value=condition in st.session_state.selected_conditions,
                        key=f"condition_{condition}"
                    )
                    if is_selected:
                        selected_conditions.append(condition)
            
            # 更新选择的条件
            st.session_state.selected_conditions = selected_conditions
            
            # 验证选择逻辑
            if "无" in selected_conditions and len(selected_conditions) > 1:
                st.warning("选择'无'时不应同时选择其他病因，已自动取消其他选择。")
                st.session_state.selected_conditions = ["无"]
                st.rerun()
            
            # 显示最终诊断
            final_diagnosis = get_final_diagnosis(st.session_state.selected_conditions)
            
            # 根据最终诊断更新诊断标签
            if "继发性" in final_diagnosis:
                st.error(f"**最终诊断**: {final_diagnosis}")
                # 更新诊断标签为继发性帕金森综合征
                st.session_state.patient_info['diagnosis_tag'] = '继发性帕金森综合征'
            else:
                st.success(f"**最终诊断**: {final_diagnosis}")
                # 更新诊断标签为疑似帕金森综合征
                st.session_state.patient_info['diagnosis_tag'] = '疑似帕金森综合征'

        # 2. 颅脑CT检查
        st.subheader("2. 颅脑CT检查")
        
        ct_col1, ct_col2 = st.columns([1, 2])
        
        with ct_col1:
            ct_image = st.file_uploader("上传颅脑CT图像", type=['jpg', 'jpeg', 'png'], 
                                    key="ct_uploader")
            if ct_image is not None:
                st.session_state.ct_data['image'] = ct_image
                st.image(ct_image, caption="颅脑CT图像", use_column_width=True)
        
        with ct_col2:
            ct_conclusion = st.text_area("CT检查结论", 
                                    value=st.session_state.ct_data['conclusion'],
                                    placeholder="请输入CT检查的影像学结论...",
                                    height=100,
                                    key="ct_conclusion")
            st.session_state.ct_data['conclusion'] = ct_conclusion
            
            # CT检查发现 - 使用单选按钮实现互斥关系
            st.write("**影像学发现（单选）**")
            
            # 获取当前选中的CT发现
            current_ct_findings = st.session_state.ct_data.get('findings', [])
            current_ct_selection = "无异常发现"  # 默认值
            
            if "正常压力性脑积水" in current_ct_findings:
                current_ct_selection = "正常压力性脑积水"
            elif "Fahr病" in current_ct_findings:
                current_ct_selection = "Fahr病"
            elif "无异常发现" in current_ct_findings:
                current_ct_selection = "无异常发现"
            
            # 在CT单选按钮后添加
            ct_option = st.radio(
                "选择CT发现:",
                ["无异常发现", "正常压力性脑积水", "Fahr病"],
                index=["无异常发现", "正常压力性脑积水", "Fahr病"].index(current_ct_selection),
                key="ct_radio"
            )

            # 根据选择更新findings
            if ct_option == "无异常发现":
                st.session_state.ct_data['findings'] = ["无异常发现"]
            elif ct_option == "正常压力性脑积水":
                st.session_state.ct_data['findings'] = ["正常压力性脑积水"]
            elif ct_option == "Fahr病":
                st.session_state.ct_data['findings'] = ["Fahr病"]

            # 立即更新诊断标签
            if ct_option != "无异常发现":
                st.session_state.patient_info['diagnosis_tag'] = '继发性帕金森综合征'
            else:
                # 只有当其他检查也没有发现继发性因素时才更新为疑似
                from components.current_patient_sidebar import get_page4_final_result_for_sidebar
                page4_result = get_page4_final_result_for_sidebar()
                if page4_result == "疑似帕金森综合征":
                    st.session_state.patient_info['diagnosis_tag'] = '疑似帕金森综合征'
        
        # 3. 头颅MRI检查
        st.subheader("3. 头颅MRI检查")
        
        mri_col1, mri_col2 = st.columns([1, 2])
        
        with mri_col1:
            mri_image = st.file_uploader("上传头颅MRI图像", type=['jpg', 'jpeg', 'png'], 
                                    key="mri_uploader")
            if mri_image is not None:
                st.session_state.mri_data['image'] = mri_image
                st.image(mri_image, caption="头颅MRI图像", use_column_width=True)
        
        with mri_col2:
            mri_conclusion = st.text_area("MRI检查结论", 
                                        value=st.session_state.mri_data['conclusion'],
                                        placeholder="请输入MRI检查的影像学结论...",
                                        height=100,
                                        key="mri_conclusion")
            st.session_state.mri_data['conclusion'] = mri_conclusion
            
            # MRI检查发现 - 使用单选按钮实现互斥关系
            st.write("**影像学发现（单选）**")
            
            # 获取当前选中的MRI发现
            current_mri_findings = st.session_state.mri_data.get('findings', [])
            current_mri_selection = "无异常发现"  # 默认值
            
            if "脑炎" in current_mri_findings:
                current_mri_selection = "脑炎"
            elif "正常压力性脑积水" in current_mri_findings:
                current_mri_selection = "正常压力性脑积水"
            elif "血管性帕金森综合征" in current_mri_findings:
                current_mri_selection = "血管性帕金森综合征"
            elif "无异常发现" in current_mri_findings:
                current_mri_selection = "无异常发现"
            
            # 在MRI单选按钮后添加类似的代码
            mri_option = st.radio(
                "选择MRI发现:",
                ["无异常发现", "脑炎", "正常压力性脑积水", "血管性帕金森综合征"],
                index=["无异常发现", "脑炎", "正常压力性脑积水", "血管性帕金森综合征"].index(current_mri_selection),
                key="mri_radio"
            )

            # 根据选择更新findings
            if mri_option == "无异常发现":
                st.session_state.mri_data['findings'] = ["无异常发现"]
            elif mri_option == "脑炎":
                st.session_state.mri_data['findings'] = ["脑炎"]
            elif mri_option == "正常压力性脑积水":
                st.session_state.mri_data['findings'] = ["正常压力性脑积水"]
            elif mri_option == "血管性帕金森综合征":
                st.session_state.mri_data['findings'] = ["血管性帕金森综合征"]

            # 立即更新诊断标签
            if mri_option != "无异常发现":
                st.session_state.patient_info['diagnosis_tag'] = '继发性帕金森综合征'
            else:
                # 只有当其他检查也没有发现继发性因素时才更新为疑似
                from components.current_patient_sidebar import get_page4_final_result_for_sidebar
                page4_result = get_page4_final_result_for_sidebar()
                if page4_result == "疑似帕金森综合征":
                    st.session_state.patient_info['diagnosis_tag'] = '疑似帕金森综合征'
        
        # 综合诊断结果
        st.markdown("---")
        st.subheader("综合诊断结果")
        
        # 根据影像学检查结果更新诊断
        final_diagnosis = update_diagnosis_based_on_imaging()
        
        if final_diagnosis == "继发性帕金森综合征":
            st.error("🔴 **最终诊断: 继发性帕金森综合征**")
            st.info("根据影像学检查发现继发性病因")
        else:
            # 检查血检结果
            if (st.session_state.ai_analysis_result and 
                st.session_state.selected_conditions and 
                "无" in st.session_state.selected_conditions):
                st.success("🟢 **最终诊断: 疑似帕金森综合征**")
                st.info("血检和影像学检查均未发现继发性因素")
            else:
                st.warning("🟡 **诊断状态: 待进一步确认**")
                st.info("请完成血检和影像学检查以确定诊断")
    
    with col2:
        display_patient_info_summary()

if __name__ == "__main__":
    main()