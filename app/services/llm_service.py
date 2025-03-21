import datetime
import json
import os

from typing import Optional, Dict, Any
from app.models.llm_dao import LlmDAO
from app.database.db import get_db
from app.utils.logger import get_logger, info, error
from openai import OpenAI
from app.config.settings import settings

logger = get_logger(__name__)

class LlmService:
    """LLM服务类"""
    
    @staticmethod
    def store_note_diagnosis(note_id: str, llm_alias: str, diagnosis_data: Dict[str, Any]) -> bool:
        """
        存储笔记诊断结果
        
        Args:
            note_id: 笔记ID
            llm_alias: 模型名称
            diagnosis_data: 诊断数据
            
        Returns:
            bool: 是否成功
        """
        try:
            db = next(get_db())
            
            # 存储诊断结果
            diagnosis = LlmDAO.store_note_diagnosis(
                db=db,
                note_id=note_id,
                llm_name=llm_alias,
                diagnosis_data=diagnosis_data
            )
            
            return diagnosis is not None
            
        except Exception as e:
            error(f"存储笔记诊断结果时出错: {str(e)}")
            return False
        
    @staticmethod
    def request_llm(llm_alias: str, prompt: str, log_file_prefix: str):
        """
        请求LLM
        """
        if (llm_alias == "qwen-max:coze"):
            # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            api_key = settings.QWEN_MODEL_API_KEY
            model_name = settings.QWEN_MODEL_NAME
            base_url = settings.QWEN_MODEL_BASE_URL
        else:
            api_key = settings.MODEL_API_KEY
            model_name = settings.MODEL_NAME
            base_url = settings.MODEL_BASE_URL
        
        client = OpenAI(
            api_key=api_key, 
            base_url=base_url,
        )
        # 从 md 文件中读取 prompt 内容
        prompt_file = "docs/prompt/coze_make_tag_from_notes_v0.2.md"
        with open(prompt_file, "r", encoding="utf-8") as f:
            system_prompt = f.read()
        completion = client.chat.completions.create(
            model=model_name, 
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"""请分析以下小红书笔记内容：
<小红书笔记>
{prompt}
</小红书笔记>"""}],
        )
        response_text = completion.choices[0].message.content
        # 确保目录存在
        log_dir = "logs/llm_http_request"
        date = datetime.now().strftime("%Y%m%d")
        os.makedirs(f"{log_dir}/{log_file_prefix}/{date}", exist_ok=True)
        # 生成文件名,使用时间戳避免重名
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{log_dir}/{log_file_prefix}/{date}/{timestamp}.json"
        # 保存响应内容
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(response_text, f, ensure_ascii=False, indent=2)
        
        return json.loads(response_text)
