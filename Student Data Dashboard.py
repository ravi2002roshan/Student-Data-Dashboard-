import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime
import random
# ── Config ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATA_FILE = "student_data.json"

# ── Colors ─────────────────────────────────────────────────────────────────────
BG_MAIN    = "#0D1117"
BG_CARD    = "#161B22"
BG_CARD2   = "#1C2333"
BG_ROW_ALT = "#1A2030"
BLUE       = "#2F81F7"
CYAN       = "#39D0D8"
GREEN      = "#3FB950"
RED        = "#F85149"
YELLOW     = "#E3B341"
PURPLE     = "#BC8CFF"
TXT        = "#F0F6FC"
TXT2       = "#8B949E"
BORDER     = "#30363D"

COURSE_META = {
    "CCC":     {"color": BLUE,   "icon": "💻", "desc": "Course on Computer Concepts"},
    "A-Level": {"color": PURPLE, "icon": "🎓", "desc": "Advanced Level Diploma"},
    "O-Level": {"color": CYAN,   "icon": "📘", "desc": "O-Level Foundation Course"},
}

# ── Data helpers ───────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {k: {"students": []} for k in COURSE_META}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save data:\n{e}")

def next_id(students):
    existing = {s["id"] for s in students}
    for i in range(1, 99999):
        sid = f"STU{i:04d}"
        if sid not in existing:
            return sid
    return f"STU{random.randint(100000,999999)}"

# ── Widget factories ───────────────────────────────────────────────────────────
def lbl(parent, text, size=12, color=TXT, bold=False, anchor="w"):
    return ctk.CTkLabel(parent, text=text, anchor=anchor,
                        font=("Segoe UI", size, "bold" if bold else "normal"),
                        text_color=color)

def entry(parent, hint):
    return ctk.CTkEntry(parent, placeholder_text=hint, height=38,
                        fg_color=BG_CARD2, border_color=BORDER, border_width=1,
                        text_color=TXT, placeholder_text_color=TXT2,
                        font=("Segoe UI", 12), corner_radius=8)

def btn(parent, text, cmd, color=BLUE, w=130, h=36):
    def _dim(c):
        r = max(0, int(c[1:3],16)-25)
        g = max(0, int(c[3:5],16)-25)
        b = max(0, int(c[5:7],16)-25)
        return f"#{r:02x}{g:02x}{b:02x}"
    return ctk.CTkButton(parent, text=text, command=cmd, width=w, height=h,
                         fg_color=color, hover_color=_dim(color),
                         font=("Segoe UI", 12, "bold"), text_color=TXT,
                         corner_radius=8)

def hdiv(parent):
    ctk.CTkFrame(parent, height=1, fg_color=BORDER).pack(fill="x", padx=16, pady=6)

