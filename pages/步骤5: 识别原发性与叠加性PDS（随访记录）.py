# pages/5_原发型与叠加型辨别.py
import streamlit as st
import pandas as pd
import io
from components.patient_info_sidebar import display_patient_info_summary

def create_warning_signs_form():
    """创建警示征象评估表单"""
    st.subheader("1. 警示征象评估")
    
    # with st.expander("警示征象说明", expanded=True):
    #     st.markdown("""
    #     **评估是否存在以下警示征象（发病后时间均从首次出现运动症状开始计算）：**
    #     """)
    
    warning_signs = []
    
    # 警示征象1
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（1）发病后5年内出现快速进展的步态障碍，以至于需要经常使用轮椅**")
    with col2:
        sign1 = st.checkbox("存在征象1", key="sign1")
        if sign1:
            warning_signs.append(1)
    
    # 警示征象2
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（2）运动症状或体征在发病后5年内或5年以上完全不进展，除非这种病情的稳定是与治疗相关**")
    with col2:
        sign2 = st.checkbox("存在征象2", key="sign2")
        if sign2:
            warning_signs.append(2)
    
    # 警示征象3
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（3）发病后5年内出现球麻痹症状，表现为严重的发音困难、构音障碍或吞咽困难**")
    with col2:
        sign3 = st.checkbox("存在征象3", key="sign3")
        if sign3:
            warning_signs.append(3)
    
    # 警示征象4
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（4）发病后5年内出现吸气性呼吸功能障碍，即在白天或夜间出现吸气性喘鸣或者频繁的吸气性叹息**")
    with col2:
        sign4 = st.checkbox("存在征象4", key="sign4")
        if sign4:
            warning_signs.append(4)
    
    # 警示征象5
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（5）发病后5年内出现严重的自主神经功能障碍**")
    with col2:
        sign5 = st.checkbox("存在征象5", key="sign5")
        if sign5:
            warning_signs.append(5)
    
    # 警示征象6
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（6）发病后3年内由于平衡障碍导致反复(>1次/年)跌倒**")
    with col2:
        sign6 = st.checkbox("存在征象6", key="sign6")
        if sign6:
            warning_signs.append(6)
    
    # 警示征象7
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（7）发病后10年内出现不成比例的颈部前倾或手足挛缩**")
    with col2:
        sign7 = st.checkbox("存在征象7", key="sign7")
        if sign7:
            warning_signs.append(7)
    
    # 警示征象8
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（8）发病后5年内不出现任何一种常见的非运动症状**")
    with col2:
        sign8 = st.checkbox("存在征象8", key="sign8")
        if sign8:
            warning_signs.append(8)
    
    # 警示征象9
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（9）出现其他原因不能解释的锥体束征**")
    with col2:
        sign9 = st.checkbox("存在征象9", key="sign9")
        if sign9:
            warning_signs.append(9)
    
    # 警示征象10
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（10）起病或病程中表现为双侧对称性的帕金森综合征症状，没有任何侧别优势**")
    with col2:
        sign10 = st.checkbox("存在征象10", key="sign10")
        if sign10:
            warning_signs.append(10)
    
    return warning_signs

def create_supportive_criteria_form():
    """创建支持条件评估表单"""
    st.subheader("2. 支持条件评估")
    
    # with st.expander("📋 支持条件说明", expanded=True):
    #     st.markdown("""
    #     **评估是否存在以下支持条件：**
    #     """)
    
    supportive_criteria = []
    
    # 支持条件1
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（1）对多巴胺能药物的治疗明确且显著有效**")
    with col2:
        support1 = st.checkbox("存在条件1", key="support1")
        if support1:
            supportive_criteria.append(1)
    
    # 支持条件2
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（2）出现左旋多巴诱导的异动症**")
    with col2:
        support2 = st.checkbox("存在条件2", key="support2")
        if support2:
            supportive_criteria.append(2)
    
    # 支持条件3
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（3）临床体检观察到单个肢体的静止性震颤**")
    with col2:
        support3 = st.checkbox("存在条件3", key="support3")
        if support3:
            supportive_criteria.append(3)
    
    # 支持条件4
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("**（4）辅助检测阳性（嗅觉减退、黑质超声异常、心脏间碘苄胍闪烁显像异常）**")
    with col2:
        support4 = st.checkbox("存在条件4", key="support4")
        if support4:
            supportive_criteria.append(4)
    
    return supportive_criteria

