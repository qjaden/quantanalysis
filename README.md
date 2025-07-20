# QuantAnalysis

<div align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/license-Apache%202.0-green.svg" alt="License">
  <img src="https://img.shields.io/badge/reports-HTML-orange.svg" alt="HTML Reports">
  <img src="https://img.shields.io/badge/language-中文%2FEnglish-red.svg" alt="Language Support">
</div>

<p align="center">
  <strong>基于 QuantStats 的现代化投资组合分析工具</strong><br>
  提供面向对象设计、中文语言支持和 HTML 报告生成
</p>

<p align="center">
  <em>A modernized portfolio analytics toolkit based on QuantStats, featuring object-oriented design, Chinese language support, and comprehensive HTML reporting.</em>
</p>

---

## ✨ 特性 Features

| Feature | Description |
|---------|-------------|
| 🎯 **面向对象设计** | 通过 `QuantAnalysis` 类统一管理所有分析功能 |
| 🇨🇳 **中文支持** | 完整的中文界面和报告支持 |
| 📄 **HTML 报告** | 生成专业的 HTML 格式分析报告 |
| ⚙️ **可配置参数** | 预设无风险收益率、基准等参数 |
| 📈 **丰富的指标** | 包含风险、收益、回撤等全面的量化指标 |
| 🎨 **美观的可视化** | 现代化的图表和报告设计 |

## 📦 安装 Installation

### 从 PyPI 安装 (暂不支持)

```bash
pip install quantanalysis
```

### 从源码安装

```bash
git clone https://github.com/yourusername/quantanalysis.git
cd quantanalysis
pip install -e .
```

### 🎨 中文字体支持

QuantAnalysis 已内置中文字体支持，无需额外配置即可正常显示中文图表。

**内置字体：**
- `SimHei.otf` (黑体)
- 自动检测系统微软雅黑字体

> 💡 字体文件已集成到安装包中，安装即可使用

## 🚀 快速开始 Quick Start

### 📋 基本用法

<details>
<summary>点击展开完整示例 Click to expand</summary>

```python
import pandas as pd
import numpy as np
from quantanalysis import QuantAnalysis

# 📊 生成示例数据
dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
returns = pd.Series(
    np.random.normal(0.0005, 0.02, len(dates)), 
    index=dates, 
    name='portfolio'
)

# ⚙️ 创建分析器
analyzer = QuantAnalysis(
    risk_free_rate=0.03,      # 3% 无风险收益率
    periods_per_year=252,     # 年交易日数
    language='zh'             # 中文界面
)

# 📈 生成完整分析报告
analyzer.generate_report(returns, title="我的投资组合分析")
```
</details>

### 📊 获取分析指标

```python
# 🎯 获取完整指标分析
metrics = analyzer.analyze(returns)

# 📋 访问具体指标
print(f"📈 夏普比率: {metrics['performance_metrics']['sharpe']:.2f}")
print(f"📉 最大回撤: {metrics['risk_metrics']['max_drawdown']:.2%}")
print(f"💰 复合年增长率: {metrics['return_metrics']['cagr']:.2%}")

# 📊 打印所有指标
for category, category_metrics in metrics.items():
    print(f"\n=== {category} ===")
    for metric, value in category_metrics.items():
        print(f"{metric}: {value}")
```

### 🔍 与基准比较

<details>
<summary>基准比较示例</summary>

```python
# 📊 生成基准数据 (如沪深300)
benchmark = pd.Series(
    np.random.normal(0.0003, 0.015, len(dates)), 
    index=dates, 
    name='hs300'
)

# 📋 完整对比分析 (包含相对指标)
metrics = analyzer.analyze(returns, benchmark)

# 🔍 访问相对指标
print(f"🔺 Alpha: {metrics['relative_metrics']['alpha']:.2%}")
print(f"📈 Beta: {metrics['relative_metrics']['beta']:.2f}")

# 📄 生成包含基准的报告
analyzer.generate_report(
    returns, 
    benchmark, 
    title="📊 我的投资组合 vs 沪深300"
)
```
</details>

## 🔧 核心功能 Core Features

### 🎯 QuantAnalysis 类

<table>
<tr>
<td><strong>参数配置</strong></td>
<td><strong>说明</strong></td>
</tr>
<tr>
<td>

```python
analyzer = QuantAnalysis(
    risk_free_rate=0.03,    # 无风险收益率
    benchmark=None,         # 基准数据
    periods_per_year=252,   # 年化周期
    language='zh',          # 语言设置
    compounded=True         # 复利计算
)
```

</td>
<td>

- 🏦 **无风险收益率**: 通常使用国债收益率
- 📊 **基准设置**: 支持自定义基准指数
- 📅 **年化周期**: 股票252天，债券365天
- 🌐 **多语言**: 支持中英文界面
- 💹 **复利模式**: 更准确的收益计算

</td>
</tr>
</table>

### 🛠️ 核心方法

| 方法 | 功能描述 | 返回类型 |
|------|----------|----------|
| `analyze()` | 🔍 综合分析，返回所有指标字典 | `Dict` |
| `generate_report()` | 📋 生成完整的HTML分析报告 | `None/HTML` |

**方法详细说明：**

- **`analyze(returns, benchmark=None)`**: 返回包含所有量化指标的字典，支持基准比较
- **`generate_report(returns, benchmark=None, title=None, output=None)`**: 生成并显示/保存HTML报告

### 📈 支持的指标体系

<details>
<summary><strong>📊 收益指标 Return Metrics</strong></summary>

