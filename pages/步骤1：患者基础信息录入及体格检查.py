# pages/1_患者基本信息录入.py
import streamlit as st
from datetime import datetime, date
import math
from components.patient_info_sidebar import display_patient_info_summary

def calculate_age(birth_date):
    """根据出生日期计算当前年龄"""
    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def sync_exclusion_criteria():
    """同步排除标准数据"""
    # 确保排除标准字典存在
    if 'exclusion_criteria' not in st.session_state:
        st.session_state.exclusion_criteria = {
            'drug_induced': False,
            'progressive_aphasia': False,
            'cerebellar_ataxia': False,
            'cerebellar_oculomotor': False,
            'vertical_saccade_slowing': False,
            'vertical_gaze_palsy': False,
            'ideomotor_apraxia': False,
            'ftd_ppa': False,
            'lower_limb_parkinsonism': False
        }
    
    # 从患者信息同步到排除标准
    if 'patient_info' in st.session_state:
        patient_info = st.session_state.patient_info
        
        # 病史判断同步
        st.session_state.exclusion_criteria['drug_induced'] = patient_info.get('dopamine_history', False)
        st.session_state.exclusion_criteria['progressive_aphasia'] = patient_info.get('progressive_aphasia', False)
        
        # 体格检查判断同步
        st.session_state.exclusion_criteria['cerebellar_ataxia'] = patient_info.get('cerebellar_ataxia', False)
        st.session_state.exclusion_criteria['cerebellar_oculomotor'] = patient_info.get('cerebellar_eye_movement', False)
        st.session_state.exclusion_criteria['vertical_saccade_slowing'] = patient_info.get('vertical_saccade_slowing', False)
        st.session_state.exclusion_criteria['vertical_gaze_palsy'] = patient_info.get('vertical_gaze_palsy', False)
        st.session_state.exclusion_criteria['ideomotor_apraxia'] = patient_info.get('apraxia', False)

