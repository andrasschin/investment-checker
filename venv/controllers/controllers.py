from tkinter import *

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