#!/usr/bin/env python
"""QuantAnalysis 简单使用示例"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
import pandas as pd
import numpy as np
from datetime import datetime

from quantanalysis import QuantAnalysis


def main():
    """演示QuantAnalysis的基本使用"""
    print("=== QuantAnalysis 简化版使用示例 ===\n")
    
    # 1. 生成示例数据
    print("1. 生成示例数据...")
    dates = pd.date_range('2021-01-01', '2023-12-31', freq='D')
    dates2 = pd.date_range('2022-01-01', '2023-12-31', freq='D')
    np.random.seed(42)
    
    # 投资组合收益率
    returns = pd.Series(
        np.random.normal(0.0008, 0.02, len(dates)),
        index=dates,
        name='投资组合'
    )
    
    # 基准收益率
    benchmark = pd.Series(
        np.random.normal(0.0005, 0.015, len(dates2)),
        index=dates2,
        name='基准'
    )
    
    print(f"   数据期间: {returns.index[0].date()} 至 {returns.index[-1].date()}")
    print(f"   数据点数: {len(returns)} 天\n")
    
    # 2. 创建分析器
    print("2. 创建分析器...")
    analyzer = QuantAnalysis(
        risk_free_rate=0.03,  # 3% 无风险收益率
        language='zh'         # 中文界面
    )
    print("   分析器配置完成\n")
    
    # 3. 计算基本指标
    print("3. 计算关键指标...")
    sharpe = analyzer.analyze(returns)['performance_metrics']['sharpe']
    max_dd = analyzer.analyze(returns)['risk_metrics']['max_drawdown']
    cagr = analyzer.analyze(returns)['returns_stats']['cagr']
    
    print(f"   夏普比率: {sharpe:.3f}")
    print(f"   最大回撤: {max_dd:.2%}")
    print(f"   复合年增长率: {cagr:.2%}\n")
    
    # 4. 生成完整报告
    print("4. 生成HTML报告...")
    
    # 只分析投资组合
    report_file1 = analyzer.generate_report(
        returns,
        title="我的投资组合分析",
        returns_freq="D"
    )
    
    # 包含基准比较
    report_file2 = analyzer.generate_report(
        returns, 
        benchmark=benchmark,
        title="投资组合 vs 基准对比分析"
    )
    
    print(f"   ✅ 投资组合报告: {report_file1}")
    print(f"   ✅ 对比分析报告: {report_file2}")
    
    # 显示报告文件信息
    import os
    size1 = os.path.getsize(report_file1) / 1024
    size2 = os.path.getsize(report_file2) / 1024
    
    print(f"\n📄 报告文件信息:")
    print(f"   文件1大小: {size1:.1f} KB")
    print(f"   文件2大小: {size2:.1f} KB")
    
    print(f"\n🎉 分析完成！")
    print(f"请在浏览器中打开以下文件查看报告:")
    print(f"   • {report_file1}")
    print(f"   • {report_file2}")
    
    print(f"\n📋 报告包含内容:")
    print(f"   • 业绩概览卡片（6个核心指标）")
    print(f"   • 4个美观图表（累计收益、回撤、热力图、分布）")
    print(f"   • 详细指标表格")
    print(f"   • 响应式设计，支持手机查看")
    print(f"   • 中文界面，字体显示优化")
    

if __name__ == "__main__":
    main()