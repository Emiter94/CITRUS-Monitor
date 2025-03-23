# import librares
import os
import sys
from PIL import Image, ImageTk
import customtkinter
import tkinter
import psutil
from tkinter import messagebox
import wmi
from datetime import datetime as dt
import socket
import configparser

# настойка либы, проверка файла с настроками
config = configparser.ConfigParser()
config.sections()

config.read('settings.ini')

try:
    mode = config['SET']['Mode']
    theme = config['SET']['Theme']
except KeyError:
     open('settings.ini', 'w')
     config.read('settings.ini')
     config.add_section('SET')
     config.set('SET', 'Mode', 'Dark')
     config.set('SET', 'Theme', 'blue')
     config.set('SET', 'activated', '0')
     config.set('SET', 'sosal', '0')
     with open('settings.ini', 'w') as config_file:
         config.write(config_file)
     tkinter.messagebox.showwarning('', 'Файл с настройками был утерян, он будет восстановлен до значений по умолчанию, перезапустите программу!')
     sys.exit()

if mode == 'Dark':
    values = ["Dark", "Light", "System"]
elif mode == 'Light':
    values = ["Light", "Dark", "System"]
elif mode == 'System':
    values = ["System", "Dark", "Light"]

computer = wmi.WMI()
app = customtkinter.CTk()
customtkinter.set_appearance_mode(mode)
customtkinter.set_default_color_theme(theme)
date = dt.now().strftime("%d.%m.%Y")

app.title('CITRUS Monitor')
app.geometry('1280x720')
app.resizable(height=False, width=False)
app.iconbitmap('custom.ico')

loading = customtkinter.CTk()

loading.geometry('500x200')
loading.resizable(height=False, width=False)
loading.title('')
loading.attributes('-toolwindow', True)
loading.attributes("-alpha", 1)

ctk = customtkinter.CTkLabel(loading, text='CITRUS Monitor')
ctk.configure(font=('Arial', 25))

load = customtkinter.CTkLabel(loading, text='Collecting system data...')

progressbar = customtkinter.CTkProgressBar(loading, orientation="horizontal",
                                           determinate_speed=2.6,
                                           height=20,
                                           width=300)
progressbar.set(0)

ctk.place(x=10, y=10)
load.place(x=12, y=40)
progressbar.pack(expand=True, anchor='s', pady=20)

loading.update()


def test_sys():
    os.system('winsat formal -restart clean')


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)
    config.set('SET', 'Mode', new_appearance_mode)
    with open('settings.ini', 'w') as config_file:
        config.write(config_file)


def clean():
    os.system('rd %temp% /s /q')
    tkinter.messagebox.showinfo('CITRUS Monitor', 'Cleaning temporary files is complete')


def about():
    tkinter.messagebox.showinfo('About', 'CITRUS Monitor\nVersion: 1.5.1\nRelease date: 22.03.2025')


def get_size(bts: int, ending='B') -> str:
    size = 1024
    for item in ["", "K", "M", "G", "T", "P"]:
        if bts < size:
            return f"{bts:.2f} {item}{ending}" if bts > 0 else f"{bts:.2f} {item}B"
        bts /= size

