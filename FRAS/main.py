from services.services import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import os
import csv
from PIL import Image, ImageTk
import time
import logging
from api.attendance_api import flask_server  # Import the FlaskServer instance

# Start Flask server in a new thread
flask_server.start()

# Constants
Video_Index = 0
COLLEGE_LOGO = "helper_anime\\skit_logo.png"  # Path to college logo
BG_COLOR = "#f8f9fa"  # Light gray background
PRIMARY_COLOR = "#0056b3"  # Deep blue (SKIT brand color)
SECONDARY_COLOR = "#6c757d"  # Gray for secondary elements
ACCENT_COLOR = "#dc3545"  # Red for important actions
TEXT_COLOR = "#212529"  # Dark gray for text
LIGHT_TEXT = "#f8f9fa"  # Light text for dark backgrounds

# Font styles
TITLE_FONT = ('Helvetica', 24, 'bold')
HEADER_FONT = ('Helvetica', 16, 'bold')
BODY_FONT = ('Helvetica', 12)
BUTTON_FONT = ('Helvetica', 12, 'bold')

# Logging configuration
LOG_FILE = "logs/app_log.txt"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

############################################# FUNCTIONS ################################################

def log(level, message):
    if level == "ERROR":
        logging.error(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "INFO":
        logging.info(message)
    else:
        logging.debug(message)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

def changeOnHover(button, colorOnHover, colorOnLeave, fontcOnHover, fontcOnLeave):
    button.bind("<Enter>", func=lambda e: button.config(
        background=colorOnHover, fg=fontcOnHover) if (button['state'] != "disabled") else None)
    button.bind("<Leave>", func=lambda e: button.config(
        background=colorOnLeave, fg=fontcOnLeave))

def create_rounded_button(parent, text, command, **kwargs):
    """Create a modern rounded button"""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bd=0,
        highlightthickness=0,
        relief=tk.FLAT,
        font=BUTTON_FONT,
        padx=kwargs.pop('padx', 20),
        pady=kwargs.pop('pady', 8),
        **kwargs
    )
    return btn

