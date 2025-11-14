# diagnosis_rules.py
from deepseek_client import deepseek_client
import pandas as pd

def assess_updrs_parkinson(updrs_data):
    """
    使用DeepSeek根据UPDRS评分判断帕金森综合症
    
    Args:
        updrs_data: DataFrame包含检测项目和评分
        
    Returns:
        dict: 评估结果
    """
    
    # 系统提示词
    system_prompt = """你是一个专业的神经科医生助手。请严格按照给定的判断步骤分析UPDRS-III评分数据，判断患者是否患有帕金森综合症。

请严格按照以下JSON格式返回评估结果：
{
    "has_parkinson": true/false,
    "core_standard_met": true/false,
    "rigidity_standard_met": true/false, 
    "tremor_standard_met": true/false,
    "core_items_met": ["检测项1", "检测项2"],
    "rigidity_score": 数字,
    "tremor_items_met": ["检测项1", "检测项2"],
    "assessment": "详细的UPDRSIII标准核对结果描述"
}

请严格按照用户提供的判断步骤进行分析，不要自行修改标准。"""

    # 构建用户提示词
    user_prompt = build_updrs_prompt(updrs_data)
    
    # 调用DeepSeek API
    result = deepseek_client.call_deepseek(system_prompt, user_prompt)
    
    if result["success"]:
        return result["parsed_content"]
    else:
        # API调用失败时使用规则回退
        return fallback_updrs_assessment(updrs_data)

def build_updrs_prompt(updrs_data):
    """构建UPDRS评估的用户提示词"""
    
    # 将DataFrame转换为易读的文本格式
    items_text = ""
    for _, row in updrs_data.iterrows():
        items_text += f"- {row['检测项目']}: 评分={row['评分']}\n"
    
    prompt = f"""请读取UPDRS III的检测项和对应评分。这些检测项是用来判断患者是否患有帕金森综合症的，判断步骤如下：

1. 首先，要判断【3.4 手指叩击（右）】、【3.5 手指叩击（左）】、【3.6 手掌握合（右）】、【3.7 手掌握合（左）】、【3.8 前臂旋前-旋后（右）】、【3.9 前臂旋前-旋后（左）】、【3.10 脚趾叩击（右）】、【3.11 脚趾叩击（左）】、【3.12 足跟点地（右）】、【3.13 足跟点地（左）】这10个检测项是否有至少1个检测项的评分大于等于2。如果满足条件，则说明病人具备"运动迟缓"这个"核心标准"。

2. 其次，判断【3.3 强直（颈+四肢）】检测项的评分是否大于等于2。如果满足条件，则说明病人具备"肌强直"的"辅助标准"。

3. 第三，判断【3.17 运动灵活性（手指-足快速轮替）】、【3.18 步态&冻结观察】这2个检测项是否至少有1个检测项的评分大于等于2。如果满足条件，则说明病人具备"姿势不稳"的"辅助标准"。

4. 如果满足"核心标准"及至少1项"辅助标准"，则可以初步判断病人属于帕金森综合症。否则，其他任何情况都表示病人不患有帕金森综合症。

当前患者的UPDRS-III评分数据：
{items_text}

请你根据上述的判断步骤，仿照给定的格式输出详细的UPDRSIII标准核对结果。"""
    
    return prompt

