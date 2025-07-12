"""QuantAnalysis: 现代投资组合分析工具

基于QuantStats重构的简化版量化分析包，专注于生成美观的HTML报告。
"""

from typing import Optional

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .core import QuantAnalysis
from . import stats, utils

__all__ = ["QuantAnalysis", "stats", "utils", "__version__"]


def create_analyzer(
    risk_free_rate: float = 0.0,
    language: str = "zh",
    periods_per_year: int = 252,
) -> QuantAnalysis:
    """创建QuantAnalysis实例的便捷函数
    
    Args:
        risk_free_rate: 年化无风险收益率 (默认: 0.0)
        language: 语言设置 ('zh' 中文, 'en' 英文)
        periods_per_year: 年化周期 (默认: 252)
        
    Returns:
        配置好的QuantAnalysis实例
    """
    return QuantAnalysis(
        risk_free_rate=risk_free_rate,
        language=language,
        periods_per_year=periods_per_year,
    )