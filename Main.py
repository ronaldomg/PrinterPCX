#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import Tk, BOTH, Label, X, Button, LEFT, CENTER, RIGHT, N, SUNKEN, DISABLED, FLAT, NORMAL, PhotoImage
from ttk import Frame, Style
from tkFileDialog import askopenfilename
from PIL import ImageTk, Image
from os import path, sep
from win32print import OpenPrinter, StartDocPrinter, StartPagePrinter, WritePrinter, EndPagePrinter, EndDocPrinter, ClosePrinter

import usb1

context = usb1.USBContext()
for device in context.getDeviceList(skip_on_error=True):
    print 'ID %04x:%04x' % (device.getVendorID(), device.getProductID()), '->'.join(str(x) for x in ['Bus %03i' % (device.getBusNumber(), )] + device.getPortNumberList()), 'Device', device.getDeviceAddress()


OPTIONS = dict(defaultextension='.jpg', title="Escolha o arquivo que deseja converter",
                  filetypes=[('Imagens', ('*.jpg', '*.jpeg', '*.png', '*.bmp')), ('Todos Arquivos', '*.*')])


placeholder = None

c_path = path.dirname(path.realpath(__file__))+sep

root = Tk()
root.geometry("450x450+200+200")
root.attributes("-alpha", 0.9)

root.title("Gravar Graficos na impressora")
# the_file = None


def select_file():
    the_file = askopenfilename(**OPTIONS)
    if the_file:
        converted_name = "converted.bmp"
        file_entry.configure(text=the_file)
        c_img = Image.open(the_file, 'r')
        c_img = c_img.convert('1')
        c_img.thumbnail((110, 110))
        c_img.save(converted_name, format="BMP")
        p_img = ImageTk.PhotoImage(Image.open(c_path+converted_name))
        img_label.configure(image=p_img)
        img_label.image = p_img
        img_label.update()

        s_btn.configure(state=NORMAL)
        s_btn.update()


def send_file():
    raw = '☻KQ'
    d_printer = OpenPrinter('Argox')  # connect to the selected printer
    StartDocPrinter(d_printer, 1, ('config', None, "RAW"))
    StartPagePrinter(d_printer)
    WritePrinter(d_printer, raw)
    EndPagePrinter(d_printer)
    EndDocPrinter(d_printer)
    ClosePrinter(d_printer)

# Top Frame Begin
Style().configure("TFrame", background="#333")
master_frame = Frame(root)
master_frame.pack(fill=BOTH, expand=True)
top_frame = Frame(master_frame)
top_frame.pack(fill=X)
lbl_help = Label(top_frame, bg="#222", fg="#EEE", pady=10,
                 text="Por favor selecione a imagem que deseja converter."
                      "\n\nIMPORTANTE:"
                      "\n -> Os arquivos devem ser em formato bmp, jpg ou png"
                      "\n -> As imagens devem ser simples e com poucos detalhes"
                      "\n -> Os arquivos devem ser menores que 6kB",
                 justify=LEFT)
lbl_help.pack(fill=X)
# Top Frame End
# Middle frame start
middle_frame = Frame(master_frame)
middle_frame.pack(fill=BOTH, expand=True)
tk_image = ImageTk.PhotoImage(Image.open(c_path+'bitmap.gif'))
img_label = Label(middle_frame, bg="#999", bd=15, padx=20, pady=20, relief=FLAT)
img_label.configure(image=tk_image)
img_label.place(relx=0.5, rely=0.5, anchor=CENTER)
# Middle Frame end

# Frame2 Begin
bottom_frame = Frame(master_frame)
bottom_frame.pack(fill=X)
file_entry = Label(bottom_frame, bg="#222", fg="#EEE", justify=LEFT, relief=SUNKEN)
s_btn = Button(bottom_frame, activebackground="#111", bg="#222", fg="#EEE",
               text="Enviar para impressora", justify=CENTER, command=send_file)  # , state=DISABLED)

sel_btn = Button(bottom_frame, activebackground="#111", bg="#222", fg="#EEE",
                 text="Selecione o Arquivo", justify=CENTER, command=select_file)
file_entry.pack(fill=BOTH, pady=5, padx=5, expand=True)
s_btn.pack(side=RIGHT, anchor=N, padx=5, pady=5)
sel_btn.pack(side=RIGHT, anchor=N, padx=5, pady=5)


Style().configure("TLabel", background="#222")
root.mainloop()
