#!/usr/bin/env python3
"""
Example demonstrating i18n (internationalization) functionality
for QuantAnalysis package with Chinese and English support.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from quantanalysis import QuantAnalysis, set_language, get_language, get_supported_languages


def generate_sample_data():
    """Generate sample portfolio returns data"""
    np.random.seed(42)
    
    # Create sample data for 2 years
    dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
    
    # Generate portfolio returns with some volatility
    returns = np.random.normal(0.0008, 0.02, len(dates))  # Daily returns with 2% volatility
    
    # Add some market effects
    returns = pd.Series(returns, index=dates)
    
    # Create benchmark (market) returns - slightly lower returns but more stable
    benchmark_returns = np.random.normal(0.0006, 0.015, len(dates))
    benchmark = pd.Series(benchmark_returns, index=dates)
    
    return returns, benchmark


def demonstrate_language_switching():
    """Demonstrate language switching functionality"""
    print("=" * 60)
    print("QuantAnalysis i18n Demonstration")
    print("=" * 60)
    print()
    
    # Show supported languages
    supported_langs = get_supported_languages()
    print(f"Supported languages: {supported_langs}")
    print(f"Current language: {get_language()}")
    print()
    
    # Generate sample data
    returns, benchmark = generate_sample_data()
    
    # Test with Chinese (default)
    print("1. Analysis in Chinese (中文)")
    print("-" * 40)
    
    analyzer_zh = QuantAnalysis(language="zh")
    print(f"Language set to: {analyzer_zh.get_language()}")
    
    # Perform analysis
    metrics_zh = analyzer_zh.analyze(returns, benchmark)
    
    # Show some key metrics
    print(f"总收益率: {metrics_zh['returns_stats']['total_return']:.2%}")
    print(f"复合年增长率: {metrics_zh['returns_stats']['cagr']:.2%}")
    print(f"最大回撤: {metrics_zh['risk_metrics']['max_drawdown']:.2%}")
    print(f"夏普比率: {metrics_zh['performance_metrics']['sharpe']:.3f}")
    print()
    
    # Generate HTML report in Chinese (with custom title)
    report_file_zh = analyzer_zh.generate_report(
        returns=returns,
        benchmark=benchmark,
        title="投资组合分析报告 - 中文示例"
    )
    print(f"Chinese report (custom title): {report_file_zh}")
    
    # Generate HTML report in Chinese (with default i18n title)
    report_file_zh_default = analyzer_zh.generate_report(
        returns=returns,
        benchmark=benchmark,
        title=None  # Use default i18n title
    )
    print(f"Chinese report (default title): {report_file_zh_default}")
    print()
    
    # Test with English
    print("2. Analysis in English")
    print("-" * 40)
    
    analyzer_en = QuantAnalysis(language="en")
    print(f"Language set to: {analyzer_en.get_language()}")
    
    # Perform analysis  
    metrics_en = analyzer_en.analyze(returns, benchmark)
    
    # Show same metrics in English
    print(f"Total Return: {metrics_en['returns_stats']['total_return']:.2%}")
    print(f"CAGR: {metrics_en['returns_stats']['cagr']:.2%}")
    print(f"Max Drawdown: {metrics_en['risk_metrics']['max_drawdown']:.2%}")
    print(f"Sharpe Ratio: {metrics_en['performance_metrics']['sharpe']:.3f}")
    print()
    
    # Generate HTML report in English (with custom title)
    report_file_en = analyzer_en.generate_report(
        returns=returns,
        benchmark=benchmark,
        title="Portfolio Analysis Report - English Example"
    )
    print(f"English report (custom title): {report_file_en}")
    
    # Generate HTML report in English (with default i18n title)
    report_file_en_default = analyzer_en.generate_report(
        returns=returns,
        benchmark=benchmark,
        title=None  # Use default i18n title
    )
    print(f"English report (default title): {report_file_en_default}")
    print()
    
    # Test dynamic language switching
    print("3. Dynamic Language Switching")
    print("-" * 40)
    
    analyzer = QuantAnalysis(language="zh")
    print(f"Initial language: {analyzer.get_language()}")
    
    # Switch to English
    analyzer.set_language("en")
    print(f"Switched to: {analyzer.get_language()}")
    
    # Switch back to Chinese
    analyzer.set_language("zh")
    print(f"Switched back to: {analyzer.get_language()}")
    print()
    
    # Test global language setting
    print("4. Global Language Setting")
    print("-" * 40)
    
    # Set global language
    set_language("en")
    print(f"Global language set to: {get_language()}")
    
    # Create new analyzer (should inherit global setting)
    analyzer_global = QuantAnalysis()
    print(f"New analyzer language: {analyzer_global.get_language()}")
    
    # Reset to Chinese
    set_language("zh")
    print(f"Global language reset to: {get_language()}")
    print()
    
    print("=" * 60)
    print("i18n demonstration completed!")
    print("Generated reports can be opened in a web browser.")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_language_switching()