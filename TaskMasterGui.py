# Russ Johnson 22 Aug 2025

import json
import tkinter as tk
from tkinter import ttk


class TaskRow(ttk.Frame):
    def __init__(self, parent, text, complete=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.check_var = tk.BooleanVar(value=complete)

        self.check = ttk.Checkbutton(self, variable=self.check_var)
        self.check.grid(row=0, column=0, sticky="w")

        self.v = tk.StringVar(parent, value=text)

        self.task_entry = ttk.Entry(self, textvariable=self.v)

        self.task_entry.grid(row=0, column=1, sticky="w", padx=(1, 8))


class ScrollList(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)  # this will call the parent class init

        # build the scrolling canvas. Needs to be a canvas becuase we have more than a stack of entries
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # build inner frame that the rows will go on
        self.inner = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # keep resizing the scrollable window whenever a change is made
        self.inner.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)


class App(tk.Tk):
    # TODO: consider picking a ttk style
    def __init__(self):
        super().__init__()
        self.title("TaskMaster")
        self.geometry("420x520")
        self.data = []
        with open("project_data.json", 'r') as project_data_file:
            self.data = json.load(project_data_file)
        # TODO: make a top menu like this [<][Pull down menu for projects][>]

        # make the scroll list that the rows will go on
        self.list_widget = ScrollList(self)
        self.list_widget.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # make rows with the data loaded from the file
        # TODO: make this support multiple projects in the future
        # TODO: make the list spilt completed tasks from incomplete tasks
        for task in self.data[0]["tasks"]:
            row = TaskRow(self.list_widget.inner, text=task["text"])
            row.pack(fill="x", padx=6, pady=4)


App().mainloop()
