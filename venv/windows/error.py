from tkinter import *
from controllers.controllers import create_widget, config_widgets

def display_error_window(err_msg):
    root = Tk()
    root.title("ERROR")
    root.config(padx="20", pady="10")

    Labels = []
    Buttons = []

    label_error = create_widget("label", Labels, root, txt=err_msg, r=1, c=1)
    btn_ok = create_widget("button", Buttons, root, txt="OK", comm=lambda: root.destroy(), r=2, c=1)

    basic_config = {
        "font": "44",
        "padx": "10",
        "pady": "8"
    }

    config_widgets(Labels, basic_cfg=basic_config)
    config_widgets(Buttons, basic_cfg=basic_config)