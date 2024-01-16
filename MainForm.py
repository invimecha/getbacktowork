# for Windows / invimecha.com / 2024

import ctypes
import os
import platform
import string 
import sys
from threading import Thread
from PIL import ImageGrab 
from PIL import Image, ImageTk 
import numpy as nm  
import pytesseract 
import time 
import configparser 
import tkinter as tk
from tkinter import messagebox
import tempfile, base64, zlib 
import pystray
import PIL.Image
import multiprocessing
import threading
from pynput.keyboard import Key, Controller
from pydoc import text
import win32con
import win32gui
import win32api
import os
import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from datetime import date
from tendo import singleton

FIRST_FORM_IS_OPENED = 0


#import win32gui, win32con
#hide = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(hide, win32con.SW_HIDE)

# .declaring path of pytesseract for windows
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

custom_font = ("system", 15)

def update(ind):
    frame = frames[ind]
    ind += 1
    if ind >= len(frames):  # Use len(frames) instead of hardcoding 30
        ind = 0
    label_logo.configure(image=frame)
    password_window.after(100, update, ind)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def exit_window(root):
    root.attributes('-fullscreen', False)  # .exit full-screen mode
    root.destroy()  

def save_text(text_widget):
    content = text_widget.get("1.0", "end-1c")  # .get the text from the text widget
    with open("blacklist.txt", "w") as file:
        file.write(content)

def save_links(link_widget):
    content = link_widget.get("1.0", "end-1c")
    if platform.system() == "Windows":
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    else:
        hosts_path ="/etc/hosts"

    lines = content.split('\n')

    with open(hosts_path, "r") as file:
        lines2 = file.readlines()

    with open(hosts_path, "w") as file:
        for line0 in lines2:
            if "127.0.0.1" not in line0:
                file.write(line0)
        for line in lines:
            modified_line = f"127.0.0.1 {line}\n\n"
            file.write(modified_line)

def clear_text3():
    result = messagebox.askyesno("Info", "Are you sure you want to delete ALL the backlog?")
    if result:
        backlog_widget.delete("1.0", "end")
        with open("backlog.txt", "w") as file:
            file.write("")
    logWIN.destroy()

def display_text_backlog(text_widget):
    file_path = "backlog.txt"
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_widget.delete("1.0", tk.END)  
            text_widget.insert(tk.END, content)  

def display_text(text_widget):
    file_path = "blacklist.txt"
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_widget.delete("1.0", tk.END)  
            text_widget.insert(tk.END, content)  
            text_widget.config(state=tk.NORMAL)  

def display_links(link_widget):
    if platform.system() == "Windows":
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    else:
        hosts_path = "/etc/hosts"
    if hosts_path:
        with open(hosts_path, "r") as file:
            content = file.read()
            link_widget.delete("1.0", tk.END) 
            lines = content.split('\n')
            for line in lines:
                if len(line) > 0 and "127.0.0.1" in line and "#" not in line:
                    modified_line = line[10:]
                    link_widget.insert(tk.END, modified_line)  
                    link_widget.insert(tk.END, "\n")
            link_widget.config(state=tk.NORMAL) 



def close_fullscreen(event):
    event.widget.quit()

def saveoption(textwidget, x):
    if (textwidget == "" and str(x)=="1") or (textwidget == "" and str(x)=="2") :
        messagebox.showinfo("Info", "You need at least a blacklisted keyword to activate the trigger.")
    else:
        optionk2 = str(x)
        config.set('TriggerType', 'trigger_option', optionk2)
        with open('config.ini', 'w') as configfile2:
            config.write(configfile2)

def func1():
    def func_call():
        import ScanScreenCat
    new_thread = threading.Thread(target=func_call)
    new_thread.start()

def thread_wrapper():
    func1()

def kill_all(root):
    config.set('KillCat', 'kill_option', "1")
    with open('config.ini', 'w') as configfile2:
        config.write(configfile2)
    exit_window(root)
    os.system("taskkill /IM python.exe /F")
    os._exit(0)

# 9999

def on_text_change(event):
    global line_numbers
    line_numbers.delete(*line_numbers.get_children())
    text_content = text.get("1.0", "end-1c").split("\n")
    for i, line in enumerate(text_content, start=1):
        line_numbers.insert("", "end", values=(i,))

