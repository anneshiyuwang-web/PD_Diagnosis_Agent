# main.py
import streamlit as st
from components.current_patient_sidebar import display_current_patient_sidebar

# 设置页面配置
st.set_page_config(
    page_title="帕金森病诊断系统",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
def initialize_session_state():
    if 'patient_info' not in st.session_state:
        st.session_state.patient_info = {
            'name': '',
            'gender': '',
            'medical_history': '',
            'birth_date': None,
            'diagnosis_tag': '疑似原发性帕金森综合征'  # 添加诊断标签
        }
    
    if 'exclusion_criteria' not in st.session_state:
        st.session_state.exclusion_criteria = {
            'cerebellar_ataxia': False,
            'vertical_gaze_palsy': False,
            'ftd_ppa': False,
            'lower_limb_parkinsonism': False,
            'drug_induced': False,
            'cortical_sensory_loss': False
        }

def main():
    # 初始化会话状态
    initialize_session_state()
    
    # 使用组件显示当前患者信息
    display_current_patient_sidebar()
    
    # 主页面内容
    st.title("帕金森病诊断系统")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("PD临床诊断SOP")
        st.markdown("""
        **1. 患者基本信息录入**
        - 记录患者个人资料和病史
        
        **2. 帕金森症候群诊断**
        - UPDRS量表数据上传和分析
        
        **3. 绝对排除标准检查**
        - 通过绝对排除标准系统化排除非典型帕金森综合征
        
        **4. 原发型与继发型辨别**
        - 鉴别特发性与继发性帕金森病
        - 病因分析和治疗建议
        
        **5. 原发型与叠加型辨别**
        - 识别帕金森叠加综合征
        - 多系统萎缩、PSP、CBD等鉴别
        """)
    
    with col2:
        st.header("诊断系统说明")
        st.markdown("""
        **1. 初诊患者诊断（手动录入患者数据试用）**
        - 诊断过程分析
        - 直接判断或转入随访流程

        **2. 随访患者诊断（未完成，待接入随访数据库系统）**
        - 对接随访数据库数据做最终诊断
        
        **3. 随访数据更新（未完成，待接入随访数据库系统）**
        - 已有随访数据录入（转院病人/过往数据）
        - 新的随访数据录入
        
        **4. 患者标签（未完成，待完善）**
        - 原发性PDS
        - 继发性PDS
        
          (1) 药物性帕金森综合征
          
          (2) 中毒性帕金森综合征
          
          (3) 血管性帕金森综合征
          
          (4) 感染性帕金森综合征
          
          (5) 头部外伤史
          
          (6) 正常压力性脑积水
          
          (7) 内分泌或代谢
        - 叠加性PDS
                
          (1) 多系统萎缩（MSA-P型：帕金森优势型；MSA-C型：小脑优势型）
          
          (2) 进行性核上性麻痹（PSP，经典型+变异型）
          
          (3) 皮质基底节变性（CBD，CBS：皮质基底节综合征）
          
          (4) 路易体痴呆（DLB）
          
          (5) 额颞叶痴呆伴帕金森综合征（FTD-P）
          
          (6) 阿尔茨海默病伴帕金森征（AD-P，扩展亚型）
          
          (7) 脊髓小脑性共济失调伴帕金森征（SCA-P，扩展亚型）
        - 非PDS
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <small>帕金森病诊断系统 | 仅供医疗专业人员使用</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
