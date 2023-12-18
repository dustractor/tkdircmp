import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import pathlib
import argparse
import sys
import filecmp
import itertools
import os

green = "#ccff00"
red = "#ffcccc"
blue = "#ccccff"



class DirCmpFrame(tk.LabelFrame):
    def lbdoubleclick_l(self,event):
        lb = event.widget
        sel = lb.curselection()
        item = lb.get(sel)
        path = self.pathA / item
        print("path:",path)
        os.system(f"explorer.exe /select,\"{path}\"")
    def lbdoubleclick_r(self,event):
        lb = event.widget
        sel = lb.curselection()
        item = lb.get(sel)
        path = self.pathB / item
        print("path:",path)
        os.system(f"explorer.exe /select,\"{path}\"")
    def yscrollA(self,*args):
        if self.listboxA.yview() != self.listboxB.yview():
            self.listboxB.yview_moveto(args[0])
        self.scrollbar.set(*args)
    def yscrollB(self,*args):
        if self.listboxA.yview() != self.listboxB.yview():
            self.listboxA.yview_moveto(args[0])
        self.scrollbar.set(*args)
    def yview(self,*args):
        self.listboxA.yview(*args)
        self.listboxB.yview(*args)
    def __init__(self,master,pathA,pathB):
        super().__init__(master)
        dc = filecmp.dircmp(pathA,pathB)
        self._labelframe = tk.Frame(self)
        self._labelstring_a = tk.StringVar()
        self._labelstring_b = tk.StringVar()
        self._labelstring_a.set(f"{str(pathA)} [{len(dc.left_list)}]")
        self._labelstring_b.set(f"[{len(dc.right_list)}] {str(pathB)}")
        self._label_a = tk.Label(self._labelframe,textvariable=self._labelstring_a)
        self._label_b = tk.Label(self._labelframe,textvariable=self._labelstring_b)
        self._label_a.pack(side="left")
        self._label_b.pack(side="right")
        self.config(labelwidget=self._labelframe,labelanchor="n")
        self.pathA = pathA
        self.pathB = pathB
        self.pathlistA = tk.StringVar()
        self.pathlistB = tk.StringVar()
        self.pathlistA.set(dc.left_list)
        self.pathlistB.set(dc.right_list)
        self.listboxA = tk.Listbox(self,listvariable=self.pathlistA)
        self.listboxA.pack(side="left",fill="both",expand=True)
        self.listboxB = tk.Listbox(self,listvariable=self.pathlistB)
        self.listboxB.pack(side="right",fill="both",expand=True)
        self.listboxA.bind("<Double-1>",self.lbdoubleclick_l)
        self.listboxB.bind("<Double-1>",self.lbdoubleclick_r)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right",fill="y",expand=True)
        self.listboxA.configure(yscrollcommand=self.yscrollA)
        self.listboxB.configure(yscrollcommand=self.yscrollB)
        self.scrollbar.configure(command=self.yview)
        sizeA = self.listboxA.size()
        sizeB = self.listboxB.size()
        left_only = dc.left_only
        right_only = dc.right_only
        common_files = dc.common_files
        common_dirs = dc.common_dirs
        diff_files = dc.diff_files
        for i in range(sizeA):
            item = self.listboxA.get(i)
            if item in left_only:
                self.listboxA.itemconfigure(i,background=red)
            elif item in common_files:
                self.listboxA.itemconfigure(i,background=green)
                if item in diff_files:
                    self.listboxA.itemconfigure(i,foreground="red")
            elif item in common_dirs:
                self.listboxA.itemconfigure(i,background=blue)
        for i in range(sizeB):
            item = self.listboxB.get(i)
            if item in right_only:
                self.listboxB.itemconfigure(i,background=red)
            elif item in common_files:
                self.listboxB.itemconfigure(i,background=green)
                if item in diff_files:
                    self.listboxB.itemconfigure(i,foreground="red")
            elif item in common_dirs:
                self.listboxB.itemconfigure(i,background=blue)
        self.pack(fill="both",expand=True)

class App(tk.Tk):
    def __init__(self,pathlist):
        super().__init__()
        self.cmpframes = list()
        for a,b in itertools.combinations(pathlist,r=2):
            print("a,b:",a,b)
            self.cmpframes.append(DirCmpFrame(self,a,b))


# {{{1
def main():
    args = argparse.ArgumentParser()
    args.add_argument("--path",action="append")
    ns = args.parse_args()
    print("ns.path:",ns.path)
    paths = list()
    if not ns.path:
        print("no paths supplied")
        sys.exit()
    for path in ns.path:
        p = pathlib.Path(path).resolve()
        if p.is_dir():
            paths.append(p)
        else:
            print("invalid dir path:",p)
    if len(paths) < 2:
        print("not enough paths supplied")
        sys.exit()
    print(len(paths),"paths:")
    for p in paths:
        print(p)
    app = App(paths)
    app.mainloop()


if __name__ == "__main__":
    main()