def dontforget(textwidget, var):
    if textwidget != "" and var == 3:
        messagebox.showinfo("Info", "Blacklist keyword trigger is inactive.")

def cklog():
    global logWIN
    logWIN = tk.Tk()
    logWIN.title("GBTW Backlog")
    window_width = 500
    window_height = 515
    center_window(logWIN, window_width, window_height)
    logWIN.resizable(0, 0)
    logWIN.attributes('-topmost', True)
    global backlog_widget
    backlog_widget = tk.Text(logWIN, wrap=tk.WORD, width=60, height=28, font=custom_font)
    backlog_widget.pack()
    display_text_backlog(backlog_widget)
    clear_backlog_button = tk.Button(logWIN, text="⛌", font=custom_font, command=clear_text3)
    clear_backlog_button.pack()
    buffer_label = tk.Label(logWIN, text="______________________________________________________________________", font=("system"))
    buffer_label.pack()
    version_label = tk.Label(logWIN, text="INVIMECo | v1.0", font=("system"))
    version_label.pack(side="bottom")
    version_label.place(x=10, y=495)

    logWIN.mainloop()

def helpme():
    import webbrowser
    webbrowser.open("https://invimecha.com/gbtw_help.html", new=0, autoraise=True)

def settings_form():
    password_window.destroy()
    settings_call()
    global set_root
    set_root = tk.Tk()
    set_root.title("Get Back To Work, Main Application")

    saveoption("", 3)

    img = ImageTk.PhotoImage(Image.open("logo_inner.png"))
    label_img = tk.Label(set_root, image = img)
    label_img.pack()

    buffer_label_p = tk.Label(set_root, text="____________________________________________________________________________", font=("system"))
    buffer_label_p.pack()

    window_width = 600
    window_height = 531
    center_window(set_root, window_width, window_height)
    set_root.resizable(0, 0)

    set_root.attributes('-topmost', True)

    blacklist_label = tk.Label(set_root, text="Keywords Blacklist", font=("system"))
    blacklist_label.pack()

    text_widget = tk.Text(set_root, wrap=tk.WORD, width=64, height=6, font= custom_font)
    text_widget.pack()

    def clear_text1():
        result = messagebox.askyesno("Info", "Are you sure you want to delete ALL the blacklisted keywords?")
        if result:
            text_widget.delete("1.0","end")

    def clear_text2():
        result = messagebox.askyesno("Info", "Are you sure you want to delete ALL the blocked domains?")
        if result:
            link_widget.delete("1.0","end")

    add_button_key = tk.Button(set_root, text="⛌", font=custom_font, command=clear_text1)
    add_button_key.pack()
    add_button_key.place(x=10, y=110, height=70)

    trigger_label = tk.Label(set_root, text="Trigger Type:", font=("system"))
    trigger_label.pack()

    var = tk.IntVar() 
    var.set(3)
   
    rb1 = tk.Radiobutton(text='Fast', font=custom_font, variable=var,
                         value=1)
    rb1.pack()

    rb1.place(x=155, y=200)

    rb4 = tk.Radiobutton(text='Inactive', font=custom_font, variable=var,
                         value=3)
    rb4.pack()


    rb2 = tk.Radiobutton(text='Slow', font=custom_font, variable=var,
                         value=2)
    rb2.pack()

    rb2.place(x=390, y=200)

    buffer_label = tk.Label(set_root, text="____________________________________________________________________________", font=("system"))
    buffer_label.pack()

    blacklist_label2 = tk.Label(set_root, text="Blocked Domains", font=("system"))
    blacklist_label2.pack()

    link_widget = tk.Text(set_root, wrap=tk.WORD, width=64, height=6, font=custom_font)
    link_widget.pack()

    add_button_link = tk.Button(set_root, text="⛌", font=custom_font, command = clear_text2)
    add_button_link.pack()
    add_button_link.place(x=10, y=305, height=70)

    display_text(text_widget)
    display_links(link_widget)
    def exitt():
        exit_window(set_root)

    save_btn = tk.Button(set_root, height=2, text="Save/Start✔", font=custom_font, command=lambda: (dontforget(text_widget.get("1.0", "end-1c"), var.get()), save_text(text_widget), save_links(link_widget), saveoption(text_widget.get("1.0", "end-1c"), var.get()), exitt()))
    save_btn.pack(pady=5)
    kill_btn = tk.Button(set_root, height=2, text="Kill💀", font=custom_font, command=lambda: kill_all(set_root))
    kill_btn.pack(pady=5)
    check_log = tk.Button(set_root, text="Backlog🔒", font=custom_font, command=lambda: cklog())
    check_log.pack(pady=5)
    check_log.place(x = 500, y = 410)
    question_button = tk.Button(set_root, text="Help Me❔", font=custom_font, command=lambda: helpme())
    question_button.pack(pady=5)
    question_button.place(x = 500, y = 450)

    buffer_label2 = tk.Label(set_root, text="____________________________________________________________________________",
                            font=("system"))
    buffer_label2.pack()

    version_label = tk.Label(set_root, text="INVIMECo | v1.0", font=("system"))
    version_label.pack(side="bottom")
    version_label.place(x=10, y=510)

    set_root.mainloop()
    global FIRST_FORM_IS_OPENED
    FIRST_FORM_IS_OPENED = 0

