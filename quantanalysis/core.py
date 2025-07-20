"""核心QuantAnalysis类 - 简化版"""

from typing import Optional, Dict, Any
import pandas as pd
import numpy as np

from . import stats, utils, reports
from .i18n import set_language, get_language, t


class QuantAnalysis:
    """简化的投资组合分析类
    
    专注于核心功能：分析计算和报告生成
    """
    
    def __init__(
        self,
        risk_free_rate: float = 0.0,
        language: str = "zh",
        periods_per_year: int = 252
    ):
        """初始化分析器
        
        Args:
            risk_free_rate: 无风险收益率 (年化)
            language: 语言设置 ('zh' 中文, 'en' 英文)
            periods_per_year: 年化周期 (默认252个交易日)
        """
        self.risk_free_rate = risk_free_rate
        self.language = language
        self.periods_per_year = periods_per_year
        
        # Set global language for i18n
        set_language(language)
    
    def analyze(
        self,
        returns: pd.Series,
        benchmark: Optional[pd.Series] = None
    ) -> Dict[str, Any]:
        """分析投资组合性能
        
        Args:
            returns: 投资组合收益率序列
            benchmark: 基准收益率序列 (可选)
            
        Returns:
            包含所有分析指标的字典
        """
        returns = self._prepare_returns(returns)
        
        # 基础收益指标
        returns_stats = {
            'total_return': stats.comp(returns),
            'cagr': stats.cagr(returns, periods=self.periods_per_year),
            'mean_return': returns.mean(),
            'std_return': returns.std(),
            'skewness': stats.skew(returns),
            'kurtosis': stats.kurtosis(returns)
        }
        
        # 风险指标
        risk_metrics = {
            'volatility': stats.volatility(returns, periods=self.periods_per_year),
            'max_drawdown': stats.max_drawdown(returns),
            'var_95': stats.value_at_risk(returns, confidence=0.95),
            'cvar_95': stats.conditional_value_at_risk(returns, confidence=0.95),
            'ulcer_index': stats.ulcer_index(returns)
        }
        
        # 绩效指标
        performance_metrics = {
            'sharpe': stats.sharpe(returns, rf=self.risk_free_rate, periods=self.periods_per_year),
            'sortino': stats.sortino(returns, rf=self.risk_free_rate, periods=self.periods_per_year),
            'calmar': stats.calmar(returns),
            'omega': stats.omega(returns)
        }
        
        # 回撤指标
        dd_series = stats.to_drawdown_series(returns)
        drawdown_metrics = {
            'max_drawdown': stats.max_drawdown(returns),
            'avg_drawdown': dd_series.mean(),
            'recovery_factor': stats.recovery_factor(returns)
        }
        
        metrics = {
            'returns_stats': returns_stats,
            'risk_metrics': risk_metrics,
            'performance_metrics': performance_metrics,
            'drawdown_metrics': drawdown_metrics
        }
        
        # 如果有基准，计算相对指标
        if benchmark is not None:
            benchmark = self._prepare_returns(benchmark)
            aligned_returns, aligned_benchmark = returns.align(benchmark, join='inner')
            
            if len(aligned_returns) > 1:
                # 计算alpha和beta
                excess_returns = aligned_returns - self.risk_free_rate / self.periods_per_year
                excess_benchmark = aligned_benchmark - self.risk_free_rate / self.periods_per_year
                
                try:
                    correlation = excess_returns.corr(excess_benchmark)
                    beta = correlation * (excess_returns.std() / excess_benchmark.std())
                    alpha = excess_returns.mean() - beta * excess_benchmark.mean()
                    
                    performance_metrics.update({
                        'alpha': alpha * self.periods_per_year,
                        'beta': beta,
                        'information_ratio': stats.information_ratio(aligned_returns, aligned_benchmark)
                    })
                except:
                    performance_metrics.update({
                        'alpha': 0.0,
                        'beta': 1.0,
                        'information_ratio': 0.0
                    })
                
                # 相对指标
                excess = aligned_returns - aligned_benchmark
                relative_metrics = {
                    'excess_return': excess.mean() * self.periods_per_year,
                    'tracking_error': excess.std() * np.sqrt(self.periods_per_year),
                    'information_ratio': stats.information_ratio(aligned_returns, aligned_benchmark)
                }
                
                metrics['relative_metrics'] = relative_metrics
        
        return metrics
    
    def generate_report(
        self,
        returns: pd.Series,
        benchmark: Optional[pd.Series] = None,
        title: Optional[str] = None,
        returns_freq: str = "M"
    ) -> str:
        """生成HTML分析报告
        
        Args:
            returns: 投资组合收益率序列
            benchmark: 基准收益率序列 (可选)
            title: 报告标题
            returns_freq: 收益率柱状图频率 ('D'=日频, 'W'=周频, 'M'=月频)
            
        Returns:
            生成的HTML文件路径
        """
        # 执行分析
        metrics = self.analyze(returns, benchmark)
        
        # 确保语言设置正确
        set_language(self.language)
        
        # 生成报告
        return reports.generate_html_report(
            returns=returns,
            benchmark=benchmark,
            metrics=metrics,
            title=title or t("report.title"),
            language=self.language,
            config={
                'risk_free_rate': self.risk_free_rate,
                'periods_per_year': self.periods_per_year
            },
            returns_freq=returns_freq
        )
    
    def _prepare_returns(self, returns: pd.Series) -> pd.Series:
        """预处理收益率数据"""
        if not isinstance(returns, pd.Series):
            raise TypeError(t("errors.invalid_returns"))
        
        # 移除NaN值
        returns = returns.dropna()
        
        # 确保日期索引
        if not isinstance(returns.index, pd.DatetimeIndex):
            try:
                returns.index = pd.to_datetime(returns.index)
            except:
                raise ValueError(t("errors.invalid_date_index"))
        
        return returns
    
    def set_language(self, language: str) -> None:
        """Set analysis language
        
        Args:
            language: Language code ('zh' for Chinese, 'en' for English)
        """
        self.language = language
        set_language(language)
    
    def get_language(self) -> str:
        """Get current analysis language
        
        Returns:
            Current language code
        """
        return self.language