- 📈 **总收益** (Total Return)
- 💰 **复合年增长率** (CAGR)  
- 📊 **平均收益** (Mean Return)
- 📐 **偏度** (Skewness)
- 📏 **峰度** (Kurtosis)

</details>

<details>
<summary><strong>⚠️ 风险指标 Risk Metrics</strong></summary>

- 📉 **波动率** (Volatility)
- 🔻 **最大回撤** (Max Drawdown)
- 💸 **风险价值** (VaR 95%, 99%)
- 🚨 **条件风险价值** (CVaR)
- 🩸 **溃疡指数** (Ulcer Index)

</details>

<details>
<summary><strong>🎯 绩效指标 Performance Metrics</strong></summary>

- ⭐ **夏普比率** (Sharpe Ratio)
- 🎭 **索提诺比率** (Sortino Ratio)  
- 📐 **卡玛比率** (Calmar Ratio)
- 🔄 **欧米茄比率** (Omega Ratio)

</details>

<details>
<summary><strong>🔍 相对指标 Relative Metrics</strong> (需要基准)</summary>

- 🔺 **阿尔法** (Alpha)
- 📈 **贝塔** (Beta)
- 📊 **信息比率** (Information Ratio)
- 📏 **跟踪误差** (Tracking Error)

</details>

## 🔬 高级用法 Advanced Usage

### ⚙️ 自定义配置

<details>
<summary>点击查看高级配置选项</summary>

```python
# 🎛️ 创建自定义分析器
analyzer = QuantAnalysis(
    risk_free_rate=0.025,       # 2.5% 无风险收益率
    periods_per_year=365,       # 使用日历日 (债券/外汇)
    language='en',              # 英文界面
    compounded=False            # 简单收益计算
)

# 📄 生成英文报告
report_html = analyzer.generate_report(
    returns, 
    title="📊 Portfolio Analysis Report",
    output='html'               # 返回HTML字符串而非显示
)
```
</details>

### 🔄 批量分析工作流

```python
# 📁 多投资组合批量分析
portfolios = {
    '🛡️ Conservative': conservative_returns,
    '🚀 Aggressive': aggressive_returns,  
    '⚖️ Balanced': balanced_returns
}

results = {}
for name, portfolio_returns in portfolios.items():
    print(f"\n📊 {name} Portfolio Analysis")
    metrics = analyzer.analyze(portfolio_returns)
    
    # 提取关键指标
    results[name] = {
        'sharpe': metrics['performance_metrics']['sharpe'],
        'max_dd': metrics['risk_metrics']['max_drawdown'],
        'cagr': metrics['return_metrics']['cagr']
    }
    
    print(f"⭐ Sharpe: {results[name]['sharpe']:.2f}")
    print(f"📉 Max DD: {results[name]['max_dd']:.2%}")
    print(f"💰 CAGR: {results[name]['cagr']:.2%}")
    
    # 📄 为每个组合生成独立报告
    analyzer.generate_report(
        portfolio_returns, 
        title=f"{name} Portfolio Report"
    )

# 📋 结果对比表格
import pandas as pd
comparison_df = pd.DataFrame(results).T
print("\n📊 投资组合对比")
print(comparison_df.round(3))
```

### 📄 报告定制选项

```python
# 📊 生成自定义HTML报告
analyzer.generate_report(
    returns,
    benchmark=benchmark,
    title="📈 我的量化策略分析报告",
    output='save'                        # 保存到文件而非显示
)

# 🌐 英文报告
analyzer_en = QuantAnalysis(language='en')
analyzer_en.generate_report(
    returns,
    title="Portfolio Performance Report"
)
```

## 🛠️ 开发指南 Development

<details>
<summary><strong>🔧 环境设置</strong></summary>

```bash
# 📥 克隆项目
git clone https://github.com/yourusername/quantanalysis.git
cd quantanalysis

# 🐍 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 📦 安装开发依赖
pip install -e ".[dev]"
```
</details>

<details>
<summary><strong>🧪 测试与质量</strong></summary>

```bash
# 🧪 运行测试套件
pytest tests/ -v --cov=quantanalysis

# 🎨 代码格式化
black src/
isort src/
flake8 src/

# 📝 类型检查
mypy src/quantanalysis
```
</details>

---

## 📄 许可证 License

```
Apache License 2.0 - 详见 LICENSE 文件
```

## 🤝 贡献指南 Contributing

我们欢迎各种形式的贡献！

- 🐛 **Bug报告**: 通过 [Issues](https://github.com/yourusername/quantanalysis/issues) 报告
- 💡 **功能建议**: 提交功能请求和改进建议  
- 🔧 **代码贡献**: 提交 Pull Request
- 📖 **文档改进**: 帮助完善文档

## 🙏 致谢 Acknowledgments

本项目基于 [**QuantStats**](https://github.com/ranaroussi/quantstats) 重构开发，感谢原作者 Ran Aroussi 的优秀工作。

---

<div align="center">

## 📈 更新日志 Changelog

| 版本 | 发布日期 | 主要更新 |
|------|----------|----------|
| **v0.1.0** | `2024-01` | 🎉 初始版本发布 |
| | | ✨ 面向对象设计重构 |
| | | 🇨🇳 中文语言支持 |
| | | 📄 HTML 报告生成 |
| | | ⚙️ 可配置参数支持 |

</div>

---

<div align="center">
  <p>
    <strong>Made with ❤️ for the quant community</strong><br>
    <sub>如果这个项目对您有帮助，请考虑给它一个 ⭐</sub>
  </p>
</div>