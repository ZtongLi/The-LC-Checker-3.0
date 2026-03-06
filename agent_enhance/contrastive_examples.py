"""
正反对比样本管理器

从 contrastive_data/ 加载正反例，根据当前审核涉及的具体字段
动态选择最相关的样本子集，格式化后返回可直接注入 prompt 的文本。
"""

import json
import os
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class SelectedExamples:
    """选中的正反例集合"""
    positive: List[Dict[str, Any]] = field(default_factory=list)   # 正例
    negative: List[Dict[str, Any]] = field(default_factory=list)   # 反例
    boundary: List[Dict[str, Any]] = field(default_factory=list)   # 边界案例
    
    def add_positive(self, example: Dict[str, Any]):
        """添加正例"""
        if example not in self.positive:
            self.positive.append(example)
    
    def add_negative(self, example: Dict[str, Any]):
        """添加反例"""
        if example not in self.negative:
            self.negative.append(example)
    
    def add_boundary(self, example: Dict[str, Any]):
        """添加边界案例"""
        if example not in self.boundary:
            self.boundary.append(example)
    
    def is_empty(self) -> bool:
        """检查是否为空"""
        return len(self.positive) == 0 and len(self.negative) == 0 and len(self.boundary) == 0


class ContrastiveExampleManager:
    """
    正反对比样本管理器
    
    功能：
    1. 加载正反例数据文件
    2. 根据单据内容智能选择相关案例
    3. 格式化为 prompt 文本
    """
    
    def __init__(self, data_dir: str = "contrastive_data"):
        """
        初始化管理器
        
        Args:
            data_dir: 数据文件目录路径
        """
        self.data_dir = data_dir
        self.positive_cases: List[Dict[str, Any]] = []
        self.negative_cases: List[Dict[str, Any]] = []
        self.boundary_cases: List[Dict[str, Any]] = []
        
        # 按类别索引
        self.positive_by_category: Dict[str, List[Dict[str, Any]]] = {}
        self.negative_by_category: Dict[str, List[Dict[str, Any]]] = {}
        self.boundary_by_category: Dict[str, List[Dict[str, Any]]] = {}
        
        self._load_data()
    
    def _load_data(self):
        """加载数据文件"""
        try:
            # 加载正例
            positive_path = os.path.join(self.data_dir, "positive_cases.json")
            if os.path.exists(positive_path):
                with open(positive_path, 'r', encoding='utf-8') as f:
                    self.positive_cases = json.load(f)
                self._index_by_category(self.positive_cases, self.positive_by_category)
                logger.info(f"Loaded {len(self.positive_cases)} positive cases")
            
            # 加载反例
            negative_path = os.path.join(self.data_dir, "negative_cases.json")
            if os.path.exists(negative_path):
                with open(negative_path, 'r', encoding='utf-8') as f:
                    self.negative_cases = json.load(f)
                self._index_by_category(self.negative_cases, self.negative_by_category)
                logger.info(f"Loaded {len(self.negative_cases)} negative cases")
            
            # 加载边界案例
            boundary_path = os.path.join(self.data_dir, "boundary_cases.json")
            if os.path.exists(boundary_path):
                with open(boundary_path, 'r', encoding='utf-8') as f:
                    self.boundary_cases = json.load(f)
                self._index_by_category(self.boundary_cases, self.boundary_by_category)
                logger.info(f"Loaded {len(self.boundary_cases)} boundary cases")
                
        except Exception as e:
            logger.error(f"Failed to load contrastive data: {e}")
    
    def _index_by_category(self, cases: List[Dict], index: Dict[str, List[Dict]]):
        """按类别建立索引"""
        for case in cases:
            category = case.get("category", "general")
            if category not in index:
                index[category] = []
            index[category].append(case)
    
    def select_relevant(
        self,
        lc: Dict[str, Any],
        invoice: Dict[str, Any],
        bl: Dict[str, Any],
        insurance: Dict[str, Any]
    ) -> SelectedExamples:
        """
        根据单据内容智能选择相关案例
        
        Args:
            lc: 信用证数据
            invoice: 发票数据
            bl: 提单数据
            insurance: 保险单数据
            
        Returns:
            选中的案例集合
        """
        selected = SelectedExamples()
        
        # 1. 金额容差相关
        amount_tolerance = lc.get("amount_tolerance", "")
        if amount_tolerance and amount_tolerance != "+/- 0%":
            self._add_from_category(selected, "amount_tolerance", "positive")
            self._add_from_category(selected, "amount_within_tolerance", "negative")
        else:
            self._add_from_category(selected, "amount_overdrawn", "positive")
        
        # 2. 公司名称一致性检查
        names = self._extract_names(lc, invoice, bl, insurance)
        unique_names = set(n.lower().strip() for n in names if n)
        if len(unique_names) > 1:
            # 检查是否为缩写差异
            self._add_from_category(selected, "name_equivalence", "negative")
        
        # 3. 约数词检查
        goods_desc = lc.get("goods_description", "")
        quantity = lc.get("quantity", "")
        text_to_check = f"{goods_desc} {quantity}".lower()
        if any(word in text_to_check for word in ["approximately", "about", "circa", "approx"]):
            self._add_from_category(selected, "approximate_quantity", "boundary")
        
        # 4. 保险险别检查
        coverage = insurance.get("coverage", "")
        required_coverage = lc.get("insurance_coverage", "")
        if coverage or required_coverage:
            self._add_from_category(selected, "insurance_coverage", "positive")
            self._add_from_category(selected, "coverage_missing", "positive")
        
        # 5. 港口匹配检查
        lc_loading = lc.get("shipment", {}).get("loading_port", "")
        bl_loading = bl.get("loading_port", "")
        if lc_loading and bl_loading:
            self._add_from_category(selected, "port_matching", "negative")
        
        # 6. 货物描述检查
        if goods_desc:
            self._add_from_category(selected, "goods_description_diff", "positive")
            self._add_from_category(selected, "singular_plural", "negative")
        
        # 7. 日期相关
        shipment_date = lc.get("shipment", {}).get("latest_date", "")
        bl_date = bl.get("shipped_on_board_date", "")
        if shipment_date and bl_date:
            self._add_from_category(selected, "late_shipment", "positive")
            self._add_from_category(selected, "date_format_diff", "negative")
        
        # 8. 货币检查
        lc_currency = lc.get("currency", "")
        inv_currency = invoice.get("currency", "")
        if lc_currency and inv_currency and lc_currency != inv_currency:
            self._add_from_category(selected, "currency_mismatch", "positive")
        
        # 9. 提单清洁度
        bl_clean = bl.get("clean_on_board", True)
        if not bl_clean:
            self._add_from_category(selected, "dirty_bl", "positive")
        
        # 10. 地址差异
        self._add_from_category(selected, "address_minor_diff", "negative")
        
        # 11. 单据份数检查
        required_docs = lc.get("required_documents", "")
        if isinstance(required_docs, list):
            required_docs = " ".join(str(d) for d in required_docs)
        required_docs_lower = str(required_docs).lower()
        if any(w in required_docs_lower for w in ["triplicate", "full set", "3/3", "duplicate", "份"]):
            self._add_from_category(selected, "document_copies", "positive")
        # 始终检查份数（高频漏报项）
        self._add_from_category(selected, "document_copies", "positive")
        
        # 12. 贸易术语检查
        lc_trade = lc.get("trade_terms", lc.get("incoterms", ""))
        inv_trade = invoice.get("trade_terms", invoice.get("incoterms", ""))
        if lc_trade or inv_trade:
            self._add_from_category(selected, "trade_terms_mismatch", "positive")
        # 始终检查贸易术语
        self._add_from_category(selected, "trade_terms_mismatch", "positive")
        
        # 13. 保险被保险人名称检查
        insured = insurance.get("insured", insurance.get("insured_party", ""))
        beneficiary = lc.get("beneficiary", {})
        if isinstance(beneficiary, dict):
            beneficiary_name = beneficiary.get("name", "")
        else:
            beneficiary_name = str(beneficiary)
        if insured and beneficiary_name:
            self._add_from_category(selected, "insured_name_mismatch", "positive")

        # 14. 始终包含一些通用案例
        self._add_from_category(selected, "general_abbreviations", "negative")
        
        logger.info(f"Selected examples: {len(selected.positive)} positive, "
                   f"{len(selected.negative)} negative, {len(selected.boundary)} boundary")
        
        return selected
    
    def _extract_names(self, lc, invoice, bl, insurance) -> List[str]:
        """提取各单据中的名称"""
        names = []
        
        # 信用证受益人
        beneficiary = lc.get("beneficiary", {})
        if isinstance(beneficiary, dict):
            names.append(beneficiary.get("name", ""))
        elif isinstance(beneficiary, str):
            names.append(beneficiary)
        
        # 发票出具人
        names.append(invoice.get("issued_by", ""))
        names.append(invoice.get("seller", ""))
        
        # 提单托运人
        names.append(bl.get("shipper", ""))
        
        # 保险单被保险人
        insured = insurance.get("insured", "")
        if isinstance(insured, list):
            names.extend(insured)
        else:
            names.append(insured)
        
        return [n for n in names if n]
    
    def _add_from_category(
        self,
        selected: SelectedExamples,
        category: str,
        case_type: str,
        max_items: int = 2
    ):
        """从指定类别添加案例"""
        if case_type == "positive":
            cases = self.positive_by_category.get(category, [])
            for case in cases[:max_items]:
                selected.add_positive(case)
        elif case_type == "negative":
            cases = self.negative_by_category.get(category, [])
            for case in cases[:max_items]:
                selected.add_negative(case)
        elif case_type == "boundary":
            cases = self.boundary_by_category.get(category, [])
            for case in cases[:max_items]:
                selected.add_boundary(case)
    
    def format_for_prompt(self, selected: SelectedExamples, max_positive: int = 5, 
                         max_negative: int = 5, max_boundary: int = 3) -> str:
        """
        将选中的案例格式化为 prompt 文本
        
        Args:
            selected: 选中的案例集合
            max_positive: 最大正例数
            max_negative: 最大反例数
            max_boundary: 最大边界案例数
            
        Returns:
            格式化后的 prompt 文本
        """
        if selected.is_empty():
            return ""
        
        lines = []
        lines.append("=" * 60)
        lines.append("【正反对比学习样本 —— 供 AI 审核参考】")
        lines.append("=" * 60)
        
        # 正例
        if selected.positive:
            lines.append("\n📌 正例（应判为不符点的场景）：")
            lines.append("-" * 40)
            for i, case in enumerate(selected.positive[:max_positive], 1):
                lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
                lines.append(f"  涉及字段: {case.get('lc_field', {}).get('field', 'N/A')} vs {case.get('doc_field', {}).get('field', 'N/A')}")
                lines.append(f"  判断结果: ✅ 构成不符点（{case.get('severity', '一般')}）")
                lines.append(f"  依据条款: {case.get('ucp_reference', 'N/A')}")
                lines.append(f"  说明: {case.get('explanation', '')}")
        
        # 反例
        if selected.negative:
            lines.append("\n\n📌 反例（不应判为不符点的场景 —— 常见误判）：")
            lines.append("-" * 40)
            for i, case in enumerate(selected.negative[:max_negative], 1):
                lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
                lines.append(f"  涉及字段: {case.get('lc_field', {}).get('field', 'N/A')} vs {case.get('doc_field', {}).get('field', 'N/A')}")
                lines.append(f"  判断结果: ❌ 不构成不符点")
                lines.append(f"  说明: {case.get('explanation', '')}")
        
        # 边界案例
        if selected.boundary:
            lines.append("\n\n📌 边界案例（需特别注意的判断标准）：")
            lines.append("-" * 40)
            for i, case in enumerate(selected.boundary[:max_boundary], 1):
                lines.append(f"\n【案例 {i}】{case.get('scenario', '')}")
                lines.append(f"  判断标准: {case.get('criteria', '')}")
                lines.append(f"  依据条款: {case.get('ucp_reference', 'N/A')}")
                lines.append(f"  说明: {case.get('explanation', '')}")
        
        lines.append("\n" + "=" * 60)
        lines.append("【请 AI 审核员参考以上案例，对当前单据进行准确判断】")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def get_all_categories(self) -> Dict[str, List[str]]:
        """获取所有可用的类别"""
        return {
            "positive": list(self.positive_by_category.keys()),
            "negative": list(self.negative_by_category.keys()),
            "boundary": list(self.boundary_by_category.keys())
        }
