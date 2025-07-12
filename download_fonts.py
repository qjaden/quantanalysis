#!/usr/bin/env python
"""下载中文字体文件的辅助脚本"""

import os
import urllib.request
import sys
from pathlib import Path


def download_font():
    """下载开源中文字体"""
    
    # 字体目录
    fonts_dir = Path(__file__).parent / "src" / "quantanalysis" / "fonts"
    fonts_dir.mkdir(exist_ok=True)
    
    print("=== QuantAnalysis 字体下载工具 ===\n")
    
    # 文泉驿正黑字体下载链接（开源字体）
    font_url = "https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf"
    font_file = fonts_dir / "SourceHanSansSC-Regular.otf"
    
    try:
        print("正在下载思源黑体字体...")
        print(f"下载URL: {font_url}")
        print(f"保存位置: {font_file}")
        
        # 下载字体文件
        urllib.request.urlretrieve(font_url, font_file)
        
        print(f"✅ 字体下载成功: {font_file}")
        print(f"文件大小: {font_file.stat().st_size / 1024 / 1024:.1f} MB")
        
        # 创建SimHei.ttf的符号链接
        simhei_link = fonts_dir / "SimHei.ttf"
        if not simhei_link.exists():
            try:
                os.symlink(font_file.name, simhei_link)
                print(f"✅ 创建符号链接: {simhei_link}")
            except:
                # 如果符号链接失败，复制文件
                import shutil
                shutil.copy2(font_file, simhei_link)
                print(f"✅ 复制字体文件: {simhei_link}")
        
        print("\n🎉 字体安装完成！")
        print("现在可以运行 python simple_example.py 来测试中文字体显示。")
        
    except Exception as e:
        print(f"❌ 字体下载失败: {e}")
        print("\n📋 手动安装说明:")
        print("1. 请手动下载中文字体文件（如SimHei.ttf）")
        print(f"2. 将字体文件放置到: {fonts_dir}")
        print("3. 支持的字体文件名:")
        print("   - SimHei.ttf (黑体)")
        print("   - microsoft-yahei.ttf (微软雅黑)")
        print("   - wqy-zenhei.ttc (文泉驿正黑)")
        
        return False
    
    return True


def check_fonts():
    """检查字体文件是否存在"""
    fonts_dir = Path(__file__).parent / "src" / "quantanalysis" / "fonts"
    
    print("=== 字体文件检查 ===")
    
    font_files = [
        "SimHei.ttf",
        "microsoft-yahei.ttf", 
        "wqy-zenhei.ttc",
        "SourceHanSansSC-Regular.otf"
    ]
    
    found_fonts = []
    for font_file in font_files:
        font_path = fonts_dir / font_file
        if font_path.exists():
            size_mb = font_path.stat().st_size / 1024 / 1024
            print(f"✅ {font_file} ({size_mb:.1f} MB)")
            found_fonts.append(font_file)
        else:
            print(f"❌ {font_file} (未找到)")
    
    if found_fonts:
        print(f"\n共找到 {len(found_fonts)} 个字体文件。")
        print("中文字体显示应该正常工作。")
    else:
        print("\n未找到任何字体文件。")
        print("请运行: python download_fonts.py")
    
    return len(found_fonts) > 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_fonts()
    else:
        if download_font():
            print("\n运行字体检查...")
            check_fonts()