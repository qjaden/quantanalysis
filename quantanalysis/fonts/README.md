# 字体文件说明

## 内置字体文件

QuantAnalysis 已内置以下中文字体文件，无需用户额外下载：

- `SimHei.otf` - 黑体字体（推荐）

## 自动检测机制

QuantAnalysis会按以下优先级自动检测和使用字体：

1. **内置字体**: 优先使用项目内置的字体文件
2. **系统字体**: 如果内置字体不可用，自动回退到系统已安装的中文字体
3. **后备字体**: 最后使用默认的后备字体，确保程序正常运行

## 字体兼容性

- **Windows**: 自动识别系统的SimHei、Microsoft YaHei等字体
- **Linux**: 自动回退到系统已安装的中文字体
- **macOS**: 支持Hiragino Sans GB、PingFang SC等系统字体

## 使用说明

安装QuantAnalysis后，中文字体支持即开即用，无需任何额外配置。所有图表和报告都将正确显示中文内容。