def show_gif(after_gif_callback):
    gif_window = tk.Toplevel(window)
    gif_window.title("Tutorial Guide")
    gif_window.geometry("500x500")
    gif_window.configure(bg=BG_COLOR)
    gif_window.resizable(False, False)

    # Header
    header_frame = tk.Frame(gif_window, bg=PRIMARY_COLOR)
    header_frame.pack(fill='x')
    
    tk.Label(
        header_frame,
        text="Tutorial Guide",
        font=HEADER_FONT,
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        pady=10
    ).pack()

    # GIF Content
    content_frame = tk.Frame(gif_window, bg=BG_COLOR)
    content_frame.pack(pady=20)

    try:
        gif_path = "helper_anime\\tutorial.gif" 
        gif_image = Image.open(gif_path)
        gif_label = tk.Label(content_frame, bg=BG_COLOR)
        gif_label.pack()
    except:
        tk.Label(
            content_frame,
            text="Tutorial content not available",
            font=BODY_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()
        gif_image = None

    def animate_gif(count=0):
        if gif_image:
            frame = count % gif_image.n_frames 
            gif_image.seek(frame)
            gif_photo = ImageTk.PhotoImage(gif_image)
            gif_label.config(image=gif_photo)
            gif_label.image = gif_photo
            gif_window.after(100, animate_gif, count + 1)

    animate_gif()

    # Footer with button
    footer_frame = tk.Frame(gif_window, bg=BG_COLOR)
    footer_frame.pack(pady=20)

    ok_button = create_rounded_button(
        footer_frame,
        text="OK",
        command=lambda: [gif_window.destroy(), after_gif_callback()],
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        activebackground="#003d7a",
        activeforeground=LIGHT_TEXT
    )
    ok_button.pack()
    changeOnHover(ok_button, "#003d7a", PRIMARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)

    gif_window.transient(window)
    gif_window.grab_set()

def psw_admin():
    """Password verification for admin access"""
    assure_path_exists("training_image_pro/")
    exists1 = os.path.isfile("training_image_pro/psd.txt")

    if exists1:
        tf = open("training_image_pro/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Password Setup', 'Please set a new admin password:', show='*')
        if not new_pas:
            mess.showerror('Password Required', 'Please provide the essential field: Password')
            log("ERROR", "Password setup aborted: no input provided.")
            return
        tf = open("training_image_pro/psd.txt", "w")
        tf.write(new_pas)
        mess.showinfo('Password Set', 'Admin password was set successfully')
        log("INFO", "Admin password set successfully.")
        return

    password = tsd.askstring('Admin Authentication', 'Enter Admin Password:', show='*')
    if not password:
        mess.showerror('Access Denied', 'Please provide the essential field: Password')
        log("ERROR", "Empty password attempt during admin login.")
        return

    if password == key:
        log("INFO", "Admin login successful.")
        admin()
    else:
        mess.showerror('Access Denied', 'Incorrect password')
        log("WARNING", "Incorrect password entered for admin.")

def validate_and_capture(id_entry, name_entry, message, status_msg, train_img_btn):
    student_id = id_entry.get().strip()
    student_name = name_entry.get().strip()

    if not student_id or not student_name:
        mess.showerror("Missing Information", "Please provide all essential fields: ID and Name")
        log("WARNING", "Missing ID or Name during student image capture.")
        return

    log("INFO", f"Captured ID and Name: {student_id}, {student_name}")
    show_gif(lambda: TakeImages(window, id_entry, name_entry, message, status_msg, train_img_btn))

def admin():
    """Admin panel window"""
    admin_window = tk.Toplevel(window)
    admin_window.title("Admin Panel - SKIT Jaipur")
    admin_window.geometry("900x650")
    admin_window.configure(bg=BG_COLOR)
    admin_window.resizable(False, False)
    
    # Header
    header_frame = tk.Frame(admin_window, bg=PRIMARY_COLOR)
    header_frame.pack(fill='x')
    
    tk.Label(
        header_frame,
        text="Admin Panel - SKIT Jaipur",
        font=HEADER_FONT,
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        pady=12
    ).pack()
    
    # Main Content
    main_frame = tk.Frame(admin_window, bg=BG_COLOR)
    main_frame.pack(pady=20, padx=20, fill='both', expand=True)
    
    # Registration Section
    reg_frame = tk.LabelFrame(
        main_frame,
        text=" New Student Registration ",
        font=BODY_FONT,
        bg=BG_COLOR,
        fg=PRIMARY_COLOR,
        padx=20,
        pady=20
    )
    reg_frame.pack(fill='both', expand=True, pady=(0, 20))
    
    # Form Fields
    fields_frame = tk.Frame(reg_frame, bg=BG_COLOR)
    fields_frame.pack()
    
    # ID Field
    tk.Label(
        fields_frame,
        text="Student ID:",
        font=BODY_FONT,
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    
    id_entry = tk.Entry(
        fields_frame,
        font=BODY_FONT,
        width=30,
        bd=1,
        relief=tk.SOLID
    )
    id_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # Name Field
    tk.Label(
        fields_frame,
        text="Student Name:",
        font=BODY_FONT,
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    
    name_entry = tk.Entry(
        fields_frame,
        font=BODY_FONT,
        width=30,
        bd=1,
        relief=tk.SOLID
    )
    name_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Status Message
    status_msg = tk.Label(
        reg_frame,
        text="Steps: 1) Take Images  →  2) Save Profile",
        font=BODY_FONT,
        bg=BG_COLOR,
        fg=SECONDARY_COLOR
    )
    status_msg.pack(pady=(10, 20))
    
    # Action Buttons
    buttons_frame = tk.Frame(reg_frame, bg=BG_COLOR)
    buttons_frame.pack()
    
    # Clear Buttons
    clear_frame = tk.Frame(buttons_frame, bg=BG_COLOR)
    clear_frame.grid(row=0, column=0, padx=10)
    
    clear_id_btn = create_rounded_button(
        clear_frame,
        text="Clear ID",
        command=lambda: clear(id_entry, status_msg),
        bg=SECONDARY_COLOR,
        fg=LIGHT_TEXT
    )
    clear_id_btn.pack(side='left', padx=5)
    changeOnHover(clear_id_btn, "#5a6268", SECONDARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)
    
    clear_name_btn = create_rounded_button(
        clear_frame,
        text="Clear Name",
        command=lambda: clear2(name_entry, status_msg),
        bg=SECONDARY_COLOR,
        fg=LIGHT_TEXT
    )
    clear_name_btn.pack(side='left', padx=5)
    changeOnHover(clear_name_btn, "#5a6268", SECONDARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)
    
    # Main Action Buttons
    action_frame = tk.Frame(buttons_frame, bg=BG_COLOR)
    action_frame.grid(row=1, column=0, pady=20)
    
    take_img_btn = create_rounded_button(
        action_frame,
        text="Take Student Images",
        command=lambda: validate_and_capture(id_entry, name_entry, message, status_msg, train_img_btn),
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        padx=30
    )
    take_img_btn.grid(row=0, column=0, padx=10, pady=5)
    changeOnHover(take_img_btn, "#003d7a", PRIMARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)
    
    train_img_btn = create_rounded_button(
        action_frame,
        text="Save Student Profile",
        command=lambda: psw(window, message, status_msg),
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        padx=30,
        state="disabled"
    )
    train_img_btn.grid(row=1, column=0, padx=10, pady=5)
    changeOnHover(train_img_btn, "#003d7a", PRIMARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)
    
    # Admin Tools Section
    tools_frame = tk.LabelFrame(
        main_frame,
        text=" Administration Tools ",
        font=BODY_FONT,
        bg=BG_COLOR,
        fg=PRIMARY_COLOR,
        padx=20,
        pady=20
    )
    tools_frame.pack(fill='both', expand=True)
    
    tools_buttons_frame = tk.Frame(tools_frame, bg=BG_COLOR)
    tools_buttons_frame.pack()
    
    attendance_btn = create_rounded_button(
        tools_buttons_frame,
        text="View Attendance Records",
        command=lambda: show_attendance(),
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        padx=20
    )
    attendance_btn.pack(side='left', padx=10, pady=5)
    changeOnHover(attendance_btn, "#003d7a", PRIMARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)
    
    manual_btn = create_rounded_button(
        tools_buttons_frame,
        text="Manual Entry",
        command=lambda: manual_attendance_entry(window, callback=show_attendance),
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        padx=20
    )
    manual_btn.pack(side='left', padx=10, pady=5)
    changeOnHover(manual_btn, "#5a6268", SECONDARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)

    report_btn = create_rounded_button(
        tools_buttons_frame,
        text="Generate attendance report",
        command=lambda: generate_report(),
        bg=PRIMARY_COLOR,
        fg=LIGHT_TEXT,
        padx=20
    )
    report_btn.pack(side='left', padx=10, pady=5)
    changeOnHover(report_btn, "#5a6268", SECONDARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)

def on_exit():
    if mess.askyesno("Confirm Exit", "Are you sure you want to exit the system?"):
        try:
            flask_server.shutdown()
            log("INFO", "Flask server shut down successfully.")
        except Exception as e:
            log("ERROR", f"Error shutting down Flask server: {e}")
        finally:
            # Delay destroy slightly to let all GUI events finish
            window.after(100, window.destroy)


############################################# MAIN WINDOW ################################################

window = tk.Tk()
window.geometry("1200x700")
window.title("SKIT Jaipur - Face Recognition Attendance System")
window.configure(background=BG_COLOR)
window.resizable(False, False)

# Add college logo and header
header_frame = tk.Frame(window, bg=PRIMARY_COLOR)
header_frame.pack(fill='x')

try:
    logo_img = Image.open(COLLEGE_LOGO)
    logo_img = logo_img.resize((80, 80), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_photo, bg=PRIMARY_COLOR)
    logo_label.image = logo_photo
    logo_label.pack(side='left', padx=20, pady=10)
except:
    pass  # Continue without logo if not found

# College name and title
title_frame = tk.Frame(header_frame, bg=PRIMARY_COLOR)
title_frame.pack(side='left', padx=10)

tk.Label(
    title_frame,
    text="Swami Keshvanand Institute of Technology",
    font=('Helvetica', 16, 'bold'),
    bg=PRIMARY_COLOR,
    fg=LIGHT_TEXT
).pack(anchor='w')

tk.Label(
    title_frame,
    text="Face Recognition Attendance System",
    font=('Helvetica', 14),
    bg=PRIMARY_COLOR,
    fg=LIGHT_TEXT
).pack(anchor='w')

# Date and time
datetime_frame = tk.Frame(header_frame, bg=PRIMARY_COLOR)
datetime_frame.pack(side='right', padx=20)

datef = tk.Label(
    datetime_frame,
    text=f"{day}-{mont[month]}-{year}   |   ",
    font=('Helvetica', 12),
    bg=PRIMARY_COLOR,
    fg=LIGHT_TEXT
)
datef.pack(side='left', pady=10)

clock = tk.Label(
    datetime_frame,
    font=('Helvetica', 12),
    bg=PRIMARY_COLOR,
    fg=LIGHT_TEXT
)
clock.pack(side='left', pady=10)
tick()

# Main content area
main_frame = tk.Frame(window, bg=BG_COLOR)
main_frame.pack(fill='both', expand=True, padx=20, pady=20)

# Registered students section
registered_frame = tk.LabelFrame(
    main_frame,
    text=" Attendance Management ",
    font=HEADER_FONT,
    bg=BG_COLOR,
    fg=PRIMARY_COLOR,
    padx=20,
    pady=20
)
registered_frame.pack(fill='both', expand=True)

# Status message
# Initialize attendance data
res = 0
exists = os.path.isfile("student_details/student_details.csv")
if exists:
    with open("student_details/student_details.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2)
    csvFile1.close()
else:
    res = 0
message = tk.Label(
    registered_frame,
    text=f"Total Registrations: {res}",
    font=BODY_FONT,
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
message.pack(anchor='w', pady=(0, 10))

# Attendance table
table_frame = tk.Frame(registered_frame, bg=BG_COLOR)
table_frame.pack(fill='both', expand=True)

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview.Heading", 
               background=PRIMARY_COLOR, 
               foreground=LIGHT_TEXT, 
               font=BUTTON_FONT,
               padding=10)
style.configure("Treeview", 
               background=BG_COLOR, 
               fieldbackground=BG_COLOR, 
               font=BODY_FONT,
               rowheight=30)
style.map("Treeview", 
          background=[('selected', '#e2e6ea')],
          foreground=[('selected', TEXT_COLOR)])

tv = ttk.Treeview(
    table_frame, 
    height=12, 
    columns=('name', 'date', 'intime', 'outtime'),
    selectmode='extended'
)
tv.column('#0', width=150, anchor='w')
tv.column('name', width=200, anchor='w')
tv.column('date', width=150, anchor='center')
tv.column('intime', width=150, anchor='center')
tv.column('outtime', width=150, anchor='center')

tv.heading('#0', text='ID', anchor='center')
tv.heading('name', text='STUDENT NAME', anchor='center')
tv.heading('date', text='DATE', anchor='center')
tv.heading('intime', text='IN TIME', anchor='center')
tv.heading('outtime', text='OUT TIME', anchor='center')

tv.pack(side='left', fill='both', expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tv.yview)
scrollbar.pack(side='right', fill='y')
tv.configure(yscrollcommand=scrollbar.set)

# Action buttons
button_frame = tk.Frame(registered_frame, bg=BG_COLOR)
button_frame.pack(fill='x', pady=(20, 0))

take_attendance_btn = create_rounded_button(
    button_frame,
    text="Take Attendance",
    command=lambda: TrackImages(window, tv),
    bg=PRIMARY_COLOR,
    fg=LIGHT_TEXT,
    padx=30
)
take_attendance_btn.pack(side='left', padx=10)
changeOnHover(take_attendance_btn, "#003d7a", PRIMARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)

admin_btn = create_rounded_button(
    button_frame,
    text="Admin Panel",
    command=psw_admin,
    bg=SECONDARY_COLOR,
    fg=LIGHT_TEXT,
    padx=30
)
admin_btn.pack(side='left', padx=10)
changeOnHover(admin_btn, "#5a6268", SECONDARY_COLOR, LIGHT_TEXT, LIGHT_TEXT)

quit_btn = create_rounded_button(
    button_frame,
    text="Exit System",
    command=on_exit,
    bg=ACCENT_COLOR,
    fg=LIGHT_TEXT,
    padx=30
)
quit_btn.pack(side='right', padx=10)
changeOnHover(quit_btn, "#c82333", ACCENT_COLOR, LIGHT_TEXT, LIGHT_TEXT)

# Menu bar
menubar = tk.Menu(window, relief='flat', bg=BG_COLOR, fg=TEXT_COLOR, activebackground=PRIMARY_COLOR)
filemenu = tk.Menu(menubar, tearoff=0, bg=BG_COLOR, fg=TEXT_COLOR)
filemenu.add_command(
    label='Change Password', 
    command=change_pass,
    font=BODY_FONT
)
filemenu.add_command(
    label='Contact Support', 
    command=contact,
    font=BODY_FONT
)
filemenu.add_separator()
filemenu.add_command(
    label='Exit', 
    command=window.destroy,
    font=BODY_FONT
)
menubar.add_cascade(
    label='Help', 
    menu=filemenu
)

att(tv)
window.configure(menu=menubar)
window.mainloop()