def main():
    # 显示侧边栏
    from components.current_patient_sidebar import display_current_patient_sidebar
    display_current_patient_sidebar()
    st.header("患者基本信息录入")
    
    # 在页面加载时同步数据
    sync_exclusion_criteria()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("patient_info_form"):
            # 基本信息部分
            st.subheader("1. 基本信息")
            
            name = st.text_input("**患者姓名**", 
                                value=st.session_state.patient_info.get('name', ''),
                                placeholder="请输入患者姓名")
            
            gender = st.selectbox("**性别**", 
                                ["请选择", "男", "女"], 
                                index=0 if not st.session_state.patient_info.get('gender') else 
                                ["男", "女"].index(st.session_state.patient_info.get('gender', '')) + 1)
            
            # 出生日期设置
            min_date = date(1900, 1, 1)
            max_date = datetime.now().date()
            
            saved_birth_date = st.session_state.patient_info.get('birth_date')
            if saved_birth_date:
                if isinstance(saved_birth_date, datetime):
                    saved_birth_date = saved_birth_date.date()
                default_date = saved_birth_date
            else:
                default_date = date(max_date.year - 30, 1, 1)
            
            birth_date = st.date_input("**出生日期**", 
                                    value=default_date,
                                    min_value=min_date,
                                    max_value=max_date,
                                    key="birth_date_input")
            
            if birth_date:
                age = calculate_age(birth_date)
                st.write(f"**当前年龄:** {age}岁")
            else:
                st.write("**当前年龄:** 请选择出生日期")

            allergy_history = st.text_area(
                "**过敏史**",
                value=st.session_state.patient_info.get('allergy_history', ''),
                height=100,
                placeholder="请输入患者的过敏史信息"
            )
            
            # 自动建档日期
            record_date = datetime.now().date()
            st.text_input("**建档日期**", value=record_date.strftime("%Y-%m-%d"), disabled=True)
        
            # 主诉
            chief_complaint = st.text_area(
                "**主诉**",
                value=st.session_state.patient_info.get('chief_complaint', ''),
                height=80,
                placeholder="请输入患者的主要症状和持续时间"
            )
            
            # 病史部分
            st.subheader("2. 病史信息")
            
            # 详细病史
            medical_history = st.text_area(
                "**现病史/既往史/个人史/家族史**",
                value=st.session_state.patient_info.get('medical_history', ''),
                height=150,
                placeholder="优化:通过模型自动语意识别勾选相关体征,\n请输入患者的详细病史信息：\n• 现病史\n• 既往史\n• 个人史\n• 家族史"
            )
            
            # 删除的症状勾选框部分已移除
            
            # 新增：继发性帕金森综合征相关病史选项
            st.write("**继发性帕金森综合征相关病史（至少选择一项）**")
            secondary_col1, secondary_col2, secondary_col3, secondary_col4 = st.columns(4)
            
            with secondary_col1:
                head_trauma = st.checkbox("严重头部外伤史", 
                                        value=st.session_state.patient_info.get('head_trauma', False),
                                        key="head_trauma_checkbox")
            
            with secondary_col2:
                drug_induced_parkinson = st.checkbox("药物性帕金森综合征", 
                                                   value=st.session_state.patient_info.get('drug_induced_parkinson', False),
                                                   key="drug_induced_parkinson_checkbox")
                if drug_induced_parkinson:
                    st.info("是否使用抗精神病药物如氟哌啶醇、利培酮、奥氮平等；止吐药：如甲氧氯普胺（胃复安）；降压药：利血平等，其他：某些钙通道阻滞剂（如氟桂利嗪）、抗抑郁药等；其剂量和时程与药物性帕金森综合征相一致。")
            
            with secondary_col3:
                toxic_induced_parkinson = st.checkbox("中毒性帕金森综合征", 
                                                    value=st.session_state.patient_info.get('toxic_induced_parkinson', False),
                                                    key="toxic_induced_parkinson_checkbox")
                if toxic_induced_parkinson:
                    st.info("接触毒物：重金属（如锰、汞）或有机化合物（如MPTP）中毒，农药中毒如有机磷中毒，敌敌畏中毒，其他毒物如海洛因、河豚毒素、一氧化碳等。")
            
            with secondary_col4:
                none_secondary_history = st.checkbox("不符合", 
                                                   value=st.session_state.patient_info.get('none_secondary_history', False),
                                                   key="none_secondary_history_checkbox")
            
            # 体格检查部分
            st.subheader("3. 体格检查")
            
            # 体格检查详细描述
            physical_exam = st.text_area(
                "**体格检查详细描述**",
                value=st.session_state.patient_info.get('physical_exam', ''),
                height=120,
                placeholder="请输入详细的体格检查结果，\n优化:通过模型自动语意识别勾选相关体征"
            )
            
            # 体格检查勾选框 - 与排除标准联动
            st.write("**是否符合相关绝对排除标准（至少选择一项）**")
            exam_col1, exam_col2 = st.columns(2)
            
            with exam_col1:
                cerebellar_ataxia = st.checkbox("小脑性共济失调", 
                                            value=st.session_state.exclusion_criteria.get('cerebellar_ataxia', False),
                                            key="cerebellar_ataxia_checkbox")
                cerebellar_eye_movement = st.checkbox("小脑性眼动异常", 
                                                    value=st.session_state.exclusion_criteria.get('cerebellar_oculomotor', False),
                                                    key="cerebellar_eye_movement_checkbox")
                vertical_saccade_slowing = st.checkbox("向下的垂直性扫视选择性减慢", 
                                                    value=st.session_state.exclusion_criteria.get('vertical_saccade_slowing', False),
                                                    key="vertical_saccade_slowing_checkbox")
                orthostatic_hypotension = st.checkbox("体位性低血压", 
                                                    value=st.session_state.patient_info.get('orthostatic_hypotension', False),
                                                    key="orthostatic_hypotension_checkbox")
            
            with exam_col2:
                vertical_gaze_palsy = st.checkbox("向下的垂直性核上性凝视麻痹", 
                                                value=st.session_state.exclusion_criteria.get('vertical_gaze_palsy', False),
                                                key="vertical_gaze_palsy_checkbox")
                apraxia = st.checkbox("观念性运动性失用", 
                                    value=st.session_state.exclusion_criteria.get('ideomotor_apraxia', False),
                                    key="apraxia_checkbox")
                no_exam_symptoms = st.checkbox("不符合", 
                                            value=st.session_state.patient_info.get('no_exam_symptoms', False),
                                            key="no_exam_symptoms_checkbox")
            
            submitted = st.form_submit_button("保存患者信息", type="primary")
            
            if submitted:
                # 验证必填字段
                errors = []
                if not name.strip():
                    errors.append("患者姓名为必填项")
                if gender == "请选择":
                    errors.append("性别为必填项")
                if not allergy_history.strip():
                    errors.append("过敏史为必填项")
                if not chief_complaint.strip():
                    errors.append("主诉为必填项")
                if not medical_history.strip():
                    errors.append("病史信息为必填项")
                if not physical_exam.strip():
                    errors.append("体格检查为必填项")
                
                # 删除的症状勾选验证已移除
                
                # 验证继发性病史勾选
                secondary_selected = head_trauma or drug_induced_parkinson or toxic_induced_parkinson or none_secondary_history
                if not secondary_selected:
                    errors.append("请至少选择一项继发性帕金森综合征相关病史")
                
                # 验证体格检查勾选
                exam_selected = (cerebellar_ataxia or cerebellar_eye_movement or 
                            vertical_saccade_slowing or vertical_gaze_palsy or 
                            apraxia or orthostatic_hypotension or no_exam_symptoms)
                if not exam_selected:
                    errors.append("请至少选择一项体格检查体征")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # 计算当前年龄
                    current_age = calculate_age(birth_date)
                    
                    # 保存到session state - 患者信息
                    st.session_state.patient_info = {
                        'name': name,
                        'gender': gender,
                        'birth_date': birth_date,
                        'age': current_age,
                        'allergy_history': allergy_history,
                        'record_date': record_date,
                        'chief_complaint': chief_complaint,
                        # 删除的症状相关字段已移除
                        # 新增继发性帕金森综合征相关字段
                        'head_trauma': head_trauma,
                        'drug_induced_parkinson': drug_induced_parkinson,
                        'toxic_induced_parkinson': toxic_induced_parkinson,
                        'none_secondary_history': none_secondary_history,
                        'medical_history': medical_history,
                        'cerebellar_ataxia': cerebellar_ataxia,
                        'cerebellar_eye_movement': cerebellar_eye_movement,
                        'vertical_saccade_slowing': vertical_saccade_slowing,
                        'vertical_gaze_palsy': vertical_gaze_palsy,
                        'apraxia': apraxia,
                        'orthostatic_hypotension': orthostatic_hypotension,
                        'no_exam_symptoms': no_exam_symptoms,
                        'physical_exam': physical_exam
                    }
                    
                    # 同步到排除标准
                    st.session_state.exclusion_criteria.update({
                        'drug_induced': False,  # 设置为默认值
                        'progressive_aphasia': False,  # 设置为默认值
                        'cerebellar_ataxia': cerebellar_ataxia,
                        'cerebellar_oculomotor': cerebellar_eye_movement,
                        'vertical_saccade_slowing': vertical_saccade_slowing,
                        'vertical_gaze_palsy': vertical_gaze_palsy,
                        'ideomotor_apraxia': apraxia
                    })
                    
                    st.success("患者信息保存成功！绝对排除标准数据已同步到步骤3页面。")

    with col2:
        display_patient_info_summary()


if __name__ == "__main__":
    main()