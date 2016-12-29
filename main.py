#coding: utf-8

import sys
import pyaudio
import tkinter
from tkinter import messagebox

from analysis import analysis

DEVICE=0

def change(hide, show):
    hide.lower()
    show.lift()

def show_img():
    global result_img
    result_img = tkinter.PhotoImage(file = 'result.gif')
    canvas.create_image(310, 310, image = result_img, tag='result_img')

def initial_txt(canvas):
    canvas.delete('all')
    canvas.create_text(310, 310, anchor='center', justify='center',
                                   text='ボタンを押して録音開始！', font=(None, 40))
    canvas.create_text(310, 30, anchor='n', justify='center',
                                   text='↑\n↑\n↑\n↑\n', font=(None, 40))

def rec_txt(canvas):
    canvas.delete('all')
    canvas.create_text(310, 310, anchor='center', justify='center',
                                   text='録音中', font=(None, 40))

def rec_start(canvas, dev):
    analysis(canvas, device=dev)
    change(button1, button2)

def quit():
    if messagebox.askokcancel("終了", "終了しますか?"):
        root.quit()
        root.destroy()

if __name__ == '__main__':
        
    # get audio device
    p = pyaudio.PyAudio()
    devices = [p.get_device_info_by_index(i)['name'] for i in range(p.get_device_count())]
    
    # build GUI app with tkinter
    root = tkinter.Tk() 
    root.title('音声分析アプリ')
    root.geometry("1000x1000")
    
    menubar = tkinter.Menu(root)
    root.configure(menu=menubar)
    
    Device=tkinter.IntVar()
    Device.set(DEVICE)
    
    filemenu = tkinter.Menu(menubar)
    menubar.add_cascade(label="デバイス", menu=filemenu)
    for i, dev in enumerate(devices):
        filemenu.add_radiobutton(label=dev, variable=Device, value=i)
    
    button1 = tkinter.Button(root, text="録音開始", height=3, width=15, font=(None, 20)) 
    button1.bind('<Button-1>', lambda e:rec_txt(canvas))
    button1.bind('<ButtonRelease-1>', lambda e:rec_start(canvas, Device.get()))
    button1.place(anchor='center', relx=0.5, y=60)
    
    button2 = tkinter.Button(root, text="結果を見る", height=3, width=15, font=(None, 20),
                                           command=lambda:(show_img(), change(button2, button3)))
    button2.place(anchor='center', relx=0.5, y=60)
    
    button3 = tkinter.Button(root, text="もう一度", height=3, width=15, font=(None, 20),
                                           command=lambda:(change(button3, button1), initial_txt(canvas)))
    button3.place(anchor='center', relx=0.5, y=60)
    
    button1.lift()
    
    canvas = tkinter.Canvas(root, width=620, height=620, highlightbackground='black')
    canvas.place(anchor='center', relx=0.5, rely=0.5)
    initial_txt(canvas)
    
    button_quit = tkinter.Button(root, text="閉じる", height=2, width=10,
                                                                                 command=quit)
    button_quit.pack(side='bottom', padx=5, pady=5)
    
    root.protocol("WM_DELETE_WINDOW", quit)
    root.mainloop()
    root.destroy()