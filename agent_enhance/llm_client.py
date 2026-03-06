"""
统一 LLM 调用封装模块

该模块封装了 LLM 调用逻辑，所有新增 Agent 统一通过此模块调用 LLM。
复用现有系统的环境变量配置，但提供独立的客户端实例。
"""

import os
import json
import logging
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass

# 配置日志
logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """LLM 配置数据类"""
    model_name: str = "qwen2.5:14b"
    base_url: str = "http://localhost:11434/v1"
    api_key: str = "ollama"
    timeout: int = 120
    
    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "LLMConfig":
        """从字典创建配置"""
        return cls(
            model_name=config.get("model_name", "qwen2.5:14b"),
            base_url=config.get("base_url", "http://localhost:11434/v1"),
            api_key=config.get("api_key", "ollama"),
            timeout=config.get("timeout", 120)
        )


class AgentLLMClient:
    """
    统一的 LLM 调用客户端
    
    特点：
    1. 封装底层 LLM 调用细节
    2. 支持 JSON 格式输出校验和重试
    3. 复用现有系统的环境变量配置
    """
    
    def __init__(self, config: Union[Dict[str, Any], LLMConfig]):
        """
        初始化 LLM 客户端
        
        Args:
            config: 配置字典或 LLMConfig 对象
        """
        if isinstance(config, dict):
            # 从配置字典创建，支持环境变量覆盖
            llm_config = config.get("llm", {})
            base_url_env = llm_config.get("base_url_env", "OPENAI_API_BASE")
            api_key_env = llm_config.get("api_key_env", "OPENAI_API_KEY")
            
            self.config = LLMConfig(
                model_name=llm_config.get("model_name", "qwen2.5:14b"),
                base_url=os.environ.get(base_url_env, llm_config.get("default_base_url", "http://localhost:11434/v1")),
                api_key=os.environ.get(api_key_env, llm_config.get("default_api_key", "ollama")),
                timeout=llm_config.get("timeout", 120)
            )
        else:
            self.config = config
        
        # 延迟初始化 OpenAI 客户端
        self._client = None
        
        logger.info(f"AgentLLMClient initialized with model: {self.config.model_name}")
    
    def _get_client(self):
        """获取或创建 OpenAI 客户端（延迟加载）"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    base_url=self.config.base_url,
                    api_key=self.config.api_key,
                    timeout=self.config.timeout
                )
            except ImportError:
                raise ImportError("openai package is required. Install with: pip install openai")
        return self._client
    
    def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        单次 LLM 调用，返回纯文本回答
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            temperature: 温度参数（默认0.1，低温度更确定）
            max_tokens: 最大生成token数
            
        Returns:
            LLM 生成的文本
        """
        client = self._get_client()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            answer = response.choices[0].message.content.strip()
            logger.debug(f"LLM call successful, response length: {len(answer)}")
            return answer
            
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            raise
    
    def call_json(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Dict[str, Any],
        temperature: float = 0.1,
        max_loop: int = 5,
        max_tokens: Optional[int] = None
    ) -> Union[Dict, list]:
        """
        调用 LLM 并校验 JSON 格式，失败自动重试
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            schema: JSON Schema 定义
            temperature: 温度参数
            max_loop: 最大重试次数
            max_tokens: 最大生成token数
            
        Returns:
            解析后的 JSON 对象（字典或列表）
        """
        from agent_enhance.output_checker import OutputChecker
        
        checker = OutputChecker(schema)
        last_error = None
        
        for attempt in range(max_loop):
            try:
                answer = self.call(system_prompt, user_prompt, temperature, max_tokens)
                result = checker.parse_and_validate(answer)
                
                if result is not None:
                    logger.info(f"JSON validation passed after {attempt + 1} attempt(s)")
                    return result
                    
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1}/{max_loop} failed: {last_error}")
                
                # 在重试时，添加更严格的指令
                if attempt < max_loop - 1:
                    user_prompt = f"""{user_prompt}

【重要提示】你之前的输出格式不正确，请严格按照 JSON 格式输出，不要添加任何额外说明文字。
确保输出可以被 Python 的 json.loads() 正确解析。"""
        
        # 所有重试都失败
        error_msg = f"Failed to get valid JSON after {max_loop} attempts. Last error: {last_error}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    def call_with_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        fallback_value: Any = None
    ) -> str:
        """
        带降级的 LLM 调用，失败时返回 fallback 值
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            temperature: 温度参数
            fallback_value: 失败时的返回值
            
        Returns:
            LLM 生成的文本，或 fallback_value
        """
        try:
            return self.call(system_prompt, user_prompt, temperature)
        except Exception as e:
            logger.error(f"LLM call failed, using fallback: {str(e)}")
            return fallback_value
