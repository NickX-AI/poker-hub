"""
打包脚本，用于将 poker_gui.py 转换为 Windows 可执行文件
使用方法：
1. 安装 PyInstaller: pip install pyinstaller
2. 运行此脚本: python poker_gui_exe.py
"""

import os
import subprocess
import sys

def create_executable():
    print("开始打包扑克手牌解析工具...")
    
    # 检查是否安装了 PyInstaller
    try:
        import PyInstaller
        print("已检测到 PyInstaller")
    except ImportError:
        print("未检测到 PyInstaller，正在安装...")
        subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 确保 poker_hand_parser_ok.py 在当前目录
    if not os.path.exists("poker_hand_parser_ok.py"):
        print("错误: 未找到 poker_hand_parser_ok.py 文件")
        print("请确保 poker_hand_parser_ok.py 与 poker_gui.py 在同一目录下")
        return
    
    # 打包命令
    cmd = [
        "pyinstaller",
        "--name=扑克手牌解析工具",
        "--windowed",  # 不显示控制台窗口
        "--onefile",   # 打包成单个可执行文件
        "--add-data=poker_hand_parser_ok.py;.",  # 添加解析器文件
        "poker_gui.py"
    ]
    
    # 执行打包命令
    print("正在打包...")
    subprocess.call(cmd)
    
    print("\n打包完成！")
    print("可执行文件位于 dist 目录中")
    print("文件名: 扑克手牌解析工具.exe")
    print("\n如果运行时出现错误，请尝试使用以下命令重新打包:")
    print("pyinstaller --name=扑克手牌解析工具 --windowed --onefile --hidden-import=tkinter --add-data=poker_hand_parser_ok.py;. poker_gui.py")

if __name__ == "__main__":
    create_executable() 