def create_additional_tests_section():
    """创建辅助检查部分"""
    st.subheader("3. 辅助检查")
    
    # 膀胱残余尿检查
    st.write("**膀胱残余尿检查**")
    bladder_col1, bladder_col2 = st.columns([1, 2])
    with bladder_col1:
        bladder_file = st.file_uploader("上传膀胱残余尿检查报告", type=['jpg', 'jpeg', 'png', 'pdf'], key="bladder_uploader")
        if bladder_file is not None:
            st.success("文件上传成功")
    with bladder_col2:
        bladder_result = st.text_area("检查结果", placeholder="请输入膀胱残余尿检查结果...", key="bladder_result")
    
    # 肛门括约肌肌电图
    st.write("**肛门括约肌肌电图**")
    emg_col1, emg_col2 = st.columns([1, 2])
    with emg_col1:
        emg_file = st.file_uploader("上传肛门括约肌肌电图报告", type=['jpg', 'jpeg', 'png', 'pdf'], key="emg_uploader")
        if emg_file is not None:
            st.success("文件上传成功")
    with emg_col2:
        emg_result = st.text_area("检查结果", placeholder="请输入肛门括约肌肌电图结果...", key="emg_result")
    
    # 嗅觉检测
    st.write("**嗅觉检测**")
    smell_col1, smell_col2 = st.columns([1, 2])
    with smell_col1:
        smell_file = st.file_uploader("上传嗅觉检测报告", type=['jpg', 'jpeg', 'png', 'pdf'], key="smell_uploader")
        if smell_file is not None:
            st.success("文件上传成功")
    with smell_col2:
        smell_result = st.text_area("检查结果", placeholder="请输入嗅觉检测结果...", key="smell_result")
    
    # 黑质超声
    st.write("**黑质超声**")
    ultrasound_col1, ultrasound_col2 = st.columns([1, 2])
    with ultrasound_col1:
        ultrasound_file = st.file_uploader("上传黑质超声报告", type=['jpg', 'jpeg', 'png', 'pdf'], key="ultrasound_uploader")
        if ultrasound_file is not None:
            st.success("文件上传成功")
    with ultrasound_col2:
        ultrasound_result = st.text_area("检查结果", placeholder="请输入黑质超声结果...", key="ultrasound_result")
    
    return {
        'bladder': {'file': bladder_file, 'result': bladder_result},
        'emg': {'file': emg_file, 'result': emg_result},
        'smell': {'file': smell_file, 'result': smell_result},
        'ultrasound': {'file': ultrasound_file, 'result': ultrasound_result}
    }

def create_imaging_section():
    """创建影像学检查部分"""
    st.subheader("4. 影像学检查")
    
    st.write("**结构磁共振成像**")
    st.info("请上传包含以下序列的MRI图像：3D T1、T2 TSE、DWI、3D Flair、SWI、DTI")
    
    mri_col1, mri_col2 = st.columns([1, 2])
    with mri_col1:
        mri_files = st.file_uploader("上传MRI图像", type=['jpg', 'jpeg', 'png', 'dcm'], 
                                   accept_multiple_files=True, key="mri_uploader")
        if mri_files:
            st.success(f"已上传 {len(mri_files)} 个文件")
            for file in mri_files[:3]:  # 显示前3个文件的预览
                st.image(file, caption=file.name, width=150)
    with mri_col2:
        mri_conclusion = st.text_area("MRI检查结论", 
                                    placeholder="请输入MRI影像学结论，特别注意以下特征：\n- 壳核、脑桥、小脑中脚和小脑萎缩\n- 壳核信号降低\n- 脑桥十字形高信号（十字征）\n- 中脑萎缩（蜂鸟征）\n- MRPI指数",
                                    height=150,
                                    key="mri_conclusion")
    
    # MSA特异性影像学特征
    st.write("**MSA特异性影像学特征**")
    msa_features = []
    col1, col2, col3 = st.columns(3)
    with col1:
        putamen_atrophy = st.checkbox("壳核萎缩")
        if putamen_atrophy:
            msa_features.append("壳核萎缩")
    with col2:
        pontine_cross = st.checkbox("脑桥十字征")
        if pontine_cross:
            msa_features.append("脑桥十字征")
    with col3:
        middle_cerebellar = st.checkbox("小脑中脚异常")
        if middle_cerebellar:
            msa_features.append("小脑中脚异常")
    
    # PSP特异性影像学特征
    st.write("**PSP特异性影像学特征**")
    psp_features = []
    col1, col2 = st.columns(2)
    with col1:
        hummingbird_sign = st.checkbox("蜂鸟征")
        if hummingbird_sign:
            psp_features.append("蜂鸟征")
    with col2:
        mrpi_index = st.number_input("MRPI指数", min_value=0.0, value=0.0, step=0.1)
        if mrpi_index > 13.55:
            psp_features.append(f"MRPI指数异常({mrpi_index})")
    
    return {
        'mri_files': mri_files,
        'mri_conclusion': mri_conclusion,
        'msa_features': msa_features,
        'psp_features': psp_features,
        'mrpi_index': mrpi_index
    }