# ══════════════════════════════════════════════════════════════════════════════
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Data Dashboard — NIELIT")
        self.geometry("1150x740")
        self.minsize(1000, 680)
        self.configure(fg_color=BG_MAIN)
        self.data = load_data()
        self.show_home()

    # ── clear window ──────────────────────────────────────────────────────────
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ══════════════════════════════════════════════════════════════════════════
    #  HOME PAGE
    # ══════════════════════════════════════════════════════════════════════════
    def show_home(self):
        self._clear()

        # ── header ────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color=BG_CARD, height=105, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        inner = ctk.CTkFrame(hdr, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(inner, text="Student Data Dashboard",
                     font=("Segoe UI", 28, "bold"), text_color=TXT).pack()
        ctk.CTkLabel(inner,
                     text="National Institute of Electronics and Information Technology",
                     font=("Segoe UI", 13), text_color=CYAN).pack()

        # ── stats strip ───────────────────────────────────────────────────────
        strip = ctk.CTkFrame(self, fg_color=BG_CARD2, height=66, corner_radius=0)
        strip.pack(fill="x")
        strip.pack_propagate(False)
        total = sum(len(v["students"]) for v in self.data.values())
        stat_items = [("Total Students", str(total), BLUE),
                      ("Total Courses",  str(len(self.data)), PURPLE)]
        for cname, cmeta in self.data.items():
            c = COURSE_META.get(cname, {}).get("color", BLUE)
            stat_items.append((f"{cname} Enrolled", str(len(cmeta["students"])), c))
        for label, val, col in stat_items:
            f = ctk.CTkFrame(strip, fg_color="transparent")
            f.pack(side="left", expand=True, fill="y")
            ctk.CTkLabel(f, text=val,   font=("Segoe UI", 19, "bold"), text_color=col).pack(pady=(8,0))
            ctk.CTkLabel(f, text=label, font=("Segoe UI", 10),          text_color=TXT2).pack()

        # ── scrollable body ───────────────────────────────────────────────────
        body = ctk.CTkScrollableFrame(self, fg_color=BG_MAIN, scrollbar_button_color=BORDER)
        body.pack(fill="both", expand=True, padx=0, pady=0)

        # course cards
        lbl(body, "  Courses", 15, TXT2, bold=True).pack(anchor="w", padx=36, pady=(20,8))
        grid_f = ctk.CTkFrame(body, fg_color="transparent")
        grid_f.pack(fill="x", padx=36, pady=(0,10))
        grid_f.columnconfigure((0,1,2), weight=1, uniform="c")

        for col_idx, (cname, cmeta) in enumerate(self.data.items()):
            meta = COURSE_META.get(cname, {"color": BLUE, "icon": "📁", "desc": cname})
            self._course_card(grid_f, cname, meta, col_idx)

        # manage course buttons
        hdiv(body)
        lbl(body, "  Manage Courses", 14, TXT2, bold=True).pack(anchor="w", padx=36, pady=(6,6))
        mgr = ctk.CTkFrame(body, fg_color="transparent")
        mgr.pack(anchor="w", padx=36, pady=(0,10))
        btn(mgr, "➕ Add Course",    self._dlg_add_course,    GREEN,  148, 38).pack(side="left", padx=4)
        btn(mgr, "✏️ Update Course", self._dlg_update_course, YELLOW, 152, 38).pack(side="left", padx=4)
        btn(mgr, "🗑️ Delete Course", self._dlg_delete_course, RED,    152, 38).pack(side="left", padx=4)

        # recent students
        hdiv(body)
        lbl(body, "  Recently Added Students", 14, TXT2, bold=True).pack(anchor="w", padx=36, pady=(6,6))
        recents = []
        for cname, cmeta in self.data.items():
            for s in cmeta["students"]:
                recents.append((cname, s))
        recents = recents[-6:][::-1]
        if not recents:
            lbl(body, "  No students added yet.", 12, TXT2).pack(anchor="w", padx=36, pady=6)
        else:
            for cname, s in recents:
                col = COURSE_META.get(cname, {}).get("color", BLUE)
                row = ctk.CTkFrame(body, fg_color=BG_CARD2, corner_radius=8, height=34)
                row.pack(fill="x", padx=36, pady=2)
                row.pack_propagate(False)
                ctk.CTkLabel(row, text=f"  {s['id']}", width=80,
                             font=("Segoe UI",11,"bold"), text_color=col, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=s["name"], width=200,
                             font=("Segoe UI",11), text_color=TXT, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=cname, width=90,
                             font=("Segoe UI",11), text_color=TXT2, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=s.get("enrolled_date",""),
                             font=("Segoe UI",10), text_color=TXT2, anchor="e").pack(side="right", padx=16)

    def _course_card(self, parent, name, meta, col):
        count = len(self.data.get(name, {}).get("students", []))
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=14,
                            border_width=1, border_color=BORDER)
        card.grid(row=0, column=col, padx=10, pady=6, sticky="nsew", ipadx=8, ipady=14)

        ctk.CTkFrame(card, height=4, fg_color=meta["color"], corner_radius=0).pack(fill="x")
        ctk.CTkLabel(card, text=meta["icon"], font=("Segoe UI", 34)).pack(pady=(14,2))
        ctk.CTkLabel(card, text=name, font=("Segoe UI",17,"bold"), text_color=TXT).pack()
        ctk.CTkLabel(card, text=meta["desc"], font=("Segoe UI",10), text_color=TXT2).pack(pady=2)

        pill = ctk.CTkFrame(card, fg_color=meta["color"], corner_radius=20, width=100, height=26)
        pill.pack(pady=6)
        pill.pack_propagate(False)
        ctk.CTkLabel(pill, text=f"{count} Students",
                     font=("Segoe UI",11,"bold"), text_color=TXT).place(relx=0.5,rely=0.5,anchor="center")

        btn(card, "Open Course", lambda n=name: self.show_course(n),
            meta["color"], 138, 34).pack(pady=(8,14))

    # ══════════════════════════════════════════════════════════════════════════
    #  COURSE PAGE
    # ══════════════════════════════════════════════════════════════════════════
    def show_course(self, name):
        self._clear()
        meta  = COURSE_META.get(name, {"color": BLUE, "icon": "📁", "desc": name})
        color = meta["color"]

        # top bar
        topbar = ctk.CTkFrame(self, fg_color=BG_CARD, height=72, corner_radius=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        btn(topbar, "← Back", self.show_home, BG_CARD2, 92, 32).pack(side="left", padx=14, pady=20)
        tf = ctk.CTkFrame(topbar, fg_color="transparent")
        tf.pack(side="left", padx=8, pady=10)
        ctk.CTkLabel(tf, text=f"{meta['icon']}  {name}",
                     font=("Segoe UI",19,"bold"), text_color=color).pack(anchor="w")
        ctk.CTkLabel(tf, text=meta["desc"],
                     font=("Segoe UI",11), text_color=TXT2).pack(anchor="w")

        # action buttons
        abf = ctk.CTkFrame(self, fg_color="transparent")
        abf.pack(fill="x", padx=28, pady=(12,4))
        btn(abf, "➕ Add Student",    lambda: self._dlg_add_student(name),    GREEN,  148,38).pack(side="left",padx=4)
        btn(abf, "✏️ Update Student", lambda: self._dlg_update_student(name), YELLOW, 152,38).pack(side="left",padx=4)
        btn(abf, "🗑️ Delete Student", lambda: self._dlg_delete_student(name), RED,    152,38).pack(side="left",padx=4)
        btn(abf, "🔍 Search",         lambda: self._dlg_search_student(name), PURPLE, 120,38).pack(side="left",padx=4)

        # table container (stored so we can refresh it)
        self._table_container = ctk.CTkFrame(self, fg_color=BG_CARD,
                                             corner_radius=10, border_width=1, border_color=BORDER)
        self._table_container.pack(fill="both", expand=True, padx=28, pady=(4,16))
        self._current_course = name
        self._render_table()

    def _render_table(self):
        name  = self._current_course
        color = COURSE_META.get(name, {}).get("color", BLUE)
        parent = self._table_container
        for w in parent.winfo_children():
            w.destroy()

        students = self.data.get(name, {}).get("students", [])

        # column header
        cols = [("ID",70),("Name",170),("Father's Name",155),("DOB",100),
                ("Phone",120),("Email",185),("Enrolled",108),("Status",82)]
        hdr = ctk.CTkFrame(parent, fg_color=BG_CARD2, height=38, corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        for cname, cw in cols:
            ctk.CTkLabel(hdr, text=cname, width=cw, anchor="w",
                         font=("Segoe UI",11,"bold"), text_color=color).pack(side="left", padx=6)

        if not students:
            ctk.CTkLabel(parent, text="No students enrolled yet.  Click  ➕ Add Student  to begin.",
                         font=("Segoe UI",13), text_color=TXT2).pack(pady=50)
            return

        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent",
                                        scrollbar_button_color=color)
        scroll.pack(fill="both", expand=True)

        for i, s in enumerate(students):
            bg = BG_CARD if i % 2 == 0 else BG_ROW_ALT
            row = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=6, height=38)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)
            sc = GREEN if s.get("status","Active") == "Active" else RED
            data_cols = [
                (s.get("id",""),            70),
                (s.get("name",""),          170),
                (s.get("father_name",""),   155),
                (s.get("dob",""),           100),
                (s.get("phone",""),         120),
                (s.get("email",""),         185),
                (s.get("enrolled_date",""), 108),
            ]
            for val, w in data_cols:
                ctk.CTkLabel(row, text=str(val)[:24], width=w, anchor="w",
                             font=("Segoe UI",11), text_color=TXT).pack(side="left", padx=6)
            ctk.CTkLabel(row, text=s.get("status","Active"), width=82, anchor="w",
                         font=("Segoe UI",11,"bold"), text_color=sc).pack(side="left", padx=6)

        # footer count
        foot = ctk.CTkFrame(parent, fg_color=BG_CARD2, height=28, corner_radius=0)
        foot.pack(fill="x")
        foot.pack_propagate(False)
        ctk.CTkLabel(foot, text=f"  Total enrolled: {len(students)} students",
                     font=("Segoe UI",11), text_color=TXT2).pack(side="left", pady=4)

    # ══════════════════════════════════════════════════════════════════════════
    #  DIALOGS — helpers
    # ══════════════════════════════════════════════════════════════════════════
    def _make_dialog(self, title, w, h):
        d = ctk.CTkToplevel(self)
        d.title(title)
        d.geometry(f"{w}x{h}")
        d.configure(fg_color=BG_CARD)
        d.resizable(False, False)
        d.grab_set()
        d.lift()
        d.focus_force()
        return d

    # ── ADD STUDENT ────────────────────────────────────────────────────────────
    def _dlg_add_student(self, course_name):
        color = COURSE_META.get(course_name, {}).get("color", BLUE)
        d = self._make_dialog("Add New Student", 500, 640)

        # header strip
        hstrip = ctk.CTkFrame(d, fg_color=color, height=46, corner_radius=0)
        hstrip.pack(fill="x")
        hstrip.pack_propagate(False)
        ctk.CTkLabel(hstrip, text=f"  ➕  Add New Student — {course_name}",
                     font=("Segoe UI",13,"bold"), text_color="white").pack(side="left", pady=12)

        # form in a scrollable frame so nothing gets cut off
        form = ctk.CTkScrollableFrame(d, fg_color="transparent",
                                      scrollbar_button_color=color, height=450)
        form.pack(fill="both", expand=True, padx=0, pady=0)

        fields = {}
        form_rows = [
            ("Full Name",      "name",        "e.g.  Rahul Kumar",      True),
            ("Father's Name",  "father_name", "e.g.  Suresh Kumar",     True),
            ("Date of Birth",  "dob",         "DD-MM-YYYY",             True),
            ("Phone Number",   "phone",       "10-digit mobile number", True),
            ("Email Address",  "email",       "example@email.com",      False),
            ("Address",        "address",     "Village / City / State", False),
        ]
        for label, key, hint, required in form_rows:
            req_mark = " *" if required else ""
            lbl(form, f"{label}{req_mark}", 12, TXT2).pack(anchor="w", padx=20, pady=(12,0))
            e = entry(form, hint)
            e.pack(fill="x", padx=20, pady=(2,0))
            fields[key] = e

        lbl(form, "Status", 12, TXT2).pack(anchor="w", padx=20, pady=(12,0))
        status_var = ctk.StringVar(value="Active")
        ctk.CTkOptionMenu(form, values=["Active","Inactive"], variable=status_var,
                          fg_color=BG_CARD2, button_color=color,
                          font=("Segoe UI",12), corner_radius=8,
                          dynamic_resizing=False).pack(fill="x", padx=20, pady=(2,16))

        # ── bottom bar (always visible) ──
        bot = ctk.CTkFrame(d, fg_color=BG_CARD2, height=82, corner_radius=0)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)

        msg = ctk.CTkLabel(bot, text="  Fill required (*) fields then click Add Student.",
                           font=("Segoe UI",11), text_color=TXT2, anchor="w")
        msg.pack(fill="x", padx=14, pady=(8,2))

        brow = ctk.CTkFrame(bot, fg_color="transparent")
        brow.pack(fill="x", padx=14, pady=(0,8))

        cdata = self.data.setdefault(course_name, {"students": []})

        def do_add():
            name_v   = fields["name"].get().strip()
            father_v = fields["father_name"].get().strip()
            dob_v    = fields["dob"].get().strip()
            phone_v  = fields["phone"].get().strip()
            if not (name_v and father_v and dob_v and phone_v):
                msg.configure(text="  ⚠️  Please fill all required (*) fields.", text_color=RED)
                return
            student = {
                "id":            next_id(cdata["students"]),
                "name":          name_v,
                "father_name":   father_v,
                "dob":           dob_v,
                "phone":         phone_v,
                "email":         fields["email"].get().strip(),
                "address":       fields["address"].get().strip(),
                "status":        status_var.get(),
                "enrolled_date": datetime.now().strftime("%d-%m-%Y"),
            }
            cdata["students"].append(student)
            save_data(self.data)
            self._render_table()                      # refresh live table
            msg.configure(
                text=f"  ✅  Added! ID: {student['id']} — fields cleared, add another or Close.",
                text_color=GREEN,
            )
            for e in fields.values():
                e.delete(0, "end")
            status_var.set("Active")

        btn(brow, "➕  Add Student", do_add,    GREEN,  160, 40).pack(side="left")
        btn(brow, "Close",           d.destroy, BG_CARD2, 96, 40).pack(side="right")

    # ── DELETE STUDENT ────────────────────────────────────────────────────────
    def _dlg_delete_student(self, course_name):
        cdata = self.data.get(course_name, {"students": []})
        if not cdata["students"]:
            messagebox.showinfo("Empty", "No students in this course yet."); return

        d = self._make_dialog("Delete Student", 440, 260)
        ctk.CTkFrame(d, fg_color=RED, height=4, corner_radius=0).pack(fill="x")
        lbl(d, "  🗑️  Delete Student", 14, RED, bold=True).pack(anchor="w", padx=20, pady=(14,4))
        hdiv(d)
        lbl(d, "Enter Student ID or Full Name:", 12, TXT2).pack(anchor="w", padx=20, pady=(8,2))
        e = entry(d, "e.g.  STU0001  or  Rahul Kumar")
        e.pack(fill="x", padx=20)

        msg = lbl(d, "", 11, TXT2)
        msg.pack(anchor="w", padx=20, pady=4)

        def do_delete():
            val = e.get().strip().lower()
            if not val:
                msg.configure(text="Please enter an ID or name.", text_color=YELLOW); return
            students = cdata["students"]
            match = next((s for s in students
                          if s["id"].lower() == val or s["name"].lower() == val), None)
            if not match:
                msg.configure(text="No student found with that ID or name.", text_color=RED); return
            if messagebox.askyesno("Confirm Delete",
                                   f"Delete  '{match['name']}'  (ID: {match['id']})?\nThis cannot be undone.",
                                   parent=d):
                students.remove(match)
                save_data(self.data)
                self._render_table()
                d.destroy()
                messagebox.showinfo("Deleted", f"Student '{match['name']}' removed successfully.")

        brow = ctk.CTkFrame(d, fg_color="transparent")
        brow.pack(fill="x", padx=20, pady=12)
        btn(brow, "🗑️  Delete", do_delete, RED,      120, 38).pack(side="left")
        btn(brow, "Cancel",     d.destroy,  BG_CARD2,  96, 38).pack(side="right")

    # ── UPDATE STUDENT ────────────────────────────────────────────────────────
    def _dlg_update_student(self, course_name):
        cdata = self.data.get(course_name, {"students": []})
        if not cdata["students"]:
            messagebox.showinfo("Empty", "No students in this course yet."); return

        color = COURSE_META.get(course_name, {}).get("color", BLUE)
        d = self._make_dialog("Update Student", 500, 620)
        ctk.CTkFrame(d, fg_color=YELLOW, height=4, corner_radius=0).pack(fill="x")
        lbl(d, "  ✏️  Update Student Record", 14, YELLOW, bold=True).pack(anchor="w", padx=20, pady=(12,4))
        hdiv(d)

        # search row
        sr = ctk.CTkFrame(d, fg_color="transparent")
        sr.pack(fill="x", padx=20, pady=(4,0))
        sid_e = entry(sr, "Enter Student ID  (e.g. STU0001)")
        sid_e.pack(side="left", fill="x", expand=True, padx=(0,8))
        find_msg = lbl(d, "", 11, TXT2)
        find_msg.pack(anchor="w", padx=20, pady=2)

        # form frame (populated after Find)
        form_outer = ctk.CTkScrollableFrame(d, fg_color="transparent",
                                            scrollbar_button_color=YELLOW, height=360)
        form_outer.pack(fill="both", expand=True, padx=0, pady=0)

        fields = {}
        status_var = ctk.StringVar(value="Active")
        _match_holder = [None]

        def do_find():
            sid = sid_e.get().strip()
            for w in form_outer.winfo_children():
                w.destroy()
            fields.clear()
            _match_holder[0] = None
            if not sid:
                find_msg.configure(text="Enter an ID first.", text_color=YELLOW); return
            match = next((s for s in cdata["students"] if s["id"].lower() == sid.lower()), None)
            if not match:
                find_msg.configure(text=f"No student found with ID '{sid}'.", text_color=RED); return
            find_msg.configure(text=f"Found: {match['name']}  —  editing fields below.", text_color=GREEN)
            _match_holder[0] = match

            for label, key in [("Full Name","name"),("Father's Name","father_name"),
                                ("Date of Birth","dob"),("Phone Number","phone"),
                                ("Email Address","email"),("Address","address")]:
                lbl(form_outer, label, 12, TXT2).pack(anchor="w", padx=20, pady=(10,0))
                e = entry(form_outer, label)
                e.insert(0, match.get(key,""))
                e.pack(fill="x", padx=20, pady=(2,0))
                fields[key] = e

            lbl(form_outer, "Status", 12, TXT2).pack(anchor="w", padx=20, pady=(10,0))
            status_var.set(match.get("status","Active"))
            ctk.CTkOptionMenu(form_outer, values=["Active","Inactive"], variable=status_var,
                              fg_color=BG_CARD2, button_color=YELLOW,
                              font=("Segoe UI",12), corner_radius=8,
                              dynamic_resizing=False).pack(fill="x", padx=20, pady=(2,14))

        btn(sr, "🔍 Find", do_find, BLUE, 92, 36).pack(side="left")

        # bottom bar
        bot = ctk.CTkFrame(d, fg_color=BG_CARD2, height=60, corner_radius=0)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)
        brow = ctk.CTkFrame(bot, fg_color="transparent")
        brow.pack(fill="x", padx=14, pady=10)

        def do_save():
            if _match_holder[0] is None:
                messagebox.showwarning("No Student", "Use Find first to load a student.", parent=d); return
            match = _match_holder[0]
            for key in ["name","father_name","dob","phone","email","address"]:
                if key in fields:
                    match[key] = fields[key].get().strip()
            match["status"] = status_var.get()
            save_data(self.data)
            self._render_table()
            d.destroy()
            messagebox.showinfo("Updated", f"Student '{match['name']}' updated successfully.")

        btn(brow, "💾  Save Changes", do_save,    YELLOW,   148, 38).pack(side="left")
        btn(brow, "Cancel",           d.destroy,  BG_CARD2,  96, 38).pack(side="right")

    # ── SEARCH STUDENT ─────────────────────────────────────────────────────────
    def _dlg_search_student(self, course_name):
        d = self._make_dialog("Search Students", 480, 380)
        ctk.CTkFrame(d, fg_color=PURPLE, height=4, corner_radius=0).pack(fill="x")
        lbl(d, "  🔍  Search Students", 14, PURPLE, bold=True).pack(anchor="w", padx=20, pady=(12,4))
        hdiv(d)
        lbl(d, "Enter name, ID, or phone number:", 12, TXT2).pack(anchor="w", padx=20, pady=(6,2))
        e = entry(d, "Type to search...")
        e.pack(fill="x", padx=20, pady=(2,8))

        results_frame = ctk.CTkScrollableFrame(d, fg_color="transparent",
                                               scrollbar_button_color=PURPLE, height=200)
        results_frame.pack(fill="both", expand=True, padx=16, pady=4)
        count_lbl = lbl(d, "", 11, TXT2)
        count_lbl.pack(anchor="w", padx=20, pady=4)

        def do_search(*_):
            q = e.get().strip().lower()
            for w in results_frame.winfo_children():
                w.destroy()
            if not q:
                count_lbl.configure(text=""); return
            students = self.data.get(course_name, {}).get("students", [])
            matches = [s for s in students if
                       q in s.get("name","").lower() or
                       q in s.get("id","").lower()   or
                       q in s.get("phone","").lower()]
            count_lbl.configure(text=f"  Found {len(matches)} result(s).",
                                 text_color=GREEN if matches else RED)
            for s in matches:
                row = ctk.CTkFrame(results_frame, fg_color=BG_CARD2, corner_radius=6, height=34)
                row.pack(fill="x", pady=2)
                row.pack_propagate(False)
                ctk.CTkLabel(row, text=f"  {s['id']}", width=80, anchor="w",
                             font=("Segoe UI",11,"bold"), text_color=PURPLE).pack(side="left")
                ctk.CTkLabel(row, text=s["name"], width=160, anchor="w",
                             font=("Segoe UI",11), text_color=TXT).pack(side="left")
                ctk.CTkLabel(row, text=s["phone"], anchor="w",
                             font=("Segoe UI",11), text_color=TXT2).pack(side="left", padx=8)

        e.bind("<KeyRelease>", do_search)
        btn(d, "Search", do_search, PURPLE, 110, 36).pack(padx=20, anchor="w", pady=4)

    # ══════════════════════════════════════════════════════════════════════════
    #  COURSE MANAGEMENT DIALOGS
    # ══════════════════════════════════════════════════════════════════════════
    def _dlg_add_course(self):
        d = self._make_dialog("Add New Course", 420, 280)
        ctk.CTkFrame(d, fg_color=GREEN, height=4, corner_radius=0).pack(fill="x")
        lbl(d, "  ➕  Add New Course", 14, GREEN, bold=True).pack(anchor="w", padx=20, pady=(12,4))
        hdiv(d)
        lbl(d, "Course Name  *", 12, TXT2).pack(anchor="w", padx=20, pady=(8,2))
        name_e = entry(d, "e.g. B-Level")
        name_e.pack(fill="x", padx=20)
        lbl(d, "Description", 12, TXT2).pack(anchor="w", padx=20, pady=(10,2))
        desc_e = entry(d, "Short description of the course")
        desc_e.pack(fill="x", padx=20)

        msg = lbl(d, "", 11, TXT2)
        msg.pack(anchor="w", padx=20, pady=4)

        def do_add():
            name = name_e.get().strip()
            if not name:
                msg.configure(text="Course name is required.", text_color=RED); return
            if name in self.data:
                msg.configure(text=f"Course '{name}' already exists.", text_color=RED); return
            self.data[name] = {"students": []}
            COURSE_META[name] = {
                "color": random.choice([BLUE, CYAN, PURPLE, YELLOW, GREEN]),
                "icon": "📂",
                "desc": desc_e.get().strip() or "New Course",
            }
            save_data(self.data)
            d.destroy()
            self.show_home()

        brow = ctk.CTkFrame(d, fg_color="transparent")
        brow.pack(fill="x", padx=20, pady=10)
        btn(brow, "➕  Add Course", do_add,    GREEN,    140, 38).pack(side="left")
        btn(brow, "Cancel",         d.destroy,  BG_CARD2,  96, 38).pack(side="right")

    def _dlg_update_course(self):
        if not self.data:
            messagebox.showinfo("No Courses", "No courses available."); return
        d = self._make_dialog("Update Course", 420, 260)
        ctk.CTkFrame(d, fg_color=YELLOW, height=4, corner_radius=0).pack(fill="x")
        lbl(d, "  ✏️  Update Course", 14, YELLOW, bold=True).pack(anchor="w", padx=20, pady=(12,4))
        hdiv(d)
        lbl(d, "Select Course", 12, TXT2).pack(anchor="w", padx=20, pady=(8,2))
        cv = ctk.StringVar(value=list(self.data.keys())[0])
        ctk.CTkOptionMenu(d, values=list(self.data.keys()), variable=cv,
                          fg_color=BG_CARD2, button_color=YELLOW,
                          font=("Segoe UI",12), dynamic_resizing=False).pack(fill="x", padx=20)
        lbl(d, "New Description", 12, TXT2).pack(anchor="w", padx=20, pady=(10,2))
        desc_e = entry(d, "Updated description")
        desc_e.pack(fill="x", padx=20)

        def do_update():
            name = cv.get()
            desc = desc_e.get().strip()
            if name in COURSE_META and desc:
                COURSE_META[name]["desc"] = desc
            d.destroy()
            self.show_home()

        brow = ctk.CTkFrame(d, fg_color="transparent")
        brow.pack(fill="x", padx=20, pady=12)
        btn(brow, "💾  Save", do_update,  YELLOW,   120, 38).pack(side="left")
        btn(brow, "Cancel",   d.destroy,  BG_CARD2,  96, 38).pack(side="right")

    def _dlg_delete_course(self):
        if not self.data:
            messagebox.showinfo("No Courses", "No courses to delete."); return
        d = self._make_dialog("Delete Course", 420, 240)
        ctk.CTkFrame(d, fg_color=RED, height=4, corner_radius=0).pack(fill="x")
        lbl(d, "  🗑️  Delete Course", 14, RED, bold=True).pack(anchor="w", padx=20, pady=(12,4))
        hdiv(d)
        lbl(d, "Select Course to Delete", 12, TXT2).pack(anchor="w", padx=20, pady=(8,2))
        cv = ctk.StringVar(value=list(self.data.keys())[0])
        ctk.CTkOptionMenu(d, values=list(self.data.keys()), variable=cv,
                          fg_color=BG_CARD2, button_color=RED,
                          font=("Segoe UI",12), dynamic_resizing=False).pack(fill="x", padx=20)

        def do_delete():
            name  = cv.get()
            count = len(self.data.get(name,{}).get("students",[]))
            if not messagebox.askyesno("Confirm",
                    f"Delete course  '{name}'  and its {count} student record(s)?\nThis cannot be undone.",
                    parent=d):
                return
            del self.data[name]
            COURSE_META.pop(name, None)
            save_data(self.data)
            d.destroy()
            self.show_home()

        brow = ctk.CTkFrame(d, fg_color="transparent")
        brow.pack(fill="x", padx=20, pady=14)
        btn(brow, "🗑️  Delete", do_delete,  RED,       120, 38).pack(side="left")
        btn(brow, "Cancel",      d.destroy,  BG_CARD2,   96, 38).pack(side="right")


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