def check_password(password_entry, type):
    entered_password = password_entry.get()
    stored_password = config.get('Security', 'password')
    if entered_password == stored_password and type == "settings":
        settings_form()
    elif entered_password == stored_password and type == "stop":
        exit_window(password_window)
        os._exit(0)
    else:
        messagebox.showerror("Access Denied", "Invalid key. Try again.")

def change_password():
    password_window.destroy()
    change_password_window = tk.Tk()
    change_password_window.resizable(0, 0)
   
    window_width = 160
    window_height = 229
    center_window(change_password_window, window_width, window_height)

    change_password_window.iconbitmap(default=ICON_PATH)

    def back_to_password_form():
        change_password_window.destroy()
        create_password_form()

    old_password_label = tk.Label(change_password_window, text="Old Key:", font=custom_font)
    old_password_label.pack()
    old_password_entry = tk.Entry(change_password_window, show="*")
    old_password_entry.pack()
    new_password_label = tk.Label(change_password_window, text="New Key:", font=custom_font)
    new_password_label.pack()
    new_password_entry = tk.Entry(change_password_window, show="*")
    new_password_entry.pack()
    confirm_password_label = tk.Label(change_password_window, text="New Key:", font=custom_font)
    confirm_password_label.pack()
    confirm_password_entry = tk.Entry(change_password_window, show="*")
    confirm_password_entry.pack()
    change_button = tk.Button(change_password_window, text="Change Key", font=custom_font, command=lambda:
                              change_password_action(old_password_entry.get(), new_password_entry.get(),
                                                     confirm_password_entry.get()))
    change_button.pack(pady=5)
    back_button = tk.Button(change_password_window, text="Exit", font=custom_font, command=back_to_password_form)
    back_button.pack(pady=5)

    buffer_label_pp = tk.Label(change_password_window, text="-------------------------------------------", font=("system"))
    buffer_label_pp.pack()

    version_label = tk.Label(change_password_window, text="INVIMECo | v1.0", padx=0, pady=0, font=("system"))
    version_label.pack(side="bottom")
    version_label.place(x=10, y=208)
    change_password_window.mainloop()

def change_password_action(old_password, new_password, confirm_password):
    stored_password = config.get('Security', 'password')
    if old_password == stored_password:
        if new_password == confirm_password:
            config.set('Security', 'password', new_password)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo("Info", "New key accepted.")
        else:
            messagebox.showerror("Error", "New key mismatch. Try again.")
    else:
        messagebox.showerror("Error", "Old Key invalid. Try again.")

