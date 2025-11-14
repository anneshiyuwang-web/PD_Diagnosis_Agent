# deepseek_client.py
import requests
import json
import os

class DeepSeekClient:
    def __init__(self, api_key=None, base_url="https://api.deepseek.com/v1"):
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def call_deepseek(self, system_prompt, user_prompt, model="deepseek-chat", temperature=0.1):
        """
        调用DeepSeek API
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            model: 模型名称
            temperature: 温度参数
            
        Returns:
            dict: 包含API响应和解析后的数据
        """
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # 尝试解析JSON响应
                try:
                    parsed_content = json.loads(content)
                    return {
                        "success": True,
                        "raw_response": result,
                        "parsed_content": parsed_content,
                        "content": content
                    }
                except json.JSONDecodeError:
                    return {
                        "success": True,
                        "raw_response": result,
                        "parsed_content": {"response": content},
                        "content": content
                    }
            else:
                return {
                    "success": False,
                    "error": f"API调用失败: {response.status_code}",
                    "details": response.text
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"请求异常: {str(e)}"
            }

# 创建全局客户端实例
deepseek_client = DeepSeekClient()