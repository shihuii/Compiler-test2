import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
import re
from matplotlib import pyplot as plt
from test import func1

# DFA 
def DFA(input_text):
    pass
    #plt.imshow()

# NFA
def NFA(input_text):
    pass
    #plt.imshow()

# Minimize DFA
def Min_DFA(input_text):
    pass
    #plt.imshow()

def submit_button_clicked():
    regex = regex_entry.get()
    option = option_combobox.get()

    # 检查正则表达式是否有效
    try:
        re.compile(regex)
    except re.error:
        messagebox.showerror('Invalid regular expression', 'Invalid regular expression. Please enter a valid one.')
        return

    # 根据选项调用相应的函数
    if option == 'NFA':
        func1()# 这里调用了测试用的那个函数
    elif option == 'DFA':
        DFA(regex)
    elif option == 'Minimized DFA':
        Min_DFA(regex)
    else:
        option = None
        messagebox.showerror('Invalid option', 'Invalid option. Please select NFA, DFA, or Minimized DFA.')
        return

# 创建主窗口
root = tk.Tk()
root.title('Experiment-2')
root.configure(bg='#FFC0CB')  

# 创建布局
frame = ttk.Frame(root, padding='10', style='My.TFrame')
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 创建控件
regex_label = ttk.Label(frame, text='INPUT:', style='My.TLabel')
regex_entry = ttk.Entry(frame, width=30)
option_label = ttk.Label(frame, text='SELECT:', style='My.TLabel')
option_combobox = ttk.Combobox(frame, values=['NFA', 'DFA', 'Minimized DFA'], width=25)
submit_button = ttk.Button(frame, text='Submit', command=submit_button_clicked, style='My.TButton')

# 布局控件
regex_label.grid(column=0, row=0, pady=(10, 10))
regex_entry.grid(column=1, row=0, pady=(10, 10))
option_label.grid(column=0, row=1, pady=(10, 10))
option_combobox.grid(column=1, row=1, pady=(10, 10))
submit_button.grid(column=0, row=2, columnspan=2, pady=(10, 20))


# 定义样式
style = ttk.Style()
style.configure('My.TFrame', background='#FFC0CB')  # 设置Frame背景色
style.configure('My.TLabel', background='#FFC0CB')  # 设置Label背景色
style.configure('My.TButton', background='#FF69B4')  # 设置Button背景色

# 调整窗口大小
root.geometry("350x200")  # 设置宽度为500像素，高度为300像素

# 运行主循环
root.mainloop()
