"""简化的HTML报告生成模块"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from datetime import datetime
import base64
import io
import os
from typing import Dict, Any, Optional

from . import stats
from .i18n import t, get_language, set_language


def generate_html_report(
    returns: pd.Series,
    benchmark: Optional[pd.Series],
    metrics: Dict[str, Any],
    title: str,
    language: str = "zh",
    config: Optional[Dict[str, Any]] = None,
    returns_freq: str = "M"
) -> str:
    """生成完整的HTML报告文件
    
    Args:
        returns: 投资组合收益率序列
        benchmark: 基准收益率序列
        metrics: 分析指标字典
        title: 报告标题
        language: 语言设置
        config: 配置参数
        returns_freq: 收益率柱状图频率 ('D'=日频, 'W'=周频, 'M'=月频)
        
    Returns:
        生成的HTML文件路径
    """
    config = config or {}
    
    # 确保当前上下文中的语言设置正确
    set_language(language)
    
    # 生成图表
    charts_base64 = _generate_charts(returns, benchmark, language, returns_freq)
    
    # 生成HTML内容
    html_content = _create_html_content(
        returns, benchmark, metrics, title, language, charts_base64
    )
    
    # 保存文件
    filename = f"portfolio_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename


def _setup_chinese_fonts():
    """配置中文字体"""
    # 获取项目字体目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(current_dir, 'fonts')
    
    # 项目内的字体文件列表
    project_fonts = [
        ('SimHei.otf', 'SimHei'),
        ('SimHei.ttf', 'SimHei'),
        ('microsoft-yahei.ttf', 'Microsoft YaHei'),
        ('msyh.ttc', 'Microsoft YaHei'),
        ('simhei.ttf', 'SimHei')
    ]
    
    # 首先尝试加载项目内的字体文件
    font_loaded = False
    if os.path.exists(fonts_dir):
        for font_file, _ in project_fonts:
            font_path = os.path.join(fonts_dir, font_file)
            if os.path.exists(font_path):
                try:
                    # 注册字体
                    from matplotlib.font_manager import FontProperties, fontManager
                    fontManager.addfont(font_path)
                    
                    # 重建字体缓存
                    fontManager._load_fontmanager(try_read_cache=False)
                    
                    # 使用字体名称而不是字体文件名
                    if 'SimHei' in font_file or 'simhei' in font_file.lower():
                        font_name = 'SimHei'
                    elif 'yahei' in font_file.lower() or 'msyh' in font_file:
                        font_name = 'Microsoft YaHei'
                    else:
                        # 尝试从字体文件获取字体名称
                        prop = FontProperties(fname=font_path)
                        font_name = prop.get_name()
                    
                    
                    plt.rcParams['font.sans-serif'] = [font_name] + plt.rcParams['font.sans-serif']
                    
                    # 测试字体是否可用
                    fig, ax = plt.subplots(figsize=(1, 1))
                    ax.text(0.5, 0.5, '测试', fontsize=12)
                    plt.close(fig)
                    font_loaded = True
                    break
                except Exception as e:
                    continue
    
    # 如果项目字体加载失败，尝试系统字体
    if not font_loaded:
        system_fonts = [
            'SimHei',           # 黑体
            'Microsoft YaHei',  # 微软雅黑
            'PingFang SC',      # Mac字体
            'Hiragino Sans GB', # Mac字体
            'DejaVu Sans',      # 后备字体
            'Arial Unicode MS'  # 通用字体
        ]
        
        for font in system_fonts:
            try:
                plt.rcParams['font.sans-serif'] = [font]
                # 测试字体是否可用
                fig, ax = plt.subplots(figsize=(1, 1))
                ax.text(0.5, 0.5, '测试', fontsize=12)
                plt.close(fig)
                font_loaded = True
                break
            except:
                continue
    
    # 设置负号正常显示
    plt.rcParams['axes.unicode_minus'] = False
    
    # 如果都失败了，设置警告抑制
    if not font_loaded:
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib.font_manager')
        warnings.filterwarnings('ignore', message='Glyph .* missing from font.*')
        warnings.filterwarnings('ignore', message='findfont: Generic family .* not found.*')


def _generate_charts(returns: pd.Series, benchmark: Optional[pd.Series], language: str, returns_freq: str = "M") -> str:
    """生成所有图表并返回base64编码"""
    
    # 设置图表样式 - Apple风格的现代化设计
    plt.style.use('default')
    _setup_chinese_fonts()
    
    # Apple风格配色方案
    colors = {
        'primary': '#007AFF',      # Apple蓝
        'secondary': '#34C759',    # Apple绿  
        'tertiary': '#FF3B30',     # Apple红
        'quaternary': '#FF9500',   # Apple橙
        'text': '#1D1D1F',         # Apple深灰
        'grid': '#F2F2F7',         # Apple浅灰
        'background': '#FFFFFF'     # 白色背景
    }
    
    # 创建子图 - 使用Apple风格的布局，上面2x2，下面1x2
    from matplotlib.gridspec import GridSpec
    fig = plt.figure(figsize=(16, 15))
    fig.patch.set_facecolor(colors['background'])
    
    # 创建网格：3行2列，其中最后一行的图占据2列
    gs = GridSpec(3, 2, figure=fig, height_ratios=[1, 1, 1], hspace=0.4, wspace=0.3)
    
    # 设置全局字体大小和样式
    plt.rcParams.update({
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 11,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'axes.titleweight': 'normal',
        'figure.titleweight': 'normal',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linewidth': 0.5
    })
    
    # Get labels from i18n
    labels = {
        'cumulative_returns': t('charts.cumulative_returns'),
        'drawdown': t('charts.drawdown'), 
        'monthly_heatmap': t('charts.monthly_heatmap'),
        'return_distribution': t('charts.return_distribution'),
        'returns_bar': t('charts.returns_bar'),
        'portfolio': t('common.portfolio'),
        'benchmark': t('common.benchmark'),
        'drawdown_label': t('charts.drawdown_label'),
        'daily_return': t('charts.daily_return'),
        'frequency': t('charts.frequency'),
        'mean': t('charts.mean')
    }
    
    # 频率标签
    freq_labels = {
        'D': t('charts.daily_returns'),
        'W': t('charts.weekly_returns'), 
        'M': t('charts.monthly_returns')
    }
    
    # 1. 累计收益图 - Apple风格 (左上)
    ax1 = fig.add_subplot(gs[0, 0])
    cum_returns = (1 + returns).cumprod()
    ax1.plot(cum_returns.index, cum_returns.values, 
             label=labels['portfolio'], linewidth=2, color=colors['primary'])
    
    if benchmark is not None:
        cum_benchmark = (1 + benchmark).cumprod()
        ax1.plot(cum_benchmark.index, cum_benchmark.values,
                 label=labels['benchmark'], linewidth=2, color=colors['tertiary'], alpha=0.8)
    
    ax1.set_title(labels['cumulative_returns'], fontsize=14, fontweight='normal', pad=20, color=colors['text'])
    ax1.legend(loc='upper left', fontsize=10, frameon=False)
    ax1.grid(True, alpha=0.2, color=colors['grid'])
    ax1.set_facecolor(colors['background'])
    ax1.spines['left'].set_color('#D1D1D6')
    ax1.spines['bottom'].set_color('#D1D1D6')
    ax1.tick_params(colors=colors['text'])
    
    # 2. 回撤图 - Apple风格 (右上)
    ax2 = fig.add_subplot(gs[0, 1])
    drawdown = stats.to_drawdown_series(returns)
    ax2.fill_between(drawdown.index, drawdown.values, 0, 
                     alpha=0.3, color=colors['tertiary'], label=labels['drawdown_label'])
    ax2.plot(drawdown.index, drawdown.values, color=colors['tertiary'], linewidth=1.5)
    
    # 标记最大回撤点
    max_dd_idx = drawdown.idxmin()
    max_dd_val = drawdown.min()
    ax2.plot(max_dd_idx, max_dd_val, 'o', markersize=6, markerfacecolor=colors['tertiary'], 
             markeredgecolor='white', markeredgewidth=2)
    
    ax2.set_title(labels['drawdown'], fontsize=14, fontweight='normal', pad=20, color=colors['text'])
    ax2.grid(True, alpha=0.2, color=colors['grid'])
    ax2.set_facecolor(colors['background'])
    ax2.spines['left'].set_color('#D1D1D6')
    ax2.spines['bottom'].set_color('#D1D1D6')
    ax2.tick_params(colors=colors['text'])
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
    
    # 3. 月度收益热力图 - Apple风格 (左下)
    ax3 = fig.add_subplot(gs[1, 0])
    try:
        monthly_returns = returns.resample('ME').apply(lambda x: (1 + x).prod() - 1)
        
        # 创建年月表格
        monthly_data = []
        years = sorted(monthly_returns.index.year.unique())
        months = range(1, 13)
        
        for year in years:
            year_data = []
            for month in months:
                try:
                    value = monthly_returns[
                        (monthly_returns.index.year == year) & 
                        (monthly_returns.index.month == month)
                    ].iloc[0]
                    year_data.append(value)
                except:
                    year_data.append(np.nan)
            monthly_data.append(year_data)
        
        if monthly_data:
            # 使用Apple风格的颜色映射
            from matplotlib.colors import LinearSegmentedColormap
            apple_colors = ['#FF3B30', '#FFFFFF', '#34C759']  # 红-白-绿
            apple_cmap = LinearSegmentedColormap.from_list('apple', apple_colors, N=256)
            im = ax3.imshow(monthly_data, cmap=apple_cmap, aspect='auto', vmin=-0.1, vmax=0.1)
            
            # 添加数值标注 - Apple风格
            for i in range(len(years)):
                for j in range(12):
                    if not np.isnan(monthly_data[i][j]):
                        text_color = colors['text'] if abs(monthly_data[i][j]) < 0.03 else 'white'
                        ax3.text(j, i, f'{monthly_data[i][j]:.1%}', 
                               ha='center', va='center', fontsize=8, color=text_color, fontweight='500')
            
            ax3.set_xticks(range(12))
            ax3.set_xticklabels(t('months.short'))
            ax3.set_yticks(range(len(years)))
            ax3.set_yticklabels(years)
            ax3.tick_params(colors=colors['text'])
            
            # 添加色彩条
            cbar = plt.colorbar(im, ax=ax3, shrink=0.8, format=plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
            cbar.ax.tick_params(colors=colors['text'])
    except:
        ax3.text(0.5, 0.5, t('report.insufficient_data'), 
                ha='center', va='center', transform=ax3.transAxes, fontsize=12, color=colors['text'])
    
    ax3.set_title(labels['monthly_heatmap'], fontsize=14, fontweight='normal', pad=20, color=colors['text'])
    ax3.set_facecolor(colors['background'])
    
    # 4. 收益率分布直方图 - Apple风格 (右下)
    ax4 = fig.add_subplot(gs[1, 1])
    n_bins = min(50, len(returns) // 10)
    _, bins, patches = ax4.hist(returns.values, bins=n_bins, alpha=0.7, 
                               color=colors['primary'], edgecolor='white', linewidth=0.5)
    
    # 着色（正负收益不同颜色）
    for i, p in enumerate(patches):
        if bins[i] < 0:
            p.set_facecolor(colors['tertiary'])
            p.set_alpha(0.6)
        else:
            p.set_facecolor(colors['secondary'])
            p.set_alpha(0.6)
    
    # 添加均值线
    mean_return = returns.mean()
    ax4.axvline(mean_return, color=colors['text'], linestyle='--', linewidth=2, alpha=0.8,
               label=f"{labels['mean']}: {mean_return:.3%}")
    
    ax4.set_title(labels['return_distribution'], fontsize=14, fontweight='normal', pad=20, color=colors['text'])
    ax4.set_xlabel(labels['daily_return'], fontsize=11, color=colors['text'])
    ax4.set_ylabel(labels['frequency'], fontsize=11, color=colors['text'])
    ax4.legend(fontsize=10, frameon=False)
    ax4.grid(True, alpha=0.2, color=colors['grid'])
    ax4.set_facecolor(colors['background'])
    ax4.spines['left'].set_color('#D1D1D6')
    ax4.spines['bottom'].set_color('#D1D1D6')
    ax4.tick_params(colors=colors['text'])
    ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
    
    # 5. 收益率柱状图 - 新增 (底部，占据两列)
    ax5 = fig.add_subplot(gs[2, :])
    _create_returns_bar_chart(ax5, returns, returns_freq, freq_labels, colors, language)
    
    # 调整布局 - 使用subplots_adjust替代tight_layout以避免GridSpec冲突
    plt.subplots_adjust(left=0.08, right=0.95, top=0.93, bottom=0.08)
    
    # 转换为base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    
    return chart_base64


def _create_returns_bar_chart(ax, returns: pd.Series, freq: str, freq_labels: dict, colors: dict, language: str):
    """创建收益率柱状图"""
    try:
        # 根据频率重采样数据
        if freq == 'D':
            # 日频：显示所有数据
            resampled_returns = returns
            # 根据数据跨度选择合适的日期格式
            data_span_days = (returns.index[-1] - returns.index[0]).days
            if data_span_days > 365:
                # 超过一年的数据，显示年-月
                date_format = '%Y-%m' if language == 'zh' else '%Y-%m'
            else:
                # 一年内的数据，显示月-日
                date_format = '%m-%d' if language == 'zh' else '%m-%d'
        elif freq == 'W':
            # 周频：每周最后一个交易日
            resampled_returns = returns.resample('W').apply(lambda x: (1 + x).prod() - 1)
            resampled_returns = resampled_returns.tail(52)  # 最近52周
            date_format = '%m-%d' if language == 'zh' else '%m-%d'
        else:  # 'M'
            # 月频：每月最后一个交易日  
            resampled_returns = returns.resample('ME').apply(lambda x: (1 + x).prod() - 1)
            resampled_returns = resampled_returns.tail(24)  # 最近24个月
            date_format = '%Y-%m' if language == 'zh' else '%Y-%m'
        
        # 创建柱状图
        bars = ax.bar(range(len(resampled_returns)), resampled_returns.values, 
                     width=0.8, alpha=0.8)
        
        # 根据正负值着色
        for i, (bar, value) in enumerate(zip(bars, resampled_returns.values)):
            if value >= 0:
                bar.set_color(colors['secondary'])  # 绿色表示正收益
            else:
                bar.set_color(colors['tertiary'])   # 红色表示负收益
        
        # 设置X轴标签 - 智能间隔算法
        data_length = len(resampled_returns)
        if data_length <= 30:
            # 数据点很少时，显示所有标签
            step = 1
        elif data_length <= 100:
            # 中等数据量，每5个显示一个
            step = max(1, data_length // 20)
        elif data_length <= 500:
            # 较多数据，每10-15个显示一个
            step = max(1, data_length // 15)
        else:
            # 大量数据，每20-30个显示一个
            step = max(1, data_length // 20)
        
        x_labels = [date.strftime(date_format) for date in resampled_returns.index[::step]]
        ax.set_xticks(range(0, len(resampled_returns), step))
        ax.set_xticklabels(x_labels, rotation=45, ha='right')
        
        # 添加零基准线
        ax.axhline(y=0, color=colors['text'], linestyle='-', alpha=0.3, linewidth=1)
        
        # 设置标题和样式
        title = freq_labels.get(freq, freq_labels['M'])
        ax.set_title(title, fontsize=14, fontweight='normal', pad=20, color=colors['text'])
        ax.set_ylabel('收益率' if language == 'zh' else 'Returns', fontsize=11, color=colors['text'])
        
        # 格式化Y轴为百分比
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
        
        # 应用Apple风格
        ax.grid(True, alpha=0.2, color=colors['grid'])
        ax.set_facecolor(colors['background'])
        ax.spines['left'].set_color('#D1D1D6')
        ax.spines['bottom'].set_color('#D1D1D6')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors=colors['text'])
        
    except Exception as e:
        # 如果出错，显示错误信息
        ax.text(0.5, 0.5, f'{t("report.data_error")}: {str(e)}', 
                ha='center', va='center', transform=ax.transAxes, fontsize=12, color=colors['text'])
        ax.set_title(freq_labels.get(freq, freq_labels['M']), fontsize=14, fontweight='normal', pad=20, color=colors['text'])


def _create_html_content(
    returns: pd.Series, 
    _: Optional[pd.Series], 
    metrics: Dict[str, Any], 
    title: str, 
    language: str, 
    charts_base64: str
) -> str:
    """创建完整的HTML内容"""
    
    # Get translations from i18n system
    translations = {
        'performance_summary': t('categories.performance_summary'),
        'analysis_period': t('report.analysis_period'),
        'generated_on': t('common.generated_on'),
        'total_return': t('metrics.total_return'),
        'cagr': t('metrics.cagr'),
        'sharpe_ratio': t('metrics.sharpe_ratio'),
        'max_drawdown': t('metrics.max_drawdown'),
        'volatility': t('metrics.volatility'),
        'sortino_ratio': t('metrics.sortino_ratio'),
        'detailed_metrics': t('report.detailed_metrics'),
        'metric': t('common.metric'),
        'value': t('common.value'),
        'risk_metrics': t('categories.risk_metrics'),
        'performance_metrics': t('categories.performance_metrics'),
        'chart_analysis': t('report.chart_analysis'),
        'var_95': t('metrics.var_95'),
        'cvar_95': t('metrics.cvar_95'),
        'calmar_ratio': t('metrics.calmar_ratio'),
        'omega_ratio': t('metrics.omega_ratio'),
        'recovery_factor': t('metrics.recovery_factor'),
        'generated_by': t('report.generated_by')
    }
    
    # 计算期间信息
    start_date = returns.index[0].strftime('%Y-%m-%d')
    end_date = returns.index[-1].strftime('%Y-%m-%d')
    trading_days = len(returns)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="{language}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
                line-height: 1.47;
                color: #1d1d1f;
                background: #f5f5f7;
                min-height: 100vh;
                padding: 24px;
                font-weight: 400;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 18px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
                overflow: hidden;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }}
            
            .header {{
                background: #ffffff;
                color: #1d1d1f;
                padding: 48px 48px 32px;
                text-align: center;
                border-bottom: 1px solid rgba(0, 0, 0, 0.08);
            }}
            
            .header h1 {{
                font-size: 2.25rem;
                font-weight: 600;
                margin-bottom: 16px;
                letter-spacing: -0.02em;
                line-height: 1.2;
            }}
            
            .header-info {{
                font-size: 1rem;
                color: #86868b;
                margin-bottom: 8px;
                font-weight: 400;
            }}
            
            .content {{
                padding: 48px;
            }}
            
            .section {{
                margin-bottom: 64px;
            }}
            
            .section h2 {{
                color: #1d1d1f;
                font-size: 1.75rem;
                font-weight: 600;
                margin-bottom: 32px;
                letter-spacing: -0.01em;
                position: relative;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 24px;
                margin-bottom: 32px;
            }}
            
            .metric-card {{
                background: #ffffff;
                padding: 32px 24px;
                border-radius: 16px;
                border: 1px solid rgba(0, 0, 0, 0.06);
                transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                position: relative;
            }}
            
            .metric-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
                border-color: rgba(0, 0, 0, 0.12);
            }}
            
            .metric-card.positive {{
                background: linear-gradient(135deg, #f0f9ff 0%, #f8fafc 100%);
                border-color: rgba(34, 197, 94, 0.2);
            }}
            
            .metric-card.negative {{
                background: linear-gradient(135deg, #fef2f2 0%, #f8fafc 100%);
                border-color: rgba(239, 68, 68, 0.2);
            }}
            
            .metric-title {{
                font-size: 0.875rem;
                color: #86868b;
                margin-bottom: 12px;
                font-weight: 500;
                text-transform: none;
                letter-spacing: 0;
            }}
            
            .metric-value {{
                font-size: 2rem;
                font-weight: 600;
                color: #1d1d1f;
                margin-bottom: 0;
                letter-spacing: -0.02em;
                line-height: 1.1;
            }}
            
            .metric-value.positive {{
                color: #22c55e;
            }}
            
            .metric-value.negative {{
                color: #ef4444;
            }}
            
            .chart-container {{
                text-align: center;
                margin: 32px 0;
                background: #ffffff;
                padding: 32px;
                border-radius: 16px;
                border: 1px solid rgba(0, 0, 0, 0.06);
            }}
            
            .chart-container img {{
                max-width: 100%;
                height: auto;
                border-radius: 12px;
            }}
            
            .metrics-table {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin: 32px 0;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                border: 1px solid rgba(0, 0, 0, 0.06);
            }}
            
            .metrics-table th {{
                background: #f5f5f7;
                color: #1d1d1f;
                padding: 16px 20px;
                text-align: left;
                font-weight: 600;
                font-size: 0.875rem;
                border-bottom: 1px solid rgba(0, 0, 0, 0.06);
            }}
            
            .metrics-table td {{
                padding: 16px 20px;
                border-bottom: 1px solid rgba(0, 0, 0, 0.04);
                font-size: 0.875rem;
                color: #1d1d1f;
            }}
            
            .metrics-table tr:last-child td {{
                border-bottom: none;
            }}
            
            .metrics-table tr:hover {{
                background: #f9f9f9;
                transition: background 0.15s ease;
            }}
            
            .category-header {{
                background: #f5f5f7 !important;
                color: #1d1d1f !important;
                font-weight: 600 !important;
                text-align: center !important;
                font-size: 0.875rem !important;
            }}
            
            .footer {{
                background: #f5f5f7;
                color: #86868b;
                padding: 32px;
                text-align: center;
                border-top: 1px solid rgba(0, 0, 0, 0.06);
            }}
            
            .footer p {{
                margin: 4px 0;
                font-size: 0.875rem;
                font-weight: 400;
            }}
            
            @media (max-width: 768px) {{
                body {{
                    padding: 16px;
                }}
                
                .container {{
                    border-radius: 12px;
                }}
                
                .header {{
                    padding: 32px 24px 24px;
                }}
                
                .header h1 {{
                    font-size: 1.875rem;
                }}
                
                .content {{
                    padding: 32px 24px;
                }}
                
                .section {{
                    margin-bottom: 48px;
                }}
                
                .metrics-grid {{
                    grid-template-columns: 1fr;
                    gap: 16px;
                }}
                
                .chart-container {{
                    padding: 24px 16px;
                }}
                
                .metric-card {{
                    padding: 24px 20px;
                }}
            }}
            
            @media (prefers-color-scheme: dark) {{
                body {{
                    background: #000000;
                    color: #f5f5f7;
                }}
                
                .container {{
                    background: #1d1d1f;
                    border-color: rgba(255, 255, 255, 0.1);
                }}
                
                .header {{
                    background: #1d1d1f;
                    color: #f5f5f7;
                    border-bottom-color: rgba(255, 255, 255, 0.1);
                }}
                
                .section h2 {{
                    color: #f5f5f7;
                }}
                
                .metric-card {{
                    background: #2d2d2d;
                    border-color: rgba(255, 255, 255, 0.1);
                }}
                
                .metric-title {{
                    color: #a1a1a6;
                }}
                
                .metric-value {{
                    color: #f5f5f7;
                }}
                
                .chart-container {{
                    background: #2d2d2d;
                    border-color: rgba(255, 255, 255, 0.1);
                }}
                
                .metrics-table {{
                    background: #2d2d2d;
                    border-color: rgba(255, 255, 255, 0.1);
                }}
                
                .metrics-table th {{
                    background: #3d3d3d;
                    color: #f5f5f7;
                    border-bottom-color: rgba(255, 255, 255, 0.1);
                }}
                
                .metrics-table td {{
                    border-bottom-color: rgba(255, 255, 255, 0.05);
                    color: #f5f5f7;
                }}
                
                .footer {{
                    background: #2d2d2d;
                    color: #a1a1a6;
                    border-top-color: rgba(255, 255, 255, 0.1);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{title}</h1>
                <p class="header-info">{translations['analysis_period']}: {start_date} {t('common.to')} {end_date}</p>
                <p class="header-info">{t('common.trading_days')}: {trading_days} {t('common.days')} | {translations['generated_on']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📊 {translations['performance_summary']}</h2>
                    <div class="metrics-grid">
                        <div class="metric-card {'positive' if metrics['returns_stats']['total_return'] > 0 else 'negative'}">
                            <div class="metric-title">{translations['total_return']}</div>
                            <div class="metric-value {'positive' if metrics['returns_stats']['total_return'] > 0 else 'negative'}">{metrics['returns_stats']['total_return']:.2%}</div>
                        </div>
                        
                        <div class="metric-card {'positive' if metrics['returns_stats']['cagr'] > 0 else 'negative'}">
                            <div class="metric-title">{translations['cagr']}</div>
                            <div class="metric-value {'positive' if metrics['returns_stats']['cagr'] > 0 else 'negative'}">{metrics['returns_stats']['cagr']:.2%}</div>
                        </div>
                        
                        <div class="metric-card {'positive' if metrics['performance_metrics']['sharpe'] > 1 else 'negative' if metrics['performance_metrics']['sharpe'] < 0 else ''}">
                            <div class="metric-title">{translations['sharpe_ratio']}</div>
                            <div class="metric-value">{metrics['performance_metrics']['sharpe']:.3f}</div>
                        </div>
                        
                        <div class="metric-card negative">
                            <div class="metric-title">{translations['max_drawdown']}</div>
                            <div class="metric-value negative">{metrics['risk_metrics']['max_drawdown']:.2%}</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-title">{translations['volatility']}</div>
                            <div class="metric-value">{metrics['risk_metrics']['volatility']:.2%}</div>
                        </div>
                        
                        <div class="metric-card {'positive' if metrics['performance_metrics']['sortino'] > 1 else 'negative' if metrics['performance_metrics']['sortino'] < 0 else ''}">
                            <div class="metric-title">{translations['sortino_ratio']}</div>
                            <div class="metric-value">{metrics['performance_metrics']['sortino']:.3f}</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📈 {translations['chart_analysis']}</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{charts_base64}" alt="{t('common.portfolio')}{t('common.analysis')}{t('charts.cumulative_returns')}">
                    </div>
                </div>
                
                <div class="section">
                    <h2>📋 {translations['detailed_metrics']}</h2>
                    <table class="metrics-table">
                        <thead>
                            <tr>
                                <th>{translations['metric']}</th>
                                <th>{translations['value']}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td colspan="2" class="category-header">{translations['risk_metrics']}</td></tr>
                            <tr><td>{translations['volatility']}</td><td>{metrics['risk_metrics']['volatility']:.2%}</td></tr>
                            <tr><td>{translations['max_drawdown']}</td><td>{metrics['risk_metrics']['max_drawdown']:.2%}</td></tr>
                            <tr><td>{translations['var_95']}</td><td>{metrics['risk_metrics']['var_95']:.3%}</td></tr>
                            <tr><td>{translations['cvar_95']}</td><td>{metrics['risk_metrics']['cvar_95']:.3%}</td></tr>
                            <tr><td>{t('metrics.ulcer_index')}</td><td>{metrics['risk_metrics']['ulcer_index']:.4f}</td></tr>
                            
                            <tr><td colspan="2" class="category-header">{translations['performance_metrics']}</td></tr>
                            <tr><td>{translations['sharpe_ratio']}</td><td>{metrics['performance_metrics']['sharpe']:.3f}</td></tr>
                            <tr><td>{translations['sortino_ratio']}</td><td>{metrics['performance_metrics']['sortino']:.3f}</td></tr>
                            <tr><td>{translations['calmar_ratio']}</td><td>{metrics['performance_metrics']['calmar']:.3f}</td></tr>
                            <tr><td>{translations['omega_ratio']}</td><td>{metrics['performance_metrics']['omega']:.3f}</td></tr>
                            <tr><td>{translations['recovery_factor']}</td><td>{metrics['drawdown_metrics']['recovery_factor']:.3f}</td></tr>
    """
    
    # 如果有基准比较，添加相对指标
    if 'relative_metrics' in metrics:
        html_content += f"""
                            <tr><td colspan="2" class="category-header">{t('categories.relative_metrics')}</td></tr>
                            <tr><td>{t('metrics.excess_return')}</td><td>{metrics['relative_metrics']['excess_return']:.2%}</td></tr>
                            <tr><td>{t('metrics.tracking_error')}</td><td>{metrics['relative_metrics']['tracking_error']:.2%}</td></tr>
                            <tr><td>{t('metrics.information_ratio')}</td><td>{metrics['relative_metrics']['information_ratio']:.3f}</td></tr>
        """
        
        if 'alpha' in metrics['performance_metrics']:
            html_content += f"""
                            <tr><td>{t('metrics.alpha')}</td><td>{metrics['performance_metrics']['alpha']:.3%}</td></tr>
                            <tr><td>{t('metrics.beta')}</td><td>{metrics['performance_metrics']['beta']:.3f}</td></tr>
            """
    
    html_content += f"""
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="footer">
                <p>{translations['generated_by']}</p>
                <p>{translations['generated_on']}: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S' if get_language() == 'zh' else '%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content