#!/usr/bin/env python3

"""
GUI for ltocheck_gui.py
"""

# Import from Python Standard Library
import os
import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

# Import from the package
import ltocheck_gui
import gui_support


def vp_start_gui():
    """Starting point when module is the main routine."""
    global val, w, root
    root = tk.Tk()
    top = LTOCheck (root)
    gui_support.init(root, top)
    root.mainloop()


w = None


def create_lto_check(root, *args, **kwargs):
    """Starting point when module is imported by another program."""
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = LTOCheck (w)
    gui_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_lto_check():
    global w
    w.destroy()
    w = None


class LTOCheck:

    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        self.style = ttk.Style()
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.map('.',background=[('selected', _compcolor), ('active', _ana2color)])

        top.geometry("800x250+630+60")
        top.title("LTO Check")

        self.main_frame = tk.Frame(top)
        self.main_frame.place(relx=0.01, rely=0.03, relheight=0.4, relwidth=0.98)

        self.main_frame.configure(relief=tk.GROOVE, borderwidth="2", width=780)

        self.ss_csv_label = tk.Label(self.main_frame)
        self.ss_csv_label.place(relx=0.01, rely=0.2, height=20, width=100)
        self.ss_csv_label.configure(anchor=tk.E)
        self.ss_csv_label.configure(justify=tk.RIGHT)
        self.ss_csv_label.configure(text='''Master csv:''')
        self.ss_csv_label.configure(width=99)

        self.lto_csv_label = tk.Label(self.main_frame)
        self.lto_csv_label.place(relx=0.01, rely=0.55, height=20, width=100)
        self.lto_csv_label.configure(activebackground="#f9f9f9")
        self.lto_csv_label.configure(anchor=tk.E)
        self.lto_csv_label.configure(justify=tk.RIGHT)
        self.lto_csv_label.configure(text='''LTO csv:''')
        self.lto_csv_label.configure(width=105)

        self.ss_csv_path = tk.Entry(self.main_frame)
        self.ss_csv_path.place(relx=0.15, rely=0.2,height=20, relwidth=0.51)
        self.ss_csv_path.configure(background="white")
        self.ss_csv_path.configure(font="TkFixedFont")

        self.ss_csv_path_dialog = tk.Button(self.main_frame, command=self.get_ss_csv_path)
        self.ss_csv_path_dialog.place(relx=0.67, rely=0.2, height=20, width=30)
        self.ss_csv_path_dialog.configure(activebackground="#d9d9d9")
        self.ss_csv_path_dialog.configure(text='''...''')

        self.check = tk.Button(self.main_frame, command=self.run_check)
        self.check.place(relx=0.77, rely=0.2, height=26, width=92)
        self.check.configure(activebackground="#d9d9d9")
        self.check.configure(text='''Check''')
        self.check.configure(width=92)

        self.save_report = tk.Button(self.main_frame, command=self.save_report)
        self.save_report.place(relx=0.77, rely=0.5, height=26, width=95)
        self.save_report.configure(activebackground="#d9d9d9")
        self.save_report.configure(text='''Save Report''')

        self.lto_csv_path = tk.Entry(self.main_frame)
        self.lto_csv_path.place(relx=0.15, rely=0.57,height=20, relwidth=0.51)
        self.lto_csv_path.configure(background="white")
        self.lto_csv_path.configure(font="TkFixedFont")
        self.lto_csv_path.configure(selectbackground="#c4c4c4")

        self.lto_csv_path_dialog = tk.Button(self.main_frame, command=self.get_lto_csv_path)
        self.lto_csv_path_dialog.place(relx=0.67, rely=0.57, height=20, width=30)

        self.lto_csv_path_dialog.configure(activebackground="#d9d9d9")
        self.lto_csv_path_dialog.configure(cursor="fleur")
        self.lto_csv_path_dialog.configure(text='''...''')

        self.results_frame = tk.LabelFrame(top)
        self.results_frame.place(relx=0.01, rely=0.43, relheight=0.54, relwidth=0.98)
        self.results_frame.configure(relief=tk.GROOVE)
        self.results_frame.configure(text='''Result''')
        self.results_frame.configure(width=780)

        self.results_textbox = ScrolledText(self.results_frame)
        self.results_textbox.place(relx=0.01, rely=0.15, relheight=0.8, relwidth=0.97, y=-11, h=11)
        self.results_textbox.configure(background="white")
        self.results_textbox.configure(font="TkTextFont")
        self.results_textbox.configure(insertborderwidth="3")
        self.results_textbox.configure(selectbackground="#c4c4c4")
        self.results_textbox.configure(width=10)
        self.results_textbox.configure(wrap=tk.NONE)

        self.results_summary = ""
        self.results_report = []

    def get_lto_csv_path(self):
        if os.path.exists(self.lto_csv_path.get()):
            initialdir=self.lto_csv_path.get()
        else:
            initialdir="/Volumes/"
            self.lto_csv_path.delete(0, 'end')
        lto_csv_path = filedialog.askopenfilename(initialdir=initialdir,
                                                  title="Select the LTO csv file", filetypes=(
                                                   ("csv files", "*.csv"), ("all files", "*.*")))
        self.lto_csv_path.insert(0, lto_csv_path)

    def get_ss_csv_path(self):
        self.ss_csv_path.delete(0, 'end')
        ss_csv_path = filedialog.askopenfilename(initialdir="/Volumes/GoogleDrive/My\ Drive/",
                                                 title="Select the SS csv file", filetypes=(
                                                  ("csv files", "*.csv"), ("all files", "*.*")))
        self.ss_csv_path.insert(0, ss_csv_path)

    def run_check(self):
        if os.path.exists(self.ss_csv_path.get()) and os.path.exists(self.lto_csv_path.get()):
            self.results_summary, self.results_report = ltocheck_gui.check(self.ss_csv_path.get(), self.lto_csv_path.get())
            self.results_printer()
        else:
            messagebox.showinfo(title="Message", message="Please enter correct csv paths using the '...' buttons")

    def results_printer(self):
        self.results_textbox.insert(tk.END, self.results_summary)

    def save_report(self):
        f = filedialog.asksaveasfile(initialdir=os.getcwd(), mode='w', defaultextension=".csv",
                                     initialfile="lto_check_report_{:%Y-%m-%d_%H%M}.csv"
                                     .format(datetime.datetime.today()))
        if f:
            ltocheck_gui.write_csv(f, self.results_report)


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    """Configure the scrollbars for a widget."""

    def __init__(self, master):
        vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)


        self.configure(yscrollcommand=self._autoscroll(vsb))
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')

        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped


class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


if __name__ == '__main__':
    vp_start_gui()