def create_password_form(type):
    k = 0
    global label_logo, password_window, frames
    password_window = tk.Tk()
    password_window.title("GBTW")
    
    window_width = 160
    window_height = 215
    center_window(password_window, window_width, window_height)
    password_window.resizable(0, 0)
    
    password_window.attributes('-topmost', True)
   
    password_window.iconbitmap(default=ICON_PATH)
    
    label_logo = tk.Label(password_window)
    label_logo.pack()
    frames = [tk.PhotoImage(file="rat_logo5.gif", format="gif -index %i" % i) for i in range(30)]
    password_window.after(0, update, 0)

    #
    #password_label = tk.Label(password_window, text="Get Back To Work!", font=custom_font)
    #password_label.pack()

    img = ImageTk.PhotoImage(Image.open("logo_outer.png"))
    label_img = tk.Label(password_window, image=img)
    label_img.pack()
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()
    login_button = tk.Button(password_window, text="Enter Key", font=custom_font, command=lambda: check_password(password_entry, type))
    login_button.pack(pady=5)
    change_password_button = tk.Button(password_window, text="Reset Key", font=custom_font, command=change_password)
    change_password_button.pack(pady=5)

    buffer_label_pp = tk.Label(password_window,text="-------------------------------------------", font=("system"))
    buffer_label_pp.pack()
    version_label = tk.Label(password_window, text="INVIMECo | v1.0", padx=0, pady=0, font=("system"))
    version_label.pack(side="bottom")
    version_label.place(x=10, y=195)
    password_window.bind("<Return>", lambda event=None: check_password(password_entry, type))
    password_window.mainloop()
    global FIRST_FORM_IS_OPENED
    FIRST_FORM_IS_OPENED = 0

config = configparser.ConfigParser()
config.read('config.ini')

if 'Security' not in config:
    config['Security'] = {'password': 'your_default_password_here'}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

if 'TriggerType' not in config:
    config['TriggerType'] = {'trigger_option': 0}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

if 'KillCat' not in config:
    config['KillCat'] = {'kill_option': 0}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def settings_call():
    global FIRST_FORM_IS_OPENED
    if FIRST_FORM_IS_OPENED == 0:
        FIRST_FORM_IS_OPENED = 1
        tkinter_process = multiprocessing.Process(target=create_password_form("settings"))
        tkinter_process.start()

ICON_PATH = "example.ico"  # Replace with the path to your icon file

def on_tray_icon_clicked(hwnd, msg, wparam, lparam):
    if lparam == win32con.WM_LBUTTONDOWN:
        settings_call()
    elif lparam == win32con.WM_RBUTTONDOWN:
        print("Tray icon right-clicked!")

def create_tray_icon():
    wc = win32gui.WNDCLASS()
    hinst = wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = "MyTrayIcon"
    wc.lpfnWndProc = on_tray_icon_clicked
    class_atom = win32gui.RegisterClass(wc)

    hwnd = win32gui.CreateWindow(
        class_atom, "MyTrayIcon", 0,
        0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
        0, 0, hinst, None
    )

    hicon = win32gui.LoadImage(0, ICON_PATH, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE)
    nid = (hwnd, 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE, win32con.WM_USER + 20, hicon, "TrayIconDemo")
    try:
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
    except win32gui.error:
        pass
    
    #hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
    #nid = (hwnd, 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE, win32con.WM_USER + 20, hicon, "TrayIconDemo")
    #try:
    #    win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
    #except win32gui.error:
    #    pass

    win32gui.PumpMessages()

def funnc1():
    if getattr(sys, 'frozen', False):
        script_location = sys.executable
    else:
        script_location = os.path.abspath(__file__)

    script_location = os.path.dirname(script_location)

    os.system(f'"{script_location}/ScanScreenCat.exe"')