if 0 == 0:
    print(12)
    config.set('DATA', 'system', f'System: {computer.Win32_OperatingSystem()[0].caption}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'cpu', f'CPU: {computer.Win32_Processor()[0].name}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'ram', f'RAM: {round(psutil.virtual_memory().total / (1024.0 ** 3))} GB')
    progressbar.step()
    loading.update()
    config.set('DATA', 'name', f'Computer name:  {socket.gethostname()}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'bv', f'BIOS name: {computer.Win32_Bios()[0].caption}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'bm', f'BIOS manufacturer: {computer.Win32_Bios()[0].manufacturer}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'cor', f'Cores: {computer.Win32_Processor()[0].numberofcores}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'log_proc', f'Logical processors: {computer.Win32_Processor()[0].numberoflogicalprocessors}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'mbm', f'Motherboard manufacturer: {computer.Win32_ComputerSystem()[0].manufacturer}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'mbv', f'Motherboard model: {computer.Win32_ComputerSystem()[0].model}')
    progressbar.step()
    loading.update()
    progressbar.step()
    loading.update()
    config.set('DATA', 'soc', f'CPU socket: {computer.Win32_processor()[0].socketdesignation}')
    progressbar.step()
    loading.update()
    config.set('DATA', 'cclk', f'CPU frequency: {computer.Win32_processor()[0].currentclockspeed / 1000} GHz')
    progressbar.step()
    loading.update()
    config.set('DATA', 'l2', f'L2 cache: {computer.Win32_processor()[0].l2cachesize / 1000} MB')
    progressbar.step()
    loading.update()
    progressbar.step()
    loading.update()

    if computer.Win32_processor()[0].l3cachesize / 1000 <= 0:
        l3 = ''
        config.set('DATA', 'l3', '')
    else:
        config.set('DATA', 'l3', f'L3 cache: {computer.Win32_processor()[0].l3cachesize / 1000} MB')

    progressbar.step()
    loading.update()
    config.set('DATA', 'bn', f'BIOS version: {computer.Win32_bios()[0].SMBIOSBIOSVersion}')
    progressbar.step()
    loading.update()

    try:
        config.set('DATA', 'gpu', f'First GPU name: {computer.Win32_VideoController()[0].name}')
        config.set('DATA', 'gpram', f'First GPU memory: {get_size(abs(computer.Win32_VideoController()[0].adapterram))}')
        config.set('DATA', 'gpus', f'Second GPU name : {computer.Win32_VideoController()[1].name}')
        config.set('DATA', 'gprams', f'Second GPU memory : {get_size(abs(computer.Win32_VideoController()[1].adapterram))}')
    except IndexError:
        config.set('DATA', 'gpu', f'GPU name: {computer.Win32_VideoController()[0].name}')
        config.set('DATA', 'gpram',f'GPU memory: {get_size(abs(computer.Win32_VideoController()[0].adapterram))}')
        config.set('DATA', 'gpus', '')
        config.set('DATA', 'gprams','')
    except TypeError:
        config.set('DATA', 'gpu', f'GPU name: {computer.Win32_VideoController()[0].name}')
        config.set('DATA', 'gpram', f'GPU memory: {get_size(abs(computer.Win32_VideoController()[0].adapterram))}')
        config.set('DATA', 'gpus', '')
        config.set('DATA', 'gprams', '')
    progressbar.step()
    loading.update()

    if computer.Win32_Processor()[0].VirtualizationFirmwareEnabled is True:
        b = "On"
        tc = '#25c206'
    else:
        b = "Off"
        tc = '#d60b0b'

    config.set('DATA', 'virt', f'Firmware virtualization: {b}')
    config.set('DATA', 'tc', tc)
    progressbar.step()
    loading.update()
    with open('settings.ini', 'w') as config_file:
        config.write(config_file)
    system = config['DATA']['system']
    cpu = config['DATA']['cpu']
    ram = config['DATA']['ram']
    name = config['DATA']['name']
    bv = config['DATA']['bv']
    bm = config['DATA']['bm']
    cor = config['DATA']['cor']
    log_proc = config['DATA']['log_proc']
    mbm = config['DATA']['mbm']
    mbv = config['DATA']['mbv']
    gpu = config['DATA']['gpu']
    gpram = config['DATA']['gpram']
    gpus = config['DATA']['gpus']
    gprams = config['DATA']['gprams']
    soc = config['DATA']['soc']
    cclk = config['DATA']['cclk']
    l2 = config['DATA']['l2']
    bn = config['DATA']['bn']
    a = config['DATA']['virt']
    tc = config['DATA']['tc']
    l3 = config['DATA']['l3']

if computer.Win32_NetworkAdapterConfiguration()[0].ipaddress is None:
    my_ip = f'IP address: {computer.Win32_NetworkAdapterConfiguration()[1].ipaddress}'
