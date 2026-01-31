import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess
import json
import win32ui, win32gui, win32con

# ---------------- CONFIG ----------------
APP_NAME = "airLaunch Beta"
VERSION = "v0.2.0 / Build 99"
CHANGELOG = (
    "• MASSIVE Bug fixes\n GUI Overhaul, • new settings\n • Launcher frame impoved\n • This Changelog is now BIGGER!\n"
)

DEFAULT_DATA_DIR = os.path.join(
    os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
    "airLaunch", "001", "JSON", "0", "storage"
)
os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)

DATA_FILE = os.path.join(DEFAULT_DATA_DIR, "launcher_entries.json")

SIDEBAR_WIDTH = 600
WINDOW_HEIGHT = 580

ENTRY_WIDTH = 260
ENTRY_HEIGHT = 140
ENTRY_PADDING = 10

# ---------------- DATA ----------------
entries = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        entries = json.load(f)

# ---------------- TOOLTIP ----------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _=None):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + 20
        self.tip = tk.Toplevel(self.widget)
        self.tip.overrideredirect(True)
        self.tip.geometry(f"+{x}+{y}")
        tk.Label(
            self.tip,
            text=self.text,
            bg="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9)
        ).pack(ipadx=4, ipady=2)

    def hide(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None

# ---------------- ICON EXTRACTION ----------------
def extract_icon(exe, size=(64, 64)):
    try:
        large, small = win32gui.ExtractIconEx(exe, 0)
        ico = small[0] if small else large[0]
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, *size)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        win32gui.DrawIconEx(
            hdc.GetSafeHdc(), 0, 0, ico,
            size[0], size[1], 0, None, win32con.DI_NORMAL
        )
        info = hbmp.GetInfo()
        bits = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            "RGB",
            (info["bmWidth"], info["bmHeight"]),
            bits, "raw", "BGRX", 0, 1
        )
        win32gui.DestroyIcon(ico)
        return img
    except:
        return None

# ---------------- SAVE ----------------
def save_entries():
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)

# ---------------- LAUNCH ----------------
def launch_entry(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", "File not found")
        return
    subprocess.Popen(path, shell=True)

# ---------------- ADD ENTRY ----------------
def add_entry():
    exe = filedialog.askopenfilename(
        filetypes=[("Executables", "*.exe *.bat *.com *.py")]
    )
    if not exe:
        return

    img = extract_icon(exe)
    icon_path = None
    if img:
        os.makedirs("temp_icons", exist_ok=True)
        icon_path = f"temp_icons/{os.path.basename(exe)}.png"
        img.save(icon_path)

    name = os.path.splitext(os.path.basename(exe))[0]

    entries.append({
        "name": name,
        "exe": exe,
        "icon": icon_path
    })
    save_entries()
    refresh_entries()

# ---------------- REMOVE ----------------
def remove_entry(i):
    if messagebox.askyesno("Confirm", "Delete this entry?"):
        del entries[i]
        save_entries()
        refresh_entries()

# ---------------- CHANGE DATA FOLDER ----------------
def select_data_folder():
    global DATA_FILE, entries
    folder = filedialog.askdirectory()
    if not folder:
        return

    DATA_FILE = os.path.join(folder, "launcher_entries.json")
    loc_box.config(state="normal")
    loc_box.delete(0, tk.END)
    loc_box.insert(0, folder)
    loc_box.config(state="readonly")

    entries = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            entries = json.load(f)
    refresh_entries()

# ---------------- UI ----------------
root = tk.Tk()
root.title(APP_NAME)
root.geometry(f"1000x{WINDOW_HEIGHT}")
root.configure(bg="#2c2c2c")

# LEFT SIDEBAR
sidebar = tk.Frame(root, bg="#333", width=SIDEBAR_WIDTH)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

canvas = tk.Canvas(sidebar, bg="#333", highlightthickness=0)
scroll = tk.Scrollbar(sidebar, command=canvas.yview)
inner = tk.Frame(canvas, bg="#333")

inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=inner, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# RIGHT PANEL
right = tk.Frame(root, bg="#2c2c2c")
right.pack(side="right", fill="both", expand=True)

# ADD BUTTON
tk.Button(
    right, text="+ Add Entry",
    bg="#2196F3", fg="white",
    font=("Segoe UI", 11, "bold"),
    command=add_entry
).pack(pady=(15, 8))

# -------- OPTIONS BLOCK (BLACK BACKGROUND) --------
options_block = tk.Frame(right, bg="black")
options_block.pack(fill="x", padx=10, pady=6)

tk.Label(
    options_block,
    text="Options",
    fg="white",
    bg="black",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", padx=6, pady=(4, 2))

tk.Button(
    options_block,
    text="Select Folder",
    bg="#444",
    fg="white",
    command=select_data_folder
).pack(fill="x", padx=6, pady=4)

loc_box = tk.Entry(
    options_block,
    bg="black",
    fg="white",
    insertbackground="white"
)
loc_box.pack(fill="x", padx=6, pady=(0, 6))
loc_box.insert(0, DEFAULT_DATA_DIR)
loc_box.config(state="readonly")

# -------- CHANGELOG (BIGGER) --------
cl_frame = tk.Frame(right, bg="black", height=300)
cl_frame.pack(fill="x", padx=10, pady=10)
cl_frame.pack_propagate(False)

cl_scroll = tk.Scrollbar(cl_frame)
cl_scroll.pack(side="right", fill="y")

cl_text = tk.Text(
    cl_frame,
    bg="black",
    fg="white",
    wrap="word",
    yscrollcommand=cl_scroll.set
)
cl_text.pack(fill="both", expand=True)
cl_text.insert("1.0", CHANGELOG)
cl_text.config(state="disabled")
cl_scroll.config(command=cl_text.yview)

# VERSION (TOP RIGHT)
tk.Label(
    right,
    text=VERSION,
    fg="white",
    bg="#2c2c2c",
    font=("Segoe UI", 9)
).place(relx=1.0, x=-10, y=5, anchor="ne")

icon_refs = []

# ---------------- ENTRIES ----------------
def refresh_entries():
    for w in inner.winfo_children():
        w.destroy()
    icon_refs.clear()

    for i, e in enumerate(entries):
        r, c = divmod(i, 2)

        frame = tk.Frame(inner, bg="#444", width=ENTRY_WIDTH, height=ENTRY_HEIGHT)
        frame.grid(row=r, column=c, padx=ENTRY_PADDING, pady=ENTRY_PADDING)
        frame.pack_propagate(False)

        if e["icon"] and os.path.exists(e["icon"]):
            img = Image.open(e["icon"]).resize((48, 48))
        else:
            img = Image.new("RGB", (48, 48), "#666")

        photo = ImageTk.PhotoImage(img)
        icon_refs.append(photo)

        tk.Label(frame, image=photo, bg="#444").place(x=6, y=6)

        name = tk.Label(
            frame, text=e["name"],
            fg="white", bg="#444",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        )
        name.place(x=60, y=8, width=190)
        ToolTip(name, e["name"])

        tk.Button(
            frame, text="▶ Start",
            bg="#4CAF50", fg="white",
            command=lambda p=e["exe"]: launch_entry(p)
        ).place(x=150, y=90, width=90)

        tk.Button(
            frame, text="Delete",
            bg="#F44336", fg="white",
            command=lambda i=i: remove_entry(i)
        ).place(x=20, y=90, width=80)

# INIT
refresh_entries()
root.mainloop()
