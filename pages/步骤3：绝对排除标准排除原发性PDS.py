# pages/3_绝对排除标准.py
import streamlit as st
from aec_dia import assess_absolute_exclusion_criteria
from components.patient_info_sidebar import display_patient_info_summary

def sync_to_patient_info():
    """将排除标准数据同步回患者信息"""
    if 'exclusion_criteria' in st.session_state and 'patient_info' in st.session_state:
        exclusion = st.session_state.exclusion_criteria
        
        # 同步到患者信息
        st.session_state.patient_info.update({
            'dopamine_history': exclusion.get('drug_induced', False),
            'progressive_aphasia': exclusion.get('progressive_aphasia', False),
            'cerebellar_ataxia': exclusion.get('cerebellar_ataxia', False),
            'cerebellar_eye_movement': exclusion.get('cerebellar_oculomotor', False),
            'vertical_saccade_slowing': exclusion.get('vertical_saccade_slowing', False),
            'vertical_gaze_palsy': exclusion.get('vertical_gaze_palsy', False),
            'apraxia': exclusion.get('ideomotor_apraxia', False)
        })

def main():
    # 显示侧边栏
    from components.current_patient_sidebar import display_current_patient_sidebar
    display_current_patient_sidebar()
    
    st.header("绝对排除标准排除非典型PDS")
    
    # 在页面加载时从患者信息同步数据
    if 'patient_info' in st.session_state:
        patient_info = st.session_state.patient_info
        
        # 确保排除标准字典存在
        if 'exclusion_criteria' not in st.session_state:
            st.session_state.exclusion_criteria = {}
        
        # 从患者信息同步到排除标准
        st.session_state.exclusion_criteria.update({
            'drug_induced': patient_info.get('dopamine_history', False),
            'progressive_aphasia': patient_info.get('progressive_aphasia', False),
            'cerebellar_ataxia': patient_info.get('cerebellar_ataxia', False),
            'cerebellar_oculomotor': patient_info.get('cerebellar_eye_movement', False),
            'vertical_saccade_slowing': patient_info.get('vertical_saccade_slowing', False),
            'vertical_gaze_palsy': patient_info.get('vertical_gaze_palsy', False),
            'ideomotor_apraxia': patient_info.get('apraxia', False)
        })
    
    # 创建两列布局
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("""
        以下标准用于排除非典型帕金森综合征。如果患者符合以下任何一项标准，应重新考虑帕金森病的诊断。
        """)
        
        # 排除标准表单
        with st.form("exclusion_criteria_form"):
            st.subheader("（1/2）请确认有无9条排除标准")
            
            st.markdown("---")
            
            # 病史判断部分
            st.markdown("#### 病史判断")
            
            # 标准1: 多巴胺受体阻滞剂或多巴胺耗竭剂服用史
            drug_induced = st.checkbox(
                "标准1: 多巴胺受体阻滞剂或多巴胺耗竭剂服用史（药物性帕金森综合征）",
                value=st.session_state.exclusion_criteria.get('drug_induced', False),
                help="多巴胺受体阻滞剂或多巴胺耗竭剂治疗诱导的帕金森综合征，其剂量和时程与药物性帕金森综合征相一致。"
            )
            st.session_state.exclusion_criteria['drug_induced'] = drug_induced
            
            # 标准2: 进行性失语
            progressive_aphasia = st.checkbox(
                "标准2: 进行性失语",
                value=st.session_state.exclusion_criteria.get('progressive_aphasia', False),
                help="存在明确的进行性失语。"
            )
            st.session_state.exclusion_criteria['progressive_aphasia'] = progressive_aphasia
        
            st.markdown("---")
            
            # 体格检查判断部分
            st.markdown("#### 体格检查判断")
            
            # 标准3: 小脑性共济失调
            cerebellar_ataxia = st.checkbox(
                "标准3: 小脑性共济失调",
                value=st.session_state.exclusion_criteria.get('cerebellar_ataxia', False),
                help="存在明确的小脑性共济失调。"
            )
            st.session_state.exclusion_criteria['cerebellar_ataxia'] = cerebellar_ataxia
            
            # 标准4: 小脑性眼动异常
            cerebellar_oculomotor = st.checkbox(
                "标准4: 小脑性眼动异常",
                value=st.session_state.exclusion_criteria.get('cerebellar_oculomotor', False),
                help="小脑性眼动异常(持续的凝视诱发的眼震、巨大方波跳动、超节律扫视)。"
            )
            st.session_state.exclusion_criteria['cerebellar_oculomotor'] = cerebellar_oculomotor
            
            # 标准5: 向下的垂直性扫视选择性减慢
            vertical_saccade_slowing = st.checkbox(
                "标准5: 向下的垂直性扫视选择性减慢",
                value=st.session_state.exclusion_criteria.get('vertical_saccade_slowing', False),
                help="向下的垂直性扫视选择性减慢。"
            )
            st.session_state.exclusion_criteria['vertical_saccade_slowing'] = vertical_saccade_slowing

            # 标准6: 向下的垂直性核上性凝视麻痹
            vertical_gaze_palsy = st.checkbox(
                "标准6: 向下的垂直性核上性凝视麻痹",
                value=st.session_state.exclusion_criteria.get('vertical_gaze_palsy', False),
                help="出现向下的垂直性核上性凝视麻痹。"
            )
            st.session_state.exclusion_criteria['vertical_gaze_palsy'] = vertical_gaze_palsy
            
            # 标准7: 观念性运动性失用
            ideomotor_apraxia = st.checkbox(
                "标准7: 观念性运动性失用",
                value=st.session_state.exclusion_criteria.get('ideomotor_apraxia', False),
                help="存在明确的肢体观念运动性失用。"
            )
            st.session_state.exclusion_criteria['ideomotor_apraxia'] = ideomotor_apraxia
        
            st.markdown("---")
            
            # 病史/随访判断部分
            st.markdown("#### 病史/随访判断")
            
            # 标准8: 发病后5年内诊断FTD或PPA
            ftd_ppa = st.checkbox(
                "标准8: 发病后5年内诊断FTD或PPA",
                value=st.session_state.exclusion_criteria.get('ftd_ppa', False),
                help="在发病后5年内，患者被诊断为高度怀疑的行为变异型额颞叶痴呆或原发性进行性失语。"
            )
            st.session_state.exclusion_criteria['ftd_ppa'] = ftd_ppa
            
            # 标准9: 发病3年后仍局限于下肢的帕金森样症状
            lower_limb_parkinsonism = st.checkbox(
                "标准9: 发病3年后仍局限于下肢的帕金森样症状",
                value=st.session_state.exclusion_criteria.get('lower_limb_parkinsonism', False),
                help="发病3年后仍局限于下肢的帕金森样症状。"
            )
            st.session_state.exclusion_criteria['lower_limb_parkinsonism'] = lower_limb_parkinsonism
        
            st.markdown("---")
            
            submitted = st.form_submit_button("保存排除标准评估", type="primary")
            
            if submitted:
                # 同步数据到患者信息页面
                sync_to_patient_info()
                st.session_state.exclusion_criteria_updated = True
                st.success("排除标准评估已保存！数据已同步到患者信息页面。")
        
        # 显示评估结果
        st.markdown("")
        st.subheader("（2/2）排除标准评估结果")
        
        # 使用DeepSeek API进行评估
        if st.button("使用AI分析排除标准", type="primary"):
            with st.spinner("AI正在分析绝对排除标准..."):
                assessment_result = assess_absolute_exclusion_criteria(st.session_state.exclusion_criteria)
                
                if assessment_result:
                    st.session_state.exclusion_assessment = assessment_result
                    
                    # 显示评估结果
                    st.markdown(assessment_result.get("assessment", ""))
                    
                    # 显示详细结果
                    if assessment_result.get("is_primary_parkinson", False):
                        st.error("🟡 疑似帕金森综合症")
                        st.info("可以继续进行继发性病因的鉴别诊断。")
                    else:
                        st.success("🔵 非帕金森综合症")
                        st.warning("建议移交至其他科室进行进一步评估。")
                        
                        # 显示阳性标准详情
                        positive_details = assessment_result.get("positive_criteria_details", [])
                        if positive_details:
                            st.write("**发现的阳性排除标准:**")
                            for detail in positive_details:
                                st.write(f"• {detail}")
                else:
                    st.error("AI分析失败，请稍后重试。")

    with col_right:
        display_patient_info_summary()


if __name__ == "__main__":
    main()