def fallback_updrs_assessment(updrs_data):
    """API失败时的回退规则评估"""
    
    # 将DataFrame转换为字典便于查询
    scores_dict = dict(zip(updrs_data['检测项目'], updrs_data['评分']))
    
    # 1. 核心标准判断 - 运动迟缓
    core_items = [
        "3.4 手指叩击（右）", "3.5 手指叩击（左）", "3.6 手掌握合（右）", 
        "3.7 手掌握合（左）", "3.8 前臂旋前-旋后（右）", "3.9 前臂旋前-旋后（左）",
        "3.10 脚趾叩击（右）", "3.11 脚趾叩击（左）", "3.12 足跟点地（右）", "3.13 足跟点地（左）"
    ]
    
    core_met_items = [item for item in core_items if scores_dict.get(item, 0) >= 2]
    core_standard_met = len(core_met_items) > 0
    
    # 2. 辅助标准1 - 肌强直
    rigidity_score = scores_dict.get("3.3 强直（颈+四肢）", 0)
    rigidity_standard_met = rigidity_score >= 2
    
    # 3. 辅助标准2 - 静止性震颤
    tremor_items = ["3.17 运动灵活性（手指-足快速轮替）", "3.18 步态&冻结观察"]
    tremor_met_items = [item for item in tremor_items if scores_dict.get(item, 0) >= 2]
    tremor_standard_met = len(tremor_met_items) > 0
    
    # 4. 最终判断
    has_parkinson = core_standard_met and (rigidity_standard_met or tremor_standard_met)
    
    # 构建评估描述
    assessment = build_assessment_text(
        core_standard_met, core_met_items,
        rigidity_standard_met, rigidity_score,
        tremor_standard_met, tremor_met_items,
        has_parkinson
    )
    
    return {
        "has_parkinson": has_parkinson,
        "core_standard_met": core_standard_met,
        "rigidity_standard_met": rigidity_standard_met,
        "tremor_standard_met": tremor_standard_met,
        "core_items_met": core_met_items,
        "rigidity_score": rigidity_score,
        "tremor_items_met": tremor_met_items,
        "assessment": assessment
    }

def build_assessment_text(core_met, core_items, rigidity_met, rigidity_score, tremor_met, tremor_items, has_parkinson):
    """构建评估结果文本"""
    
    # 1. 核心标准
    text = "**1. 核心标准——\"运动迟缓\"**\n"
    text += "需10项中至少1项的评分≥2。"
    if core_met:
        text += f"{'、'.join(core_items)}已满足，**患者具备\"运动迟缓\"症状。**\n\n"
    else:
        text += "10项的评分没有大于等于2的，**患者不具备\"运动迟缓\"症状。**\n\n"
    
    # 2. 肌强直标准
    text += "**2. 辅助标准——\"肌强直\"**\n"
    text += f"3.3 强直（颈+四肢）的评分={rigidity_score} "
    if rigidity_met:
        text += "≥2，**患者符合\"肌强直\"症状。**\n\n"
    else:
        text += "<2，**患者不符合\"肌强直\"症状。**\n\n"
    
    # 3. 静止性震颤标准
    text += "**3. 辅助标准——\"静止性震颤\"**\n"
    text += "3.17、3.18中至少1项的评分≥2。"
    if tremor_met:
        text += f"{'、'.join(tremor_items)}已满足，**患者符合\"静止性震颤\"症状。**\n\n"
    else:
        text += "两项评分均<2，**患者不符合\"静止性震颤\"症状。**\n\n"
    
    # 4. 综合评估
    text += "因此，综合评估患者"
    if has_parkinson:
        text += "**具有运动迟缓的主症**，"
        if rigidity_met and tremor_met:
            text += "和**肌强直、静止性震颤的2项辅症**。"
        elif rigidity_met:
            text += "和**肌强直的1项辅症**。"
        else:
            text += "和**静止性震颤的1项辅症**。"
        text += "**符合**UPDRS-III量表对帕金森综合症的初步诊断标准，判断患者**疑似帕金森综合症患者**，将进行后续辅助检查。"
    else:
        if core_met:
            text += "仅具有\"运动迟缓\"的主症，但缺少必要的辅助标准。"
        elif rigidity_met or tremor_met:
            text += "仅具有辅助标准症状，但缺少核心标准。"
        else:
            text += "未满足核心标准和辅助标准。"
        text += "**不符合**UPDRS-III量表对帕金森综合症的初步诊断标准，判断患者为**非帕金森综合症患者**，将移交至其他科室。"
    
    return text