def perform_diagnosis(warning_signs, supportive_criteria, msa_features, psp_features, mrpi_index):
    """执行诊断逻辑"""
    st.subheader("诊断结果")
    
    num_warning_signs = len(warning_signs)
    num_supportive_criteria = len(supportive_criteria)
    
    # 诊断逻辑
    if num_warning_signs == 0:
        st.success("🟢 **原发性帕金森综合征**")
        st.info("未发现警示征象，符合原发性帕金森病诊断")
        return "原发性帕金森病"
    
    elif num_warning_signs == 1:
        if num_supportive_criteria >= 1:
            st.success("🟢 **原发性帕金森综合征**")
            st.info("1条警示征象被1条支持条件抵消")
            return "原发性帕金森病"
        else:
            st.error("🔴 **叠加性帕金森综合征**")
            st.info("1条警示征象未被支持条件抵消")
            return "帕金森叠加综合征"
    
    elif num_warning_signs == 2:
        if num_supportive_criteria >= 2:
            st.success("🟢 **原发性帕金森综合征**")
            st.info("2条警示征象被2条支持条件抵消")
            return "原发性帕金森病"
        else:
            st.error("🔴 **叠加性帕金森综合征**")
            st.info("2条警示征象未被足够支持条件抵消")
            return "帕金森叠加综合征"
    
    else:  # num_warning_signs >= 3
        st.error("🔴 **叠加性帕金森综合征**")
        st.info("3条或以上警示征象，诊断不能成立")
        
        # 进一步区分叠加综合征类型
        if any(sign in [1, 3, 4, 5, 7, 9] for sign in warning_signs) or msa_features:
            st.warning("⚠️ **高度怀疑多系统萎缩（MSA）**")
            if msa_features:
                st.write(f"**MSA影像学特征：** {', '.join(msa_features)}")
        
        if any(sign in [1, 3, 6] for sign in warning_signs) or psp_features:
            st.warning("⚠️ **高度怀疑进行性核上性麻痹（PSP）**")
            if psp_features:
                st.write(f"**PSP影像学特征：** {', '.join(psp_features)}")
            if mrpi_index > 13.55:
                st.write(f"**MRPI指数：** {mrpi_index} (异常)")
        
        return "帕金森叠加综合征"

def main():
    # 显示侧边栏
    from components.current_patient_sidebar import display_current_patient_sidebar
    display_current_patient_sidebar()
    
    st.header("原发型与叠加型帕金森综合征辨别")
    
    # 检查患者信息是否已录入
    if not st.session_state.patient_info['name']:
        st.warning("请先在'患者基本信息录入'页面填写患者信息")
        return
    
    # 初始化session state
    if 'page5_warning_signs' not in st.session_state:
        st.session_state.page5_warning_signs = []
    if 'page5_supportive_criteria' not in st.session_state:
        st.session_state.page5_supportive_criteria = []
    if 'page5_diagnosis_result' not in st.session_state:
        st.session_state.page5_diagnosis_result = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 显示诊断流程说明
        with st.expander("诊断规则", expanded=True):
            st.markdown("""
            - 0条警示征象 → 原发性帕金森病
            - 1条警示征象 → 需要至少1条支持条件抵消
            - 2条警示征象 → 需要至少2条支持条件抵消  
            - ≥3条警示征象 → 帕金森叠加综合征
            """)
        
        # 1. 警示征象评估
        warning_signs = create_warning_signs_form()
        st.session_state.page5_warning_signs = warning_signs
        
        # 2. 支持条件评估
        supportive_criteria = create_supportive_criteria_form()
        st.session_state.page5_supportive_criteria = supportive_criteria
        
        # 如果存在警示征象，显示辅助检查和影像学检查
        if warning_signs:
            st.info("🔍 **检测到警示征象，建议进行以下检查：**")
            
            # 3. 辅助检查
            additional_tests = create_additional_tests_section()
            
            # 4. 影像学检查
            imaging_data = create_imaging_section()
            
            # 诊断按钮
            if st.button("进行综合诊断", type="primary", use_container_width=True):
                diagnosis_result = perform_diagnosis(
                    warning_signs, 
                    supportive_criteria,
                    imaging_data['msa_features'],
                    imaging_data['psp_features'],
                    imaging_data['mrpi_index']
                )
                st.session_state.page5_diagnosis_result = diagnosis_result
                
                # 更新诊断标签
                if diagnosis_result == "原发性帕金森病":
                    st.session_state.patient_info['diagnosis_tag'] = '原发性帕金森综合征'
                else:
                    st.session_state.patient_info['diagnosis_tag'] = '叠加性帕金森综合征'
        
        else:
            # 如果没有警示征象，可以直接诊断
            if st.button("进行诊断", type="primary", use_container_width=True):
                diagnosis_result = perform_diagnosis([], supportive_criteria, [], [], 0)
                st.session_state.page5_diagnosis_result = diagnosis_result
                st.session_state.patient_info['diagnosis_tag'] = '原发性帕金森综合征'
    
    with col2:
        display_patient_info_summary()

if __name__ == "__main__":
    main()