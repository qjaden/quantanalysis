#!/usr/bin/env python
"""Example usage of QuantAnalysis package."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import the main package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from quantanalysis import QuantAnalysis, create_analyzer


def generate_sample_data():
    """Generate sample portfolio and benchmark data."""
    # Create date range
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Generate portfolio returns with some trend and volatility
    np.random.seed(42)  # For reproducible results
    
    # Portfolio with slight positive drift and higher volatility
    portfolio_returns = pd.Series(
        np.random.normal(0.0008, 0.02, len(dates)),  # 20% annual drift, 32% volatility
        index=dates,
        name='portfolio'
    )
    
    # Benchmark with lower drift and volatility
    benchmark_returns = pd.Series(
        np.random.normal(0.0005, 0.015, len(dates)),  # 12.5% annual drift, 24% volatility
        index=dates,
        name='benchmark'
    )
    
    return portfolio_returns, benchmark_returns


def example_basic_analysis():
    """Demonstrate basic analysis functionality."""
    print("=== 基本分析示例 ===\n")
    
    # Generate sample data
    returns, benchmark = generate_sample_data()
    
    # Create analyzer with Chinese language
    analyzer = QuantAnalysis(
        risk_free_rate=0.03,
        periods_per_year=252,
        language='zh'
    )
    
    # Calculate individual metrics
    print("主要指标:")
    print(f"总收益: {analyzer.calculate_sharpe(returns):.2f}")
    print(f"夏普比率: {analyzer.calculate_sharpe(returns):.2f}")
    print(f"索提诺比率: {analyzer.calculate_sortino(returns):.2f}")
    print(f"最大回撤: {analyzer.calculate_max_drawdown(returns):.2%}")
    print(f"复合年增长率: {analyzer.calculate_cagr(returns):.2%}")
    print(f"年化波动率: {analyzer.calculate_volatility(returns):.2%}")
    print()


def example_comprehensive_analysis():
    """Demonstrate comprehensive analysis with benchmark."""
    print("=== 综合分析示例 ===\n")
    
    # Generate sample data
    returns, benchmark = generate_sample_data()
    
    # Create analyzer
    analyzer = QuantAnalysis(
        risk_free_rate=0.03,
        language='zh'
    )
    
    # Perform comprehensive analysis
    metrics = analyzer.analyze(returns, benchmark)
    
    # Display results
    print("收益统计:")
    for key, value in metrics['returns_stats'].items():
        if isinstance(value, float):
            if 'return' in key or 'cagr' in key:
                print(f"  {key}: {value:.2%}")
            else:
                print(f"  {key}: {value:.4f}")
    
    print("\n风险指标:")
    for key, value in metrics['risk_metrics'].items():
        if isinstance(value, float):
            if 'drawdown' in key or 'volatility' in key:
                print(f"  {key}: {value:.2%}")
            else:
                print(f"  {key}: {value:.4f}")
    
    print("\n绩效指标:")
    for key, value in metrics['performance_metrics'].items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
    
    if 'relative_metrics' in metrics:
        print("\n相对指标:")
        for key, value in metrics['relative_metrics'].items():
            if isinstance(value, float):
                if 'return' in key or 'error' in key:
                    print(f"  {key}: {value:.2%}")
                else:
                    print(f"  {key}: {value:.4f}")
    print()


def example_english_analysis():
    """Demonstrate analysis with English language."""
    print("=== English Analysis Example ===\n")
    
    # Generate sample data
    returns, benchmark = generate_sample_data()
    
    # Create analyzer with English language
    analyzer = QuantAnalysis(
        risk_free_rate=0.03,
        language='en'
    )
    
    # Calculate key metrics
    print("Key Metrics:")
    print(f"Total Return: {(1 + returns).prod() - 1:.2%}")
    print(f"Sharpe Ratio: {analyzer.calculate_sharpe(returns):.2f}")
    print(f"Sortino Ratio: {analyzer.calculate_sortino(returns):.2f}")
    print(f"Max Drawdown: {analyzer.calculate_max_drawdown(returns):.2%}")
    print(f"CAGR: {analyzer.calculate_cagr(returns):.2%}")
    print(f"Volatility: {analyzer.calculate_volatility(returns):.2%}")
    print()


def example_convenience_function():
    """Demonstrate using the convenience function."""
    print("=== 便捷函数示例 ===\n")
    
    # Generate sample data
    returns, benchmark = generate_sample_data()
    
    # Use the convenience function
    analyzer = create_analyzer(
        risk_free_rate=0.025,
        language='zh',
        periods_per_year=252
    )
    
    print("使用便捷函数创建的分析器:")
    print(f"风险免费利率: {analyzer.risk_free_rate}")
    print(f"语言设置: {analyzer.language}")
    print(f"年化周期: {analyzer.periods_per_year}")
    print()


if __name__ == "__main__":
    print("QuantAnalysis 使用示例\n")
    print("=" * 50)
    
    # Run all examples
    example_basic_analysis()
    example_comprehensive_analysis()
    example_english_analysis()
    example_convenience_function()
    
    print("所有示例运行完成！")
    print("\n要在 Jupyter Notebook 中查看完整的交互式报告，请使用:")
    print("analyzer.create_dashboard(returns, benchmark)")
    print("analyzer.generate_report(returns, benchmark)")