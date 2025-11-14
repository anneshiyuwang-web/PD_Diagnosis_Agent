# components/current_patient_sidebar.py
import streamlit as st

def display_current_patient_sidebar():
    """显示当前患者信息的侧边栏组件"""
    
    # 确保诊断标签存在
    if 'diagnosis_tag' not in st.session_state.patient_info:
        st.session_state.patient_info['diagnosis_tag'] = '疑似帕金森综合征'
    
    # 检查是否需要根据所有页面的状态更新诊断标签
    check_and_update_diagnosis_from_all_pages()
    
    # 显示当前患者信息
    if st.session_state.patient_info.get('name'):
        st.sidebar.markdown("---")
        st.sidebar.subheader("当前患者")
        st.sidebar.write(f"**姓名:** {st.session_state.patient_info['name']}")
        st.sidebar.write(f"**性别:** {st.session_state.patient_info['gender']}")
        
        # 显示诊断标签
        diagnosis_tag = st.session_state.patient_info.get('diagnosis_tag', '疑似帕金森综合征')
        
        # 根据诊断标签设置不同的颜色和图标
        tag_config = {
            '原发性帕金森综合征': {'color': 'green', 'icon': '🟢'},
            '疑似帕金森综合征': {'color': 'orange', 'icon': '🟡'},
            '非原发性帕金森综合征': {'color': 'blue', 'icon': '🔵'},
            '继发性帕金森综合征': {'color': 'red', 'icon': '🔴'},
            '叠加性帕金森综合征': {'color': 'purple', 'icon': '🟣'}
        }
        
        config = tag_config.get(diagnosis_tag, {'color': 'orange', 'icon': '🟡'})
        
        st.sidebar.markdown(f"**诊断标签:** {config['icon']} {diagnosis_tag}")
        
        # 显示诊断进度（如果其他页面有相关信息）
        if hasattr(st.session_state, 'diagnosis_progress'):
            st.sidebar.markdown("---")
            st.sidebar.subheader("诊断进度")
            progress = st.session_state.diagnosis_progress
            st.sidebar.progress(progress)
            
    else:
        st.sidebar.markdown("---")
        st.sidebar.subheader("当前患者")
        st.sidebar.info("尚未录入患者信息")
        st.sidebar.write("请先在'患者基本信息录入'页面填写患者信息")
    
    # 在侧边栏底部添加诊断标签图例
    display_diagnosis_legend()

def check_and_update_diagnosis_from_all_pages():
    """根据所有页面的状态检查并更新诊断标签"""
    # 首先检查步骤5的结果（最高优先级）
    page5_result = get_page5_final_result_for_sidebar()
    if page5_result:
        if page5_result == "原发性帕金森病":
            st.session_state.patient_info['diagnosis_tag'] = '原发性帕金森综合征'
            return
        else:
            st.session_state.patient_info['diagnosis_tag'] = '叠加性帕金森综合征'
            return
    
    # 如果没有步骤5结果，检查步骤4的结果
    page4_result = get_page4_final_result_for_sidebar()
    if page4_result:
        if page4_result == "继发性帕金森综合征":
            st.session_state.patient_info['diagnosis_tag'] = '继发性帕金森综合征'
        elif page4_result == "疑似帕金森综合征":
            # 只有当当前标签不是继发性时才更新为疑似
            current_tag = st.session_state.patient_info.get('diagnosis_tag', '疑似帕金森综合征')
            if current_tag != '继发性帕金森综合征':
                st.session_state.patient_info['diagnosis_tag'] = '疑似帕金森综合征'

def get_page4_final_result_for_sidebar():
    """获取page4的最终结果（用于侧边栏）"""
    # 检查血检是否完成
    blood_completed = (hasattr(st.session_state, 'ai_analysis_result') and 
                      st.session_state.ai_analysis_result is not None and
                      hasattr(st.session_state, 'selected_conditions') and
                      st.session_state.selected_conditions)
    
    # 检查CT是否完成
    ct_completed = (hasattr(st.session_state, 'ct_data') and 
                   st.session_state.ct_data['findings'])
    
    # 检查MRI是否完成
    mri_completed = (hasattr(st.session_state, 'mri_data') and 
                    st.session_state.mri_data['findings'])
    
    # 如果任何一项检查未完成，返回None
    if not (blood_completed and ct_completed and mri_completed):
        return None
    
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

def get_page5_final_result_for_sidebar():
    """获取page5的最终结果（用于侧边栏）"""
    if hasattr(st.session_state, 'page5_diagnosis_result') and st.session_state.page5_diagnosis_result is not None:
        return st.session_state.page5_diagnosis_result
    return None

def update_diagnosis_tag(new_tag):
    """更新诊断标签的函数，供其他页面调用"""
    valid_tags = [
        '原发性帕金森综合征',
        '疑似帕金森综合征', 
        '非原发性帕金森综合征',
        '继发性帕金森综合征',
        '叠加性帕金森综合征'
    ]
    
    if new_tag in valid_tags:
        st.session_state.patient_info['diagnosis_tag'] = new_tag
        return True
    else:
        st.error(f"无效的诊断标签: {new_tag}")
        return False

def get_current_diagnosis_tag():
    """获取当前诊断标签"""
    return st.session_state.patient_info.get('diagnosis_tag', '疑似帕金森综合征')

def display_diagnosis_legend():
    """显示诊断标签图例"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("诊断标签总览")
    
    # 诊断标签配置
    tag_config = {
        '原发性帕金森综合征': {'color': 'green', 'icon': '🟢'},
        '疑似帕金森综合征': {'color': 'orange', 'icon': '🟡'},
        '非原发性帕金森综合征': {'color': 'blue', 'icon': '🔵'},
        '继发性帕金森综合征': {'color': 'red', 'icon': '🔴'},
        '叠加性帕金森综合征': {'color': 'purple', 'icon': '🟣'}
    }
    
    # 显示所有标签，紧凑排列
    current_tag = get_current_diagnosis_tag()
    
    for tag, config in tag_config.items():
        is_current = tag == current_tag
        current_indicator = " **← 当前**" if is_current else ""
        
        st.sidebar.markdown(f"{config['icon']} {tag}{current_indicator}")