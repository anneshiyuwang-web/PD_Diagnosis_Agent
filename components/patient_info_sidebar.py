# components/patient_info_sidebar.py
import streamlit as st

def display_patient_info_summary():
    """显示患者信息摘要和评估结果的侧边栏组件"""
    
    # 检查是否需要自动更新诊断标签
    check_and_update_diagnosis_tag()
    # 显示诊断标签状态提示
    current_tag = st.session_state.patient_info.get('diagnosis_tag', '疑似帕金森综合征')
    
    # 如果诊断标签已确定为继发性或非原发性，显示特殊提示
    if current_tag == '继发性帕金森综合征':
        st.error("🔴 **诊断标签已确定为: 继发性帕金森综合征**")
        st.info("由于患者存在继发性帕金森综合征相关病史，诊断标签已确定，无需进行后续诊断步骤。")
    elif current_tag == '非原发性帕金森综合征':
        st.error("🔵 **诊断标签已确定为: 非原发性帕金森综合征**")
        st.info("由于患者存在绝对排除标准的体征，诊断标签已确定，无需进行后续诊断步骤。")
    
    # 显示当前患者信息 - 步骤1
    st.subheader("步骤1\n ##### 患者基本信息及体格检查")
    if st.session_state.patient_info.get('name'):
        st.write(f"**姓名:** {st.session_state.patient_info['name']}")
        st.write(f"**性别:** {st.session_state.patient_info['gender']}")
        st.write(f"**出生日期:** {st.session_state.patient_info['birth_date']}")
        st.write(f"**年龄:** {st.session_state.patient_info.get('age', '')}岁")
        st.write(f"**建档日期:** {st.session_state.patient_info['record_date']}")
        
        # 显示继发性帕金森综合征相关病史
        st.write("**继发性帕金森综合征相关病史:**")
        secondary_symptoms = []
        if st.session_state.patient_info.get('head_trauma'):
            secondary_symptoms.append("严重头部外伤史（继发性帕金森综合征）")
        if st.session_state.patient_info.get('drug_induced_parkinson'):
            secondary_symptoms.append("药物性帕金森综合征（继发性帕金森综合征）")
        if st.session_state.patient_info.get('toxic_induced_parkinson'):
            secondary_symptoms.append("中毒性帕金森综合征（继发性帕金森综合征）")
        if st.session_state.patient_info.get('none_secondary_history'):
            secondary_symptoms.append("无")
        
        if secondary_symptoms:
            for symptom in secondary_symptoms:
                st.write(f"{symptom}")
        else:
            st.write("无")
        
        # 显示体格检查选择
        st.write("**体格检查绝对排除项:**")
        exam_signs = []
        # 在体格检查显示部分添加
        if st.session_state.patient_info.get('orthostatic_hypotension'):
            exam_signs.append("体位性低血压")
        if st.session_state.patient_info.get('cerebellar_ataxia'):
            exam_signs.append("小脑性共济失调")
        if st.session_state.patient_info.get('cerebellar_eye_movement'):
            exam_signs.append("小脑性眼动异常")
        if st.session_state.patient_info.get('vertical_saccade_slowing'):
            exam_signs.append("向下的垂直性扫视选择性减慢")
        if st.session_state.patient_info.get('vertical_gaze_palsy'):
            exam_signs.append("向下的垂直性核上性凝视麻痹")
        if st.session_state.patient_info.get('apraxia'):
            exam_signs.append("观念性运动性失用或进行性失语")
        if st.session_state.patient_info.get('no_exam_symptoms'):
            exam_signs.append("无")
        
        if exam_signs:
            for sign in exam_signs:
                st.write(f"{sign}")
        else:
            st.write("无")
        
        # 只在诊断标签未确定时显示后续步骤
        if current_tag == '疑似帕金森综合征':
            # UPDRS结果评估 - 步骤2
            if hasattr(st.session_state, 'parkinson_assessment'):
                parkinson_info = st.session_state.parkinson_assessment
                st.markdown("---")  # 添加分隔线
                st.subheader("步骤2\n ##### UPDRS-III量表识别PDS")
                
                # 显示诊断结果
                if parkinson_info['has_parkinson']:
                    st.error("🟡 疑似帕金森综合症")
                    st.info("可以继续进行绝对排除标准的鉴别诊断。")
                else:
                    st.success("🔵 非帕金森综合症")
                    st.warning("建议移交至其他科室进行进一步评估。")
                    # 更新诊断标签为非原发性帕金森综合征
                    st.session_state.patient_info['diagnosis_tag'] = '非原发性帕金森综合征'
                
                # 显示关键指标
                col1, col2, col3 = st.columns(3)
                with col1:
                    status = "✅ 符合" if parkinson_info['core_standard_met'] else "❌ 不符合"
                    st.markdown(f"<h6 style='text-align: center;'>核心标准</h6>", unsafe_allow_html=True)
                    st.markdown(f"<h6 style='text-align: center;'>{status}</h6>", unsafe_allow_html=True)
                with col2:
                    status = "✅ 符合" if parkinson_info['rigidity_standard_met'] else "❌ 不符合"
                    st.markdown(f"<h6 style='text-align: center;'>肌强直</h6>", unsafe_allow_html=True)
                    st.markdown(f"<h6 style='text-align: center;'>{status}</h6>", unsafe_allow_html=True)
                with col3:
                    status = "✅ 符合" if parkinson_info['tremor_standard_met'] else "❌ 不符合"
                    st.markdown(f"<h6 style='text-align: center;'>静止性震颤</h6>", unsafe_allow_html=True)
                    st.markdown(f"<h6 style='text-align: center;'>{status}</h6>", unsafe_allow_html=True)
                
                # 显示详细评估结果
                st.markdown("**评估详情:**")
                st.markdown(parkinson_info['assessment'])
            
                # 绝对排除标准评估结果 - 步骤3
                if hasattr(st.session_state, 'exclusion_assessment'):
                    exclusion_info = st.session_state.exclusion_assessment
                    st.markdown("---")  # 添加分隔线
                    st.subheader("步骤3\n ##### 绝对排除标准评估")
                    
                    # 显示诊断结果
                    if exclusion_info.get("is_primary_parkinson", False):
                        st.error("🟡 疑似帕金森综合症")
                        st.info("可以继续进行继发性病因的鉴别诊断。")
                        # 更新诊断标签为疑似帕金森综合征
                        st.session_state.patient_info['diagnosis_tag'] = '疑似帕金森综合征'
                        
                        # 原发型与继发型辨别结果 - 步骤4（只有在步骤3完成后才显示）
                        st.markdown("---")  # 添加分隔线
                        st.subheader("步骤4\n ##### 原发型与继发型辨别")
                        
                        # 显示步骤4的汇总结果
                        page4_final_result = get_page4_final_result()
                        if page4_final_result:
                            if page4_final_result == "疑似帕金森综合征":
                                st.error(f"🟡 **{page4_final_result}**")
                                # st.info("血检、CT和MRI检查均未发现继发性因素")
                            else:
                                st.success(f"🔴 **{page4_final_result}**")
                                # st.info("发现继发性帕金森综合征相关证据")
                        
                        st.markdown("###### 1. 常规血检")
                        
                        # 检查是否有原发型与继发型辨别结果
                        if (hasattr(st.session_state, 'lab_data') and 
                            hasattr(st.session_state, 'ai_analysis_result') and 
                            st.session_state.ai_analysis_result is not None):
                            
                            result = st.session_state.ai_analysis_result
                            abnormal_items = result['abnormal_items']
                            selected_conditions = st.session_state.get('selected_conditions', [])
                            
                            # 根据当前选择的条件实时确定诊断类型
                            current_diagnosis_type = get_diagnosis_type_from_conditions(selected_conditions)
                            
                            # 显示AI分析结果
                            if current_diagnosis_type == "继发性帕金森综合征":
                                st.success("🔴 **继发性帕金森综合征**")
                            else:
                                st.error("🟡  **疑似帕金森综合征**")
                            
                            # 显示异常项目
                            if abnormal_items:
                                st.write("**异常发现:**")
                                for item in abnormal_items:
                                    st.write(f"• {item}")
                            
                            # 显示医生确认的病因
                            if selected_conditions:
                                st.write("**确认的病因:**")
                                for condition in selected_conditions:
                                    st.write(f"• {condition}")
                        else:
                            st.info("尚未进行原发型与继发型辨别")
                            st.write("请前往'原发型与继发型辨别'页面进行检查")
                        
                        # 显示CT检查结果
                        st.markdown("###### 2. 颅脑CT检查")
                        if hasattr(st.session_state, 'ct_data') and st.session_state.ct_data['findings']:
                            ct_findings = st.session_state.ct_data['findings']
                            if "无异常发现" in ct_findings:
                                st.error("🟡 **疑似帕金森综合征**")
                            else:
                                st.success("🔴 **继发性帕金森综合征**")
                                st.write(f"**发现:** {', '.join(ct_findings)}")
                        else:
                            st.info("尚未进行CT检查")
                        
                        # 显示MRI检查结果
                        st.markdown("###### 3. 头颅MRI检查")
                        if hasattr(st.session_state, 'mri_data') and st.session_state.mri_data['findings']:
                            mri_findings = st.session_state.mri_data['findings']
                            if "无异常发现" in mri_findings:
                                st.error("🟡 **疑似帕金森综合征**")
                            else:
                                st.success("🔴 **继发性帕金森综合征**")
                                st.write(f"**发现:** {', '.join(mri_findings)}")
                        else:
                            st.info("尚未进行MRI检查")
                        
                        # 原发型与叠加型辨别结果 - 步骤5（只有在步骤4完成且结果为疑似时才显示）
                        if page4_final_result == "疑似帕金森综合征":
                            st.markdown("---")  # 添加分隔线
                            st.subheader("步骤5\n ##### 原发型与叠加型辨别")
                            
                            # 显示步骤5的结果
                            page5_result = get_page5_final_result()
                            if page5_result:
                                if page5_result == "原发性帕金森病":
                                    st.success("🟢 **原发性帕金森综合征**")
                                else:
                                    st.error("🟣 **叠加性帕金森综合征**")
                                
                                # 显示警示征象和支持条件统计
                                warning_signs = st.session_state.get('page5_warning_signs', [])
                                supportive_criteria = st.session_state.get('page5_supportive_criteria', [])
                                
                                if warning_signs:
                                    st.write(f"**警示征象:** {len(warning_signs)}条")
                                if supportive_criteria:
                                    st.write(f"**支持条件:** {len(supportive_criteria)}条")
                            else:
                                st.info("尚未进行原发型与叠加型辨别")
                                st.write("请前往'原发型与叠加型辨别'页面进行评估")
                    
                    else:
                        st.success("🔵 非帕金森综合症")
                        st.warning("建议移交至其他科室进行进一步评估。")
                        # 更新诊断标签为非原发性帕金森综合征
                        st.session_state.patient_info['diagnosis_tag'] = '非原发性帕金森综合征'
                else:
                    # 如果没有任何评估结果，显示提示信息
                    st.markdown("---")  # 添加分隔线
                    st.subheader("步骤3\n ##### 绝对排除标准评估")
                    st.info("尚未进行绝对排除标准评估")
                    st.write("请在左侧进行绝对排除标准评估")
            else:
                # 如果没有任何评估结果，显示提示信息
                st.markdown("---")  # 添加分隔线
                st.subheader("步骤2\n ##### UPDRS-III量表识别PDS")
                st.info("尚未进行UPDRS评估")
                st.write("请前往'帕金森症候群诊断'页面进行UPDRS评分")
            
    else:
        st.info("尚未录入患者信息")
        st.write("请先在'患者基本信息录入'页面填写患者信息")

