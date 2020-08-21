from tkinter import *
import re


def create_widget(type, widget_list, root, txt="", r=0, c=0, w=0, comm="", state="normal"):
    if type == "label":
        widget = Label(root, text=txt)
        widget_list.append(widget)
    if type == "entry":
        widget = Entry(root, width=w)
        widget_list.append(widget)
    if type == "button":
        widget = Button(root, text=txt, command=comm, state=state)
        widget_list.append(widget)

    widget.grid(row=r, column=c)

    return widget


def config_widgets(widgets=[], basic_cfg={}, additional_cfg={}):
    for widget in widgets:
        widget.config(**basic_cfg, **additional_cfg)


def check_input(quan="", price="", date=""):
    quan_pattern = re.compile("^\d+$")
    price_pattern = re.compile("^(\d+(\.\d+)?)$")
    date_pattern = re.compile("\d{4}\.\d{2}\.\d{2}$")

    if quan_pattern.match(quan) == None or price_pattern.match(price) == None or date_pattern.match(date) == None:
        return False

    return True


def color_difference(value_to_check, widget):
    if value_to_check > 0:
        widget.config(fg="#149911")
    if value_to_check < 0:
        widget.config(fg="#B23A48")