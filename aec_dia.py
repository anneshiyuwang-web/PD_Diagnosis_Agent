# aec_dia.py
from deepseek_client import deepseek_client

def assess_absolute_exclusion_criteria(exclusion_data):
    """
    使用DeepSeek根据绝对排除标准判断是否为原发性帕金森综合症
    
    Args:
        exclusion_data: 字典包含绝对排除标准的各项判断结果
        
    Returns:
        dict: 评估结果
    """
    
    # 系统提示词
    system_prompt = """你是一个专业的神经科医生助手。请严格按照给定的判断步骤分析绝对排除标准数据，判断患者是否患有原发性帕金森综合症。

请严格按照以下JSON格式返回评估结果：
{
    "is_primary_parkinson": true/false,
    "total_criteria": 数字,
    "positive_criteria_count": 数字,
    "positive_criteria_details": ["阳性标准1", "阳性标准2"],
    "assessment": "详细的绝对排除标准核对结果描述"
}

判断规则：只要有任意一条判断项的结论为"是"，则说明该患者不是原发型帕金森综合症，而是继发性帕金森综合症或叠加型帕金森综合症。"""

    # 构建用户提示词
    user_prompt = build_exclusion_prompt(exclusion_data)
    
    # 调用DeepSeek API
    result = deepseek_client.call_deepseek(system_prompt, user_prompt)
    
    if result["success"]:
        return result["parsed_content"]
    else:
        # API调用失败时使用规则回退
        return fallback_exclusion_assessment(exclusion_data)

def build_exclusion_prompt(exclusion_data):
    """构建绝对排除标准评估的用户提示词"""
    
    # 构建标准描述文本
    criteria_text = ""
    criteria_count = 0
    
    # 标准1: 多巴胺受体阻滞剂或多巴胺耗竭剂服用史
    if 'drug_induced' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 多巴胺受体阻滞剂或多巴胺耗竭剂服用史: {'是' if exclusion_data['drug_induced'] else '否'}\n"
        criteria_text += "   - 判断: 多巴胺受体阻滞剂或多巴胺耗竭剂治疗诱导的帕金森综合征，其剂量和时程与药物性帕金森综合征相一致\n\n"
    
    # 标准2: 进行性失语
    if 'progressive_aphasia' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 进行性失语: {'是' if exclusion_data['progressive_aphasia'] else '否'}\n"
        criteria_text += "   - 判断: 存在明确的进行性失语\n\n"
    
    # 标准3: 小脑性共济失调
    if 'cerebellar_ataxia' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 小脑性共济失调: {'是' if exclusion_data['cerebellar_ataxia'] else '否'}\n"
        criteria_text += "   - 判断: 存在明确的小脑性共济失调\n\n"
    
    # 标准4: 小脑性眼动异常
    if 'cerebellar_oculomotor' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 小脑性眼动异常: {'是' if exclusion_data['cerebellar_oculomotor'] else '否'}\n"
        criteria_text += "   - 判断: 小脑性眼动异常(持续的凝视诱发的眼震、巨大方波跳动、超节律扫视)\n\n"
    
    # 标准5: 向下的垂直性扫视选择性减慢
    if 'vertical_saccade_slowing' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 向下的垂直性扫视选择性减慢: {'是' if exclusion_data['vertical_saccade_slowing'] else '否'}\n"
        criteria_text += "   - 判断: 向下的垂直性扫视选择性减慢\n\n"
    
    # 标准6: 向下的垂直性核上性凝视麻痹
    if 'vertical_gaze_palsy' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 向下的垂直性核上性凝视麻痹: {'是' if exclusion_data['vertical_gaze_palsy'] else '否'}\n"
        criteria_text += "   - 判断: 出现向下的垂直性核上性凝视麻痹\n\n"
    
    # 标准7: 观念性运动性失用
    if 'ideomotor_apraxia' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 观念性运动性失用: {'是' if exclusion_data['ideomotor_apraxia'] else '否'}\n"
        criteria_text += "   - 判断: 存在明确的肢体观念运动性失用\n\n"
    
    # 标准8: 发病后5年内诊断FTD或PPA
    if 'ftd_ppa' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 发病后5年内诊断FTD或PPA: {'是' if exclusion_data['ftd_ppa'] else '否'}\n"
        criteria_text += "   - 判断: 在发病后5年内，患者被诊断为高度怀疑的行为变异型额颞叶痴呆或原发性进行性失语\n\n"
    
    # 标准9: 发病3年后仍局限于下肢的帕金森样症状
    if 'lower_limb_parkinsonism' in exclusion_data:
        criteria_count += 1
        criteria_text += f"{criteria_count}. 发病3年后仍局限于下肢的帕金森样症状: {'是' if exclusion_data['lower_limb_parkinsonism'] else '否'}\n"
        criteria_text += "   - 判断: 发病3年后仍局限于下肢的帕金森样症状\n\n"

    prompt = f"""请读取绝对排除标准的判断项和对应结果。这些判断项是用来判断患者是否患有原发型帕金森综合症的，判断规则如下：只要有任意一条判断项的结论为"是"，则说明该患者不是原发型帕金森综合症，而是继发性帕金森综合症或叠加型帕金森综合症。

当前患者的绝对排除标准评估数据：
{criteria_text}

请你根据上述的判断规则，仿照如下格式输出详细的绝对排除标准核对结果：

如果所有标准都为"否"：
## 步骤二：评估绝对排除标准
### 绝对排除标准核对结果：
核对了总共{criteria_count}条绝对排除的判断项，结论都为"否"。该患者疑似原发性帕金森综合症，因此继续根据《继发性病因清单》分辨患者是否为继发性帕金森综合症。

如果有任意标准为"是"：
## 步骤二：评估绝对排除标准
### 绝对排除标准核对结果：
核对了总共{criteria_count}条绝对排除的判断项，发现了[具体的阳性标准描述]，即相关判断项的结论为"是"。判断患者非原发性帕金森综合症，将移交至其他科室。"""
    
    return prompt

