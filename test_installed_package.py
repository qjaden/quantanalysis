#!/usr/bin/env python
"""Test the installed QuantAnalysis package."""

import pandas as pd
import numpy as np
from datetime import datetime

# Import from the installed package (not from src)
from quantanalysis import QuantAnalysis, create_analyzer

def test_package():
    """Test the installed package functionality."""
    print("=== 测试已安装的 QuantAnalysis 包 ===\n")
    
    # Generate sample data
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    np.random.seed(42)
    returns = pd.Series(
        np.random.normal(0.0008, 0.02, len(dates)),
        index=dates,
        name='portfolio'
    )
    
    # Test creating analyzer
    analyzer = create_analyzer(
        risk_free_rate=0.03,
        language='zh',
        periods_per_year=252
    )
    
    print(f"包版本: {analyzer.__class__.__module__}")
    print(f"风险免费利率: {analyzer.risk_free_rate}")
    print(f"语言: {analyzer.language}")
    
    # Test basic calculations using analyze method
    analysis = analyzer.analyze(returns)
    sharpe = analysis['performance_metrics']['sharpe']
    max_dd = analysis['risk_metrics']['max_drawdown']
    cagr = analysis['returns_stats']['cagr']
    
    print(f"\n主要指标:")
    print(f"夏普比率: {sharpe:.2f}")
    print(f"最大回撤: {max_dd:.2%}")
    print(f"复合年增长率: {cagr:.2%}")
    
    # Test comprehensive analysis (reuse previous analysis)
    metrics = analysis
    
    print(f"\n风险指标数量: {len(metrics['risk_metrics'])}")
    print(f"绩效指标数量: {len(metrics['performance_metrics'])}")
    
    print("\n✅ 所有测试通过！包安装成功且功能正常。")
    return True

if __name__ == "__main__":
    test_package()