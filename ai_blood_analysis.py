# ai_blood_analysis.py
import pandas as pd
import json

class BloodTestAnalyzer:
    def __init__(self, deepseek_client=None):
        self.deepseek_client = deepseek_client
    
    def analyze_blood_tests(self, lab_data):
        """
        分析血检数据，判断是否为继发性帕金森综合征
        """
        # 如果有DeepSeek客户端，使用AI分析，否则使用规则分析
        if self.deepseek_client:
            return self._analyze_with_ai(lab_data)
        else:
            return self._analyze_with_rules(lab_data)
    
    def _analyze_with_ai(self, lab_data):
        """
        使用DeepSeek API分析血检数据
        """
        system_prompt = """你是一个专业的神经科医生助手。请根据患者的血检数据分析是否存在继发性帕金森综合征的病因。
        
请严格按照以下JSON格式返回分析结果：
{
    "diagnosis_type": "疑似帕金森综合征/继发性帕金森综合征",
    "diagnosis_label": "具体的诊断标签",
    "abnormal_items": ["异常项目1", "异常项目2"],
    "reasoning": "详细的分析推理过程",
    "suggested_conditions": ["梅毒", "HIV", "电解质紊乱", "甲状腺功能亢进", "甲状旁腺功能异常", "肝豆状核变性", "无"]
}

分析逻辑：
1. 如果梅毒抗体或HIV抗体为阳性，诊断为感染性帕金森综合征（继发性）
2. 如果存在电解质紊乱（低钠血症快速纠正）、甲状腺功能亢进、甲状旁腺功能异常、肝豆状核变性（需进一步完善肝肾功能、电解质、甲状腺功能、甲状旁腺激素等检查），诊断为内分泌或代谢所致的帕金森综合征（继发性）
3. 如果以上均无异常，诊断为疑似帕金森综合征

注意：suggested_conditions字段要返回所有相关的条件，包括"无"选项。"""

        # 构建用户提示词
        user_prompt = f"""请分析以下血检数据：

{lab_data.to_string()}

请根据分析逻辑判断患者是否为继发性帕金森综合征，并返回指定的JSON格式结果。"""

        # 调用DeepSeek API
        result = self.deepseek_client.call_deepseek(system_prompt, user_prompt)
        
        if result["success"]:
            return result["parsed_content"]
        else:
            # API调用失败时回退到规则分析
            return self._analyze_with_rules(lab_data)
    
    def _analyze_with_rules(self, lab_data):
        """
        基于规则的血液分析（DeepSeek API不可用时的回退方案）
        """
        # 从lab_data中提取关键信息
        lab_dict = {}
        for _, row in lab_data.iterrows():
            lab_dict[row['名称']] = row['结果']
        
        abnormal_items = []
        suggested_conditions = []
        
        # 检查梅毒和HIV
        if '梅毒抗体' in lab_dict and lab_dict['梅毒抗体'] == '阳性':
            abnormal_items.append("梅毒抗体阳性")
            suggested_conditions.append("梅毒")
        
        if 'HIV抗体' in lab_dict and lab_dict['HIV抗体'] == '阳性':
            abnormal_items.append("HIV抗体阳性")
            suggested_conditions.append("HIV")
        
        # 检查电解质
        electrolyte_abnormal = False
        if '钠(Na)' in lab_dict and lab_dict['钠(Na)']:
            try:
                na_value = float(lab_dict['钠(Na)'])
                if na_value < 135:
                    abnormal_items.append("低钠血症")
                    electrolyte_abnormal = True
            except:
                pass
        
        # 检查甲状腺功能
        thyroid_abnormal = False
        if '游离T3(FT3)' in lab_dict and lab_dict['游离T3(FT3)']:
            try:
                ft3_value = float(lab_dict['游离T3(FT3)'])
                if ft3_value > 6.5:
                    abnormal_items.append("甲状腺功能亢进(FT3升高)")
                    thyroid_abnormal = True
            except:
                pass
        
        # 检查甲状旁腺功能
        parathyroid_abnormal = False
        if '甲状旁腺激素(PTH)' in lab_dict and lab_dict['甲状旁腺激素(PTH)']:
            try:
                pth_value = float(lab_dict['甲状旁腺激素(PTH)'])
                if pth_value > 65 or pth_value < 15:
                    abnormal_items.append("甲状旁腺功能异常")
                    parathyroid_abnormal = True
            except:
                pass
        
        # 检查肝功能（肝豆状核变性相关）
        liver_abnormal = False
        if any(key in lab_dict for key in ['谷丙转氨酶(ALT)', '谷草转氨酶(AST)', '总胆红素(TBIL)']):
            alt_abnormal = '谷丙转氨酶(ALT)' in lab_dict and lab_dict['谷丙转氨酶(ALT)'] and float(lab_dict['谷丙转氨酶(ALT)']) > 40
            ast_abnormal = '谷草转氨酶(AST)' in lab_dict and lab_dict['谷草转氨酶(AST)'] and float(lab_dict['谷草转氨酶(AST)']) > 40
            tbil_abnormal = '总胆红素(TBIL)' in lab_dict and lab_dict['总胆红素(TBIL)'] and float(lab_dict['总胆红素(TBIL)']) > 20.5
            
            if alt_abnormal or ast_abnormal or tbil_abnormal:
                abnormal_items.append("肝功能异常")
                liver_abnormal = True
        
        # 根据异常情况确定诊断
        if "梅毒抗体阳性" in abnormal_items or "HIV抗体阳性" in abnormal_items:
            diagnosis_type = "继发性帕金森综合征"
            diagnosis_label = "感染性帕金森综合征"
        elif electrolyte_abnormal or thyroid_abnormal or parathyroid_abnormal or liver_abnormal:
            diagnosis_type = "继发性帕金森综合征"
            diagnosis_label = "内分泌或代谢所致的帕金森综合征"
            
            if electrolyte_abnormal:
                suggested_conditions.append("电解质紊乱")
            if thyroid_abnormal:
                suggested_conditions.append("甲状腺功能亢进")
            if parathyroid_abnormal:
                suggested_conditions.append("甲状旁腺功能异常")
            if liver_abnormal:
                suggested_conditions.append("肝豆状核变性")
        else:
            diagnosis_type = "疑似帕金森综合征"
            diagnosis_label = "疑似帕金森综合征"
            suggested_conditions.append("无")
        
        # 确保有"无"选项
        if not suggested_conditions:
            suggested_conditions.append("无")
        
        reasoning = self._build_reasoning_text(abnormal_items, diagnosis_type, diagnosis_label)
        
        return {
            "diagnosis_type": diagnosis_type,
            "diagnosis_label": diagnosis_label,
            "abnormal_items": abnormal_items,
            "reasoning": reasoning,
            "suggested_conditions": suggested_conditions
        }
    
    def _build_reasoning_text(self, abnormal_items, diagnosis_type, diagnosis_label):
        """构建分析推理文本"""
        if not abnormal_items:
            return "所有血检项目均在正常范围内，未发现可能导致继发性帕金森综合征的异常指标。结论为疑似帕金森综合征，需配合其他辅助检测项进一步确认。"
        
        items_text = "、".join(abnormal_items)
        
        if diagnosis_type == "继发性帕金森综合征":
            return f"发现以下异常指标：{items_text}。这些指标异常提示存在可能导致继发性帕金森综合征的病因，诊断为{diagnosis_label}。"
        else:
            return f"发现以下轻微异常指标：{items_text}，但这些异常不足以诊断为继发性帕金森综合征。"

# 创建全局分析器实例
blood_analyzer = BloodTestAnalyzer()