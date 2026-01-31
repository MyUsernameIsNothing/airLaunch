import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import os
import subprocess
import json
import win32ui, win32gui, win32con

# ---- Config ----
DATA_FILE = "launcher_entries.json"
VERSION = "v0.2.0 Pre-Release / Build 73"
CHANGELOG = "• Massive bug fixes\n"

SIDEBAR_WIDTH = 600
ENTRY_WIDTH = 260
ENTRY_HEIGHT = 120
ENTRY_PADDING = 10

# ---- Load entries ----
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        entries = json.load(f)
else:
    entries = []

# ---- Tooltip class ----
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("Helvetica", 10))
        label.pack(ipadx=4, ipady=2)

    def hide(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

# ---- Main window ----
root = tk.Tk()
root.title("airLaunch Beta")
WINDOW_HEIGHT = 500
root.geometry(f"1000x{WINDOW_HEIGHT}")
root.configure(bg="#2c2c2c")

# ---- Sidebar ----
sidebar_height = WINDOW_HEIGHT - ENTRY_HEIGHT // 2
sidebar = tk.Frame(root, bg="#333333", width=SIDEBAR_WIDTH, height=sidebar_height)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

canvas = tk.Canvas(sidebar, bg="#333333", highlightthickness=0)
scrollbar = tk.Scrollbar(sidebar, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#333333")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ---- Bottom info ----
bottom_frame = tk.Frame(root, bg="#2c2c2c", height=50)
bottom_frame.pack(side="bottom", fill="x")
bottom_frame.pack_propagate(False)

changelog_label = tk.Label(bottom_frame, text=CHANGELOG, fg="white", bg="#2c2c2c", justify="left")
changelog_label.pack(side="left", padx=10)

version_label = tk.Label(bottom_frame, text=VERSION, fg="white", bg="#2c2c2c")
version_label.pack(side="right", padx=10)

icon_refs = []

# ---- Functions ----
def save_entries():
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)

def launch_entry(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", f"File not found: {path}")
        return
    try:
        if path.endswith(".py"):
            subprocess.Popen(["python", path])
        else:
            subprocess.Popen(path, shell=True)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---- Extract exe icon using pywin32 ----
def extract_icon(exe_path, size=(64, 64)):
    try:
        large, small = win32gui.ExtractIconEx(exe_path, 0)
        if small:
            ico = small[0]
        elif large:
            ico = large[0]
        else:
            return None

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, size[0], size[1])
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        win32gui.DrawIconEx(hdc.GetSafeHdc(), 0, 0, ico, size[0], size[1], 0, None, win32con.DI_NORMAL)

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        win32gui.DestroyIcon(ico)
        return img
    except:
        return None

# ---- Add entry ----
def add_entry():
    exe_path = filedialog.askopenfilename(
        title="Select Executable",
        filetypes=[("Executables", "*.exe *.bat *.com *.py"), ("All files", "*.*")]
    )
    if not exe_path:
        return

    # Icon choice
    choice = messagebox.askquestion("Icon choice", "Use Default icon from the app?\nYes = Default, No = Custom icon")
    if choice == "yes":
        img = extract_icon(exe_path)
        if img:
            os.makedirs("temp_icons", exist_ok=True)
            icon_path = f"temp_icons/{os.path.basename(exe_path)}.png"
            img.save(icon_path)
        else:
            icon_path = None
    else:
        icon_path = filedialog.askopenfilename(
            title="Select Custom Icon",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.jfif *.bmp *.webp *.ico"), ("All files", "*.*")]
        )

    # Entry name choice
    use_default_name = messagebox.askquestion("Name choice", "Use the app's default name?")
    if use_default_name == "yes":
        name = os.path.splitext(os.path.basename(exe_path))[0]
    else:
        name = simpledialog.askstring("Name", "Enter a name for this entry:")
        if not name:
            name = os.path.splitext(os.path.basename(exe_path))[0]

    entries.append({"name": name, "exe": exe_path, "icon": icon_path})
    save_entries()
    refresh_entries()

# ---- Remove entry ----
def remove_entry(index):
    if messagebox.askyesno("Confirm", "Are you sure you want to delete this entry?"):
        if messagebox.askyesno("Confirm Again", "This action cannot be undone. Delete anyway?"):
            del entries[index]
            save_entries()
            refresh_entries()

# ---- Refresh entries --ghdjksl;djhsk
def refresh_entries():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    icon_refs.clear()

    for idx, entry in enumerate(entries):
        row = idx  # one entry per row
        frame = tk.Frame(scrollable_frame, bg="#222222", width=SIDEBAR_WIDTH-20, height=ENTRY_HEIGHT, bd=2, relief="ridge")
        frame.grid(row=row, column=0, padx=ENTRY_PADDING, pady=ENTRY_PADDING)
        frame.pack_propagate(False)  # keep frame size fixed

        exe_path = entry["exe"]

        # --- Icon Box ---
        icon_size = 64
        icon_frame = tk.Frame(frame, width=icon_size, height=icon_size, bg="#222222", bd=1, relief="flat")
        icon_frame.place(x=10, y=10)
        try:
            if entry["icon"] and os.path.exists(entry["icon"]):
                img = Image.open(entry["icon"]).resize((icon_size, icon_size))
            else:
                img = Image.new("RGB", (icon_size, icon_size), color="#888888")
            photo = ImageTk.PhotoImage(img)
        except:
            photo = ImageTk.PhotoImage(Image.new("RGB", (icon_size, icon_size), color="#888888"))
        icon_refs.append(photo)
        icon_label = tk.Label(icon_frame, image=photo, bg="#222222")
        icon_label.pack(expand=True, fill="both")

        # --- Name Box ---
        name_frame = tk.Frame(frame, width=300, height=30, bg="#222222", bd=1, relief="flat")
        name_frame.place(x=80, y=10)
        name_label = tk.Label(name_frame, text=entry["name"], fg="white", bg="#222222",
                              font=("Helvetica", 12, "bold"), anchor="w")
        name_label.pack(expand=True, fill="both")

        # --- Metadata ---
        import datetime
        metadata = {}
        try:
            metadata["Created"] = datetime.datetime.fromtimestamp(os.path.getctime(exe_path)).strftime("%Y-%m-%d")
        except:
            metadata["Created"] = "N/A"
        try:
            metadata["Modified"] = datetime.datetime.fromtimestamp(os.path.getmtime(exe_path)).strftime("%Y-%m-%d")
        except:
            metadata["Modified"] = "N/A"

        metadata["Publisher"] = entry.get("publisher", "N/A")
        metadata["Developer"] = entry.get("author", "N/A")

        # Box dimensions and spacing
        box_width = 140
        box_height = 25
        gap_x = 10
        gap_y = 6
        x_start = 80
        y_start = 50
        parent_bg = frame["bg"]

        # Top-left: Created
        box_created = tk.Frame(frame, width=box_width, height=box_height, bg=parent_bg, bd=1, relief="flat")
        box_created.place(x=x_start, y=y_start)
        tk.Label(box_created, text=f"Created: {metadata['Created']}", fg="white", bg=parent_bg,
                 font=("Helvetica", 9), anchor="w").pack(expand=True, fill="both")

        # Bottom-left (slightly up): Modified
        box_modified = tk.Frame(frame, width=box_width, height=box_height, bg=parent_bg, bd=1, relief="flat")
        box_modified.place(x=x_start, y=y_start+box_height+gap_y-5)
        tk.Label(box_modified, text=f"Modified: {metadata['Modified']}", fg="white", bg=parent_bg,
                 font=("Helvetica", 9), anchor="w").pack(expand=True, fill="both")

        # Top-right: Publisher
        box_pub = tk.Frame(frame, width=box_width, height=box_height, bg=parent_bg, bd=1, relief="flat")
        box_pub.place(x=x_start+box_width+gap_x, y=y_start)
        tk.Label(box_pub, text=f"Publisher: {metadata['Publisher']}", fg="white", bg=parent_bg,
                 font=("Helvetica", 9), anchor="w").pack(expand=True, fill="both")

        # Bottom-right (slightly up): Developer
        box_dev = tk.Frame(frame, width=box_width, height=box_height, bg=parent_bg, bd=1, relief="flat")
        box_dev.place(x=x_start+box_width+gap_x, y=y_start+box_height+gap_y-5)
        tk.Label(box_dev, text=f"Developer: {metadata['Developer']}", fg="white", bg=parent_bg,
                 font=("Helvetica", 9), anchor="w").pack(expand=True, fill="both")

        # --- Buttons Frame inside the main frame ---
        btn_frame = tk.Frame(frame, bg=parent_bg)
        btn_frame.place(x=SIDEBAR_WIDTH - 220, y=20)

        # Play button
        play_btn = tk.Button(btn_frame, text="▶ Start", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                             width=15, height=2, command=lambda path=exe_path: launch_entry(path))
        play_btn.pack(side="top", pady=2)

        # Delete button
        del_btn = tk.Button(btn_frame, text="🗑 Delete", bg="#F44336", fg="white", width=15,
                            command=lambda idx=idx: remove_entry(idx))
        del_btn.pack(side="top", pady=2)

# ---- Add Entry Button ----
add_btn = tk.Button(root, text="+ Add Entry", bg="#2196F3", fg="white",
                    font=("Arial", 12, "bold"), width=20, height=2, command=add_entry)
add_btn.place(x=SIDEBAR_WIDTH + 20, y=20)

refresh_entries()
root.mainloop()
