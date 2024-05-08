import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox
import serial
import pandas as pd
import webbrowser

def check_uid():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        uid = line
        if uid in df['UID'].values:
            display_message(f"车牌: {uid} 匹配成功", "green")
            ser.write(b'rotate_servo')  # 给Arduino发送旋转指令
        else:
            display_message(f"UID: {uid} 没有匹配", "red")
            open_registration_page()
    
    window.after(100, check_uid)

def display_message(message, color):
    msg_label.config(text=message, foreground=color)

def open_registration_page():
    if messagebox.askyesno("提示", "UID 没有匹配，是否需要打开注册页面？"):
        webbrowser.open(url)

ser = serial.Serial('COM6', 9600, timeout=1)
ser.flush()

df = pd.read_csv('Student.csv')
url = 'http://127.0.0.1/phpmyadmin/work/index.html'  # url链接

# 创建GUI窗口
window = tk.Tk()
window.geometry("300x200")  # 窗口大小
window.title("车牌验证系统")

# 创建一个标签，指示程序正在监听和验证UID
label = ttk.Label(window, text="正在验证车牌，请等待...", font=("Arial", 12))
label.pack(pady=20)

# 创建一个标签，用于显示验证结果
msg_label = ttk.Label(window, text="", font=("Arial", 12))
msg_label.pack(pady=20)

# 在窗口创建后立即开始验证流程
window.after(100, check_uid)

# 主循环
st = ttk.Style()
st.configure("TLabel", background="black")  # 改变窗口背景颜色
window.mainloop()