else:
    my_ip = f'IP address: {computer.Win32_NetworkAdapterConfiguration()[0].ipaddress}'

customtkinter.CTkLabel(app, text=date).place(x=1200, y=690)
customtkinter.CTkLabel(app, text=system).place(x=500, y=20)
customtkinter.CTkLabel(app, text=cpu).place(x=20, y=20)
customtkinter.CTkLabel(app, text=cor).place(x=80, y=60)
customtkinter.CTkLabel(app, text=log_proc).place(x=80, y=100)
customtkinter.CTkLabel(app, text=a, text_color=tc).place(x=80, y=140)
customtkinter.CTkLabel(app, text=ram).place(x=500, y=260)
customtkinter.CTkLabel(app, text=bv).place(x=500, y=340)
customtkinter.CTkLabel(app, text=bm).place(x=500, y=300)
customtkinter.CTkLabel(app, text=mbm).place(x=500, y=380)
customtkinter.CTkLabel(app, text=mbv).place(x=500, y=420)
customtkinter.CTkLabel(app, text=my_ip).place(x=500, y=180)
customtkinter.CTkLabel(app, text=soc).place(x=80, y=180)
customtkinter.CTkLabel(app, text=cclk).place(x=80, y=220)
customtkinter.CTkLabel(app, text=l2).place(x=80, y=260)
customtkinter.CTkLabel(app, text=l3).place(x=80, y=300)
customtkinter.CTkLabel(app, text=bn).place(x=500, y=460)
customtkinter.CTkLabel(app, text=gpu).place(x=500, y=500)
customtkinter.CTkLabel(app, text=gpram).place(x=500, y=540)
customtkinter.CTkLabel(app, text=gpus).place(x=500, y=580)
customtkinter.CTkLabel(app, text=gprams).place(x=500, y=620)
sys_n = customtkinter.CTkLabel(app, text=f'Windows build: {computer.Win32_OperatingSystem()[0].buildnumber}')
sys_n.place(x=500, y=100)
sys_ar = customtkinter.CTkLabel(app, text=f'Windows architecture: {computer.Win32_OperatingSystem()[0].osarchitecture}')
sys_ar.place(x=500, y=140)


def settings():
    setin = customtkinter.CTk()
    setin.title('Settings')
    setin.geometry('400x200')
    setin.update()
    appearance_mode_optionmenu = customtkinter.CTkOptionMenu(setin, values=values, command=change_appearance_mode_event)
    appearance_mode_optionmenu.place(x=10, y=10)
    ent = customtkinter.CTkEntry(setin, width=200, height=20, placeholder_text='Activating Code')
    ent.place(x=170, y=15)


    def set_but():
        pole = ent.get()
        if pole == 'GT5748-UYTJF-76484-UY7TR':
            print('activated')
            config.set('SET', 'activated', '1')
            with open('settings.ini', 'w') as config_file:
                config.write(config_file)
            tkinter.messagebox.showinfo('Activating manager', 'Программа была успешно активирована')


    act_but = customtkinter.CTkButton(setin, text='Confirm', command=set_but)
    act_but.place(x=220, y=45)
    ab_but = customtkinter.CTkButton(setin, text='About', command=about)
    ab_but.place(x=250, y=150)
    setin.update()

image = ImageTk.PhotoImage(file="setting.png")

customtkinter.CTkButton(app, image=image, command=settings, text='', fg_color='transparent', width=70, height=70, bg_color='transparent').place(x=0, y=650)

node = customtkinter.CTkLabel(app, text=name)
node.place(x=500, y=60)
cl = customtkinter.CTkButton(app, text='Сleaning temporary files', command=clean)
cl.place(x=1070, y=20)

loading.destroy()

if config['SET']['activated']=='0':
    tkinter.messagebox.showwarning('Activating manager', 'Активируте программу, это можно сделать в настройках!')

app.mainloop()