def get_page4_final_result():
    """获取步骤4的最终结果"""
    # 检查三种检查是否都完成
    blood_completed = (hasattr(st.session_state, 'ai_analysis_result') and 
                      st.session_state.ai_analysis_result is not None and
                      hasattr(st.session_state, 'selected_conditions') and
                      st.session_state.selected_conditions)
    
    ct_completed = (hasattr(st.session_state, 'ct_data') and 
                   st.session_state.ct_data['findings'])
    
    mri_completed = (hasattr(st.session_state, 'mri_data') and 
                    st.session_state.mri_data['findings'])
    
    if not (blood_completed and ct_completed and mri_completed):
        return None  # 检查未完成
    
    # 检查血检结果
    blood_result = "疑似帕金森综合征"
    if st.session_state.selected_conditions and "无" not in st.session_state.selected_conditions:
        blood_result = "继发性帕金森综合征"
    
    # 检查CT结果
    ct_result = "疑似帕金森综合征"
    ct_findings = st.session_state.ct_data['findings']
    if "无异常发现" not in ct_findings:
        ct_result = "继发性帕金森综合征"
    
    # 检查MRI结果
    mri_result = "疑似帕金森综合征"
    mri_findings = st.session_state.mri_data['findings']
    if "无异常发现" not in mri_findings:
        mri_result = "继发性帕金森综合征"
    
    # 只有三种检查结果都为【疑似帕金森综合征】才返回【疑似帕金森综合征】
    if blood_result == "疑似帕金森综合征" and ct_result == "疑似帕金森综合征" and mri_result == "疑似帕金森综合征":
        return "疑似帕金森综合征"
    else:
        return "继发性帕金森综合征"

