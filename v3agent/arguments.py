"""
⚙️ 配置管理 - 参数加载

负责：
1. 加载和解析配置文件
2. 环境变量处理
3. 全局配置管理
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AgentConfig:
    """Agent 配置"""
    enabled: bool = True
    temperature: float = 0.1
    max_terms: int = 10
    chromadb_top_k: int = 5


@dataclass
class LLMConfig:
    """LLM 配置"""
    model_name: str = "qwen2.5:14b"
    base_url: str = "http://localhost:11434/v1"
    api_key: str = "ollama"
    timeout: int = 120


@dataclass
class ContrastiveConfig:
    """对比学习配置"""
    enabled: bool = True
    data_dir: str = "contrastive_data"
    max_positive: int = 5
    max_negative: int = 5
    max_boundary: int = 3


@dataclass
class OutputCheckerConfig:
    """输出校验配置"""
    enabled: bool = True
    max_loop: int = 5
    use_json_repair: bool = True


@dataclass
class FallbackConfig:
    """降级策略配置"""
    on_planner_fail: str = "skip"
    on_knowledge_fail: str = "skip"
    on_reflection_fail: str = "use_original"
    on_all_fail: str = "fallback_to_v2"


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config/agent_config.json"):
        self.config_path = config_path
        self.raw_config: Dict[str, Any] = {}
        
        self.planner = AgentConfig()
        self.knowledge = AgentConfig()
        self.reflection = AgentConfig()
        self.llm = LLMConfig()
        self.contrastive = ContrastiveConfig()
        self.output_checker = OutputCheckerConfig()
        self.fallback = FallbackConfig()
        
        self._load_config()
        
    def _load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            logging.warning(f"Config file not found: {self.config_path}, using defaults")
            return
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.raw_config = json.load(f)
            
            self._parse_agents_config()
            self._parse_llm_config()
            self._parse_contrastive_config()
            self._parse_output_checker_config()
            self._parse_fallback_config()
            
            logging.info(f"Config loaded from: {self.config_path}")
            
        except Exception as e:
            logging.error(f"Failed to load config: {e}, using defaults")
    
    def _parse_agents_config(self):
        """解析 Agent 配置"""
        agents = self.raw_config.get("agents", {})
        
        if "planner" in agents:
            p = agents["planner"]
            self.planner = AgentConfig(
                enabled=p.get("enabled", True),
                temperature=p.get("temperature", 0.2),
                max_terms=p.get("max_terms", 10)
            )
        
        if "knowledge" in agents:
            k = agents["knowledge"]
            self.knowledge = AgentConfig(
                enabled=k.get("enabled", True),
                temperature=k.get("temperature", 0.1),
                chromadb_top_k=k.get("chromadb_top_k", 5)
            )
        
        if "reflection" in agents:
            r = agents["reflection"]
            self.reflection = AgentConfig(
                enabled=r.get("enabled", True),
                temperature=r.get("temperature", 0.1)
            )
    
    def _parse_llm_config(self):
        """解析 LLM 配置"""
        llm = self.raw_config.get("llm", {})
        
        base_url_env = llm.get("base_url_env", "OPENAI_API_BASE")
        api_key_env = llm.get("api_key_env", "OPENAI_API_KEY")
        
        self.llm = LLMConfig(
            model_name=llm.get("model_name", "qwen2.5:14b"),
            base_url=os.environ.get(base_url_env, llm.get("default_base_url", "http://localhost:11434/v1")),
            api_key=os.environ.get(api_key_env, llm.get("default_api_key", "ollama")),
            timeout=llm.get("timeout", 120)
        )
    
    def _parse_contrastive_config(self):
        """解析对比学习配置"""
        ce = self.raw_config.get("contrastive_examples", {})
        self.contrastive = ContrastiveConfig(
            enabled=ce.get("enabled", True),
            data_dir=ce.get("data_dir", "contrastive_data"),
            max_positive=ce.get("max_positive", 5),
            max_negative=ce.get("max_negative", 5),
            max_boundary=ce.get("max_boundary", 3)
        )
    
    def _parse_output_checker_config(self):
        """解析输出校验配置"""
        oc = self.raw_config.get("output_checker", {})
        self.output_checker = OutputCheckerConfig(
            enabled=oc.get("enabled", True),
            max_loop=oc.get("max_loop", 5),
            use_json_repair=oc.get("use_json_repair", True)
        )
    
    def _parse_fallback_config(self):
        """解析降级策略配置"""
        fb = self.raw_config.get("fallback", {})
        self.fallback = FallbackConfig(
            on_planner_fail=fb.get("on_planner_fail", "skip"),
            on_knowledge_fail=fb.get("on_knowledge_fail", "skip"),
            on_reflection_fail=fb.get("on_reflection_fail", "use_original"),
            on_all_fail=fb.get("on_all_fail", "fallback_to_v2")
        )
    
    def setup_logging(self):
        """设置日志级别"""
        log_level = self.raw_config.get("logging", {}).get("level", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )


# 全局配置实例
_config_instance: Optional[ConfigManager] = None


def get_config(config_path: str = "config/agent_config.json") -> ConfigManager:
    """获取全局配置实例（单例模式）"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager(config_path)
    return _config_instance