def funcc2():
    from pynput.keyboard import Key, Controller

    if getattr(sys, 'frozen', False):
        script_location = sys.executable
    else:
        script_location = os.path.abspath(__file__)

    script_location = os.path.dirname(script_location)

    pytesseract.pytesseract.tesseract_cmd = script_location + "/Tesseract-OCR/tesseract.exe"

    # pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    config = configparser.ConfigParser()
    config.read('config.ini')

    def display_text(text_widget):
        file_path = "blacklist.txt"
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                text_widget.delete("1.0", tk.END)  # .clear the current content of the text widget
                text_widget.insert(tk.END, content)  # .insert the content from the file
                text_widget.config(state=tk.NORMAL)  # .make the text widget editable

    def capture_and_display_screenshot(x):
        global label_logo, cat_window, frames, booly

        from datetime import datetime
        dt = datetime.now()

        current_time = dt.strftime("%H:%M:%S")

        current_time0 = str(current_time)
        current_date0 = str(date.today())

        towrite = ""

        file_path = "backlog.txt"
        if file_path:
            with open(file_path, "r") as file1:
                lines = file1.read()
                lines0 = str(lines)
                towrite = towrite + lines0
            towrite = towrite + (current_date0 + " | " + current_time0 + " : " + x + " @ ")
            with open(file_path, "w") as file2:
                file2.write(towrite)

        booly = 0
        # exit the settings, if opened
        pyautogui.FAILSAFE = False

        def minimize_continuously():
            while booly == 0:
                pyautogui.hotkey('win', 'm')
                time.sleep(5)

        t = threading.Thread(target=minimize_continuously)
        t.setDaemon(True)
        t.start()

        cat_window = tk.Tk()

        # wrongkey_window = tk.Toplevel()
        # . hides window from taskbar
        # wrongkey_window.attributes('-topmost', True)
        # Convert the PIL Image to a Tkinter PhotoImage

        def close_window(_event):
            cat_window.destroy()

        label_trigger_esc = tk.Label(cat_window, text="Press 'esc' to exit. Trigger word: " + x, font=("system", 20))
        label_trigger_esc.pack(side=tk.BOTTOM)

        cat_window.attributes('-fullscreen', True)
        cat_window.overrideredirect(True)
        cat_window.wm_attributes('-transparentcolor', 'white')
        imgcat = ImageTk.PhotoImage(Image.open("gbtwcat.jpg"))
        label_img = tk.Label(cat_window, image=imgcat)
        label_img.pack()
        cat_window.bind('<Escape>', close_window)
        cat_window.attributes('-topmost', True)
        cat_window.after(1, lambda: cat_window.focus_force())
        cat_window.mainloop()

        booly = 1

    def gbtw_program():
        with open('config.ini', 'r') as config_file:
            config = configparser.ConfigParser()
            config.read_file(config_file)
        with open('config.ini', 'r') as config_file:
            new_config = configparser.ConfigParser()
            new_config.read_file(config_file)
        option_trigger = config.get('TriggerType', 'trigger_option')
        optionk = int(option_trigger)
        option_kill_cat = config.get('KillCat', 'kill_option')
        optionkillcat_ = int(option_kill_cat)

        while new_config == config and optionk != 3 and optionkillcat_ == 0:
            screenshot = ImageGrab.grab()
            words_on_screen = pytesseract.image_to_string(screenshot, lang='eng', config='--psm 6')

            if words_on_screen and optionk == 2:
                words_on_screen = words_on_screen.translate(str.maketrans('', '', string.punctuation))
                words_on_screen = words_on_screen.split(" ")
                file_path = "blacklist.txt"
                if file_path:
                    with open(file_path, "r") as file:
                        content = file.read()
                        content = content.split(", ")
                        for x in content:
                            for y in words_on_screen:
                                if x == y:
                                    capture_and_display_screenshot(x)
                                    time.sleep(1)

            elif words_on_screen and optionk == 1:
                file_path = "blacklist.txt"
                if file_path:
                    with open(file_path, "r") as file:
                        content = file.read()
                        content = content.split(", ")
                        for x in content:
                            if x.lower() in words_on_screen.lower():
                                capture_and_display_screenshot(x)
                                time.sleep(1)

            time.sleep(1)
            with open('config.ini', 'r') as config_file:
                new_config = configparser.ConfigParser()
                new_config.read_file(config_file)

        with open('config.ini', 'r') as config_file:
            config = configparser.ConfigParser()
            config.read_file(config_file)
        with open('config.ini', 'r') as config_file:
            new_config = configparser.ConfigParser()
            new_config.read_file(config_file)
        while config == new_config:
            time.sleep(1)
            with open('config.ini', 'r') as config_file:
                new_config = configparser.ConfigParser()
                new_config.read_file(config_file)
            if (optionkillcat_ == 1):
                config.set('KillCat', 'kill_option', "0")
                with open('config.ini', 'w') as configfile2:
                    config.write(configfile2)
                time.sleep(1)
                os.system("taskkill /IM python.exe /F")
                os._exit(0)
            gbtw_program()

    tkinter_thread = threading.Thread(target=gbtw_program)
    tkinter_thread.start()

import socket
s = socket.socket()
host = socket.gethostname()
port = 12344
s.bind((host, port))
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), win32con.SW_HIDE)
thread1 = Thread(target=create_tray_icon)
thread2 = Thread(target=funcc2)
thread1.start()
thread2.start()