def get_page5_final_result():
    """获取步骤5的最终结果"""
    if hasattr(st.session_state, 'page5_diagnosis_result') and st.session_state.page5_diagnosis_result is not None:
        return st.session_state.page5_diagnosis_result
    return None

def get_diagnosis_type_from_conditions(selected_conditions):
    """根据选择的病因确定诊断类型"""
    if "无" in selected_conditions:
        return "原发性帕金森综合征"
    else:
        return "继发性帕金森综合征"

def check_and_update_diagnosis_tag():
    """检查并自动更新诊断标签"""
    if 'patient_info' not in st.session_state:
        return
    
    patient_info = st.session_state.patient_info
    
    # 首先检查步骤5的结果（最高优先级）
    page5_result = get_page5_final_result()
    if page5_result:
        if page5_result == "原发性帕金森病":
            st.session_state.patient_info['diagnosis_tag'] = '原发性帕金森综合征'
            return
        else:
            st.session_state.patient_info['diagnosis_tag'] = '叠加性帕金森综合征'
            return
    
    # 检查继发性帕金森综合征相关病史
    has_secondary_history = (
        patient_info.get('head_trauma', False) or 
        patient_info.get('drug_induced_parkinson', False) or 
        patient_info.get('toxic_induced_parkinson', False)
    )
    
    # 检查体格检查绝对排除项
    has_exclusion_signs = (
        patient_info.get('orthostatic_hypotension', False) or 
        patient_info.get('cerebellar_ataxia', False) or 
        patient_info.get('cerebellar_eye_movement', False) or 
        patient_info.get('vertical_saccade_slowing', False) or 
        patient_info.get('vertical_gaze_palsy', False) or 
        patient_info.get('apraxia', False)
    )
    
    # 根据条件更新诊断标签
    if has_secondary_history:
        st.session_state.patient_info['diagnosis_tag'] = '继发性帕金森综合征'
    elif has_exclusion_signs:
        st.session_state.patient_info['diagnosis_tag'] = '非原发性帕金森综合征'
    # 如果既没有继发性病史也没有排除体征，保持为疑似帕金森综合征
    else:
        st.session_state.patient_info['diagnosis_tag'] = '疑似帕金森综合征'