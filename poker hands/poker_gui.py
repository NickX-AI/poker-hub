import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
from poker_hand_parser import PokerHandParser

class PokerHandProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("扑克手牌解析工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入文件部分
        self.input_frame = ttk.LabelFrame(self.main_frame, text="输入文件", padding="10")
        self.input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 输入文件列表
        self.input_files = []
        self.input_listbox = tk.Listbox(self.input_frame, width=70, height=10)
        self.input_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        self.scrollbar = ttk.Scrollbar(self.input_frame, orient=tk.VERTICAL, command=self.input_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.input_listbox.config(yscrollcommand=self.scrollbar.set)
        
        # 按钮框架
        self.button_frame = ttk.Frame(self.input_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # 添加文件按钮
        self.add_button = ttk.Button(self.button_frame, text="添加文件", command=self.add_files)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        # 添加文件夹按钮
        self.add_folder_button = ttk.Button(self.button_frame, text="添加文件夹", command=self.add_folder)
        self.add_folder_button.pack(side=tk.LEFT, padx=5)
        
        # 清除按钮
        self.clear_button = ttk.Button(self.button_frame, text="清除列表", command=self.clear_files)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 输出文件部分
        self.output_frame = ttk.LabelFrame(self.main_frame, text="输出文件", padding="10")
        self.output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 输出文件路径
        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path_var, width=70)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 浏览按钮
        self.browse_button = ttk.Button(self.output_frame, text="浏览...", command=self.browse_output)
        self.browse_button.pack(side=tk.RIGHT, padx=5)
        
        # 处理按钮
        self.process_button = ttk.Button(self.main_frame, text="开始处理", command=self.process_files)
        self.process_button.pack(pady=10)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # 日志框架
        self.log_frame = ttk.LabelFrame(self.main_frame, text="处理日志", padding="10")
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 日志文本框
        self.log_text = tk.Text(self.log_frame, width=70, height=10, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 日志滚动条
        self.log_scrollbar = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
    
    def add_files(self):
        """添加文件到列表"""
        files = filedialog.askopenfilenames(
            title="选择扑克手牌文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if files:
            for file in files:
                if file not in self.input_files:
                    self.input_files.append(file)
                    self.input_listbox.insert(tk.END, file)
    
    def add_folder(self):
        """添加文件夹中的所有txt文件"""
        folder = filedialog.askdirectory(title="选择包含扑克手牌文件的文件夹")
        if folder:
            try:
                for file in os.listdir(folder):
                    if file.endswith(".txt"):
                        full_path = os.path.join(folder, file)
                        if full_path not in self.input_files:
                            self.input_files.append(full_path)
                            self.input_listbox.insert(tk.END, full_path)
            except Exception as e:
                messagebox.showerror("错误", f"读取文件夹时出错: {str(e)}")
    
    def clear_files(self):
        """清除文件列表"""
        self.input_files = []
        self.input_listbox.delete(0, tk.END)
    
    def browse_output(self):
        """选择输出文件路径"""
        file = filedialog.asksaveasfilename(
            title="保存结果文件",
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        if file:
            self.output_path_var.set(file)
    
    def log(self, message):
        """添加日志消息"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def process_files(self):
        """处理所有选择的文件"""
        if not self.input_files:
            messagebox.showwarning("警告", "请先添加输入文件")
            return
        
        output_file = self.output_path_var.get()
        if not output_file:
            messagebox.showwarning("警告", "请选择输出文件路径")
            return
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        try:
            # 禁用按钮
            self.add_button.config(state=tk.DISABLED)
            self.add_folder_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.DISABLED)
            self.browse_button.config(state=tk.DISABLED)
            self.process_button.config(state=tk.DISABLED)
            
            # 开始处理
            parser = PokerHandParser()
            all_hands = []
            total_files = len(self.input_files)
            
            for i, input_file in enumerate(self.input_files):
                self.log(f"\n处理文件: {input_file}")
                current_hand = []
                
                try:
                    with open(input_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                current_hand.append(line)
                            elif current_hand:
                                hand_text = ''.join(current_hand)
                                self.log("处理新的手牌...")
                                try:
                                    hand_data = parser.parse_hand(hand_text)
                                    # 添加 BB 单位到所有底池值
                                    for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
                                        if isinstance(hand_data[key], (int, float)) and hand_data[key] > 0:
                                            hand_data[key] = f"{hand_data[key]}BB"
                                        elif isinstance(hand_data[key], (int, float)):
                                            hand_data[key] = "0BB"
                                    all_hands.append(hand_data)
                                except ZeroDivisionError:
                                    self.log(f"错误: BB值为零，无法处理该手牌")
                                except Exception as e:
                                    self.log(f"处理手牌时出错: {str(e)}")
                                current_hand = []
                    
                    # 处理最后一手牌（如果存在）
                    if current_hand:
                        hand_text = ''.join(current_hand)
                        self.log("处理最后一手牌...")
                        try:
                            hand_data = parser.parse_hand(hand_text)
                            # 添加 BB 单位到所有底池值
                            for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
                                if isinstance(hand_data[key], (int, float)) and hand_data[key] > 0:
                                    hand_data[key] = f"{hand_data[key]}BB"
                                elif isinstance(hand_data[key], (int, float)):
                                    hand_data[key] = "0BB"
                            all_hands.append(hand_data)
                        except ZeroDivisionError:
                            self.log(f"错误: BB值为零，无法处理该手牌")
                        except Exception as e:
                            self.log(f"处理最后一手牌时出错: {str(e)}")
                except Exception as e:
                    self.log(f"处理文件 {input_file} 时出错: {str(e)}")
                
                # 更新进度条
                progress = (i + 1) / total_files * 100
                self.progress_var.set(progress)
                self.root.update()
            
            self.log(f"\n总共处理了 {len(all_hands)} 手牌")
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 写入CSV文件
            if all_hands:
                fieldnames = list(all_hands[0].keys())
                # 创建自定义标题映射
                custom_headers = {
                    'result': 'Result(Hero)',
                    'total_pot': 'Total_Pot',
                    'preflop_pot': 'Preflop_Pot',
                    'flop_pot': 'Flop_Pot',
                    'turn_pot': 'Turn_Pot',
                    'river_pot': 'River_Pot',
                    'preflop_line1': 'Preflop_Line1',
                    'preflop_line2': 'Preflop_Line2',
                    'preflop_line3': 'Preflop_Line3',
                    'SB_BB': 'SB/BB',
                    'cash_drop': 'Cash_Drop'
                }
                
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    # 写入自定义标题
                    header_row = {field: custom_headers.get(field, field) for field in fieldnames}
                    writer.writerow(header_row)
                    writer.writerows(all_hands)
                    self.log(f"数据已写入 {output_file}")
                
                messagebox.showinfo("成功", f"已成功处理 {len(all_hands)} 手牌并保存到 {output_file}")
            else:
                self.log("没有找到任何手牌数据")
                messagebox.showwarning("警告", "没有找到任何手牌数据")
        
        except Exception as e:
            self.log(f"处理过程中出错: {str(e)}")
            messagebox.showerror("错误", f"处理过程中出错: {str(e)}")
        
        finally:
            # 重新启用按钮
            self.add_button.config(state=tk.NORMAL)
            self.add_folder_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)
            self.process_button.config(state=tk.NORMAL)
            # 重置进度条
            self.progress_var.set(0)

def main():
    try:
        root = tk.Tk()
        app = PokerHandProcessorGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"启动应用程序时出错: {str(e)}")
        input("按Enter键退出...")

if __name__ == "__main__":
    main() 