def fallback_exclusion_assessment(exclusion_data):
    """API失败时的回退规则评估"""
    
    # 检查是否有任何排除标准被选中
    positive_criteria = []
    
    criteria_mapping = {
        'drug_induced': '多巴胺受体阻滞剂或多巴胺耗竭剂服用史',
        'progressive_aphasia': '进行性失语',
        'cerebellar_ataxia': '小脑性共济失调',
        'cerebellar_oculomotor': '小脑性眼动异常',
        'vertical_saccade_slowing': '向下的垂直性扫视选择性减慢',
        'vertical_gaze_palsy': '向下的垂直性核上性凝视麻痹',
        'ideomotor_apraxia': '观念性运动性失用',
        'ftd_ppa': '发病后5年内诊断FTD或PPA',
        'lower_limb_parkinsonism': '发病3年后仍局限于下肢的帕金森样症状'
    }
    
    for key, description in criteria_mapping.items():
        if exclusion_data.get(key, False):
            positive_criteria.append(description)
    
    total_criteria = len([key for key in criteria_mapping.keys() if key in exclusion_data])
    positive_count = len(positive_criteria)
    is_primary_parkinson = positive_count == 0
    
    # 构建评估描述
    assessment = build_exclusion_assessment_text(total_criteria, positive_count, positive_criteria, is_primary_parkinson)
    
    return {
        "is_primary_parkinson": is_primary_parkinson,
        "total_criteria": total_criteria,
        "positive_criteria_count": positive_count,
        "positive_criteria_details": positive_criteria,
        "assessment": assessment
    }

def build_exclusion_assessment_text(total_criteria, positive_count, positive_criteria, is_primary_parkinson):
    """构建绝对排除标准评估结果文本"""
    
    if is_primary_parkinson:
        assessment = f"核对了总共{total_criteria}条绝对排除的判断项，结论都为\"否\"。该患者疑似原发性帕金森综合症，因此继续根据《继发性病因清单》分辨患者是否为继发性帕金森综合症。"
    else:
        assessment = f"核对了总共{total_criteria}条绝对排除的判断项，"
        
        if positive_count == 1:
            assessment += f"发现了患者出现{positive_criteria[0]}的症状，"
        else:
            assessment += f"发现了患者出现{', '.join(positive_criteria[:-1])}和{positive_criteria[-1]}的症状，"
        
        assessment += "即相关判断项的结论为\"是\"。判断患者非原发性帕金森综合症，将移交至其他科室。"
    
    return assessment