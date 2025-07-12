# 字体文件说明

## 字体文件位置

请将以下字体文件放置在此目录：

- `SimHei.ttf` - 黑体字体（推荐）
- `microsoft-yahei.ttf` - 微软雅黑字体
- `wqy-zenhei.ttc` - 文泉驿正黑字体

## 获取字体文件

### Windows系统
从 `C:\Windows\Fonts\` 目录复制以下文件：
- `simhei.ttf` (黑体)
- `msyh.ttc` (微软雅黑)

### Linux系统
安装字体包：
```bash
# Ubuntu/Debian
sudo apt-get install fonts-wqy-zenhei

# CentOS/RHEL
sudo yum install wqy-zenhei-fonts
```

### 在线下载
可以从以下位置下载开源中文字体：
- 文泉驿字体：http://wenq.org/
- 思源黑体：https://github.com/adobe-fonts/source-han-sans

## 使用说明

将字体文件复制到此目录后，QuantAnalysis会自动检测并使用，解决图表中文显示问题。