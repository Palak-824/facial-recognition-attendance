import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from tkcalendar import Calendar
import requests

Video_Index = 0
############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

###################################################################################

def check_haarcascadefile(window):
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

###################################################################################

def save_pass():
    assure_path_exists("training_image_pro/")
    exists1 = os.path.isfile("training_image_pro/psd.txt")
    if exists1:
        tf = open("training_image_pro/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("training_image_pro/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("training_image_pro/psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#####################################################################################

def psw(window,message,message1):
    assure_path_exists("training_image_pro/")
    exists1 = os.path.isfile("training_image_pro/psd.txt")
    if exists1:
        tf = open("training_image_pro/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("training_image_pro/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages(window,message,message1)
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################################################################

def clear(txt,message1):
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2(txt2, message1):
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

#######################################################################################

def TakeImages(window,txt,txt2,message,message1,trainImg):
    check_haarcascadefile(window)
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("student_details/")
    assure_path_exists("training_image_pro/")
    serial = 0
    exists = os.path.isfile("student_details/student_details.csv")
    if exists:
        with open("student_details/student_details.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("student_details/student_details.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(Video_Index)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = detector.detectMultiScale(gray, 1.1, 5,minSize=(100,100))
            for (x, y, w, h) in faces:
                
                face = cv2.resize(gray[y:y + h, x:x + w], (200, 200)) 
                
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("captured_image/ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",face)
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(150) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 150:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('student_details/student_details.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)
    trainImg.config(state=tk.NORMAL)

########################################################################################

def TrainImages(window,message,message1):
    check_haarcascadefile(window)
    assure_path_exists("training_image_pro/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("training_image_pro/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages(window, tv):
    check_haarcascadefile(window)
    assure_path_exists("attendance/")
    assure_path_exists("student_details/")

    for k in tv.get_children():
        tv.delete(k)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.isfile("training_image_pro/Trainner.yml"):
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    recognizer.read("training_image_pro/Trainner.yml")

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(Video_Index)  # Ensure correct camera index
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Intime', 'Outtime']

    if not os.path.isfile("student_details/student_details.csv"):
        mess._show(title='Details Missing', message='Employees details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        return

    df = pd.read_csv("student_details/student_details.csv")
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    attendance_file = f"attendance/attendance_{date}.csv"

    # Load existing attendance records into memory
    attendance_data = {}
    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if row and row[0] != 'Id':
                    attendance_data[row[0]] = row

    while True:
        ret, im = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            face_resized = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            serial, conf = recognizer.predict(face_resized)

            if conf < 60:
                ts = time.time()
                curtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID).strip("[]")
                bb = str(aa).strip("[]").strip("'")

                if ID in attendance_data:
                    attendance_data[ID][-1] = curtime  # Update outtime
                else:
                    new_record = [str(ID), bb, date, curtime, curtime]
                    attendance_data[ID] = new_record

                cv2.putText(im, f"ID: {ID} Name: {bb}", (x, y + h), font, 1, (255, 255, 255), 2)
            else:
                cv2.putText(im, "Unknown", (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)

        # Update the treeview continuously
        for k in tv.get_children():
            tv.delete(k)
        for record in attendance_data.values():
            j = len(tv.get_children()) + 1
            iidd = str(record[0]) + '   '
            ch(j, tv, iidd, record)

        tv.tag_configure('gray', background="#ebf7bc")
        tv.tag_configure('green', background="#cfec9a")

        # Write attendance data back to the file
        with open(attendance_file, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(col_names)
            writer.writerows(attendance_data.values())

        if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
            break

    cam.release()
    cv2.destroyAllWindows()

def show_attendance():
    def get_date():
        """Fetch the selected date from the calendar and close the window"""
        selected_date = cal.get_date()  # Format: 'dd-mm-yyyy'
        top.destroy()  # Close the calendar window
        fetch_attendance(selected_date)

    def fetch_attendance(formatted_date):
        """Calls the API to get attendance data and displays it"""
        api_url = f"http://127.0.0.1:5000/get-attendance?date={formatted_date}"

        try:
            response = requests.get(api_url)
            
            if response.status_code == 200:
                attendance_data = response.json()
                if attendance_data:
                    display_attendance(attendance_data, formatted_date)
                else:
                    display_attendance([], formatted_date)

            else:
                # display_attendance(f"API Call Failed: {response.status_code} - {response.text}")
                display_attendance(f"No records found for {date}")

        except requests.exceptions.RequestException as e:
            display_attendance(f"Error making API call: {e}")

    def display_attendance(data, date):
        """Displays attendance data in a new Tkinter window"""
        result_window = tk.Toplevel()
        result_window.title(f"Attendance Data - {date}")

        if not data:
            tk.Label(result_window, text=f"No records found for {date}").pack(pady=10)
        else:
            tree = ttk.Treeview(result_window, columns=('ID', 'Name'), show='headings')
            tree.heading('ID', text='ID')
            tree.heading('Name', text='Name')
            tree.pack(fill='both', expand=True)

            for record in data:
                tree.insert("", "end", values=(
                    record.get('Id', ''),
                    record.get('Name', '')
                ))

        tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=5)

    # Create a pop-up window for date selection
    top = tk.Toplevel()
    top.title("Select Date")

    cal = Calendar(top, selectmode="day", date_pattern="dd-mm-yyyy")
    cal.pack(padx=20, pady=20)

    btn_select = tk.Button(top, text="Fetch", command=get_date)
    btn_select.pack(pady=10)

#################################################################################

def att(tv):
    col_names = ['Id', 'Name', 'Date', 'InTime', 'OutTime']
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("attendance/attendance_" + date + ".csv")
    attendance_file = f"attendance/attendance_{date}.csv"
    existing_records = []
    if os.path.isfile(attendance_file):
        with open(attendance_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            existing_records = list(reader)
    for record in existing_records:
        if record and record[0] != 'Id':  # Skip header row
            j += 1
            iidd = str(record[0]) + '   '
            ch(j, tv, iidd, record)
    tv.tag_configure('gray', background="#ebf7bc")
    tv.tag_configure('green', background="#cfec9a")

#################################################################################

def ch(j,tv,iidd,lines):
    if j % 2==0:
        tv.insert('', 0, text=iidd, 
                values=(str(lines[1]), str(lines[2]), str(lines[3]), str(lines[4])), tags=['gray'])
    else:
        tv.insert('', 0, text=iidd,
                values=(str(lines[1]), str(lines[2]), str(lines[3]), str(lines[4])), tags=['green'])

##################################################################################
def psw_quit(window):
    assure_path_exists("training_image_pro/")
    exists1 = os.path.isfile("training_image_pro/psd.txt")
    if exists1:
        tf = open("training_image_pro/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("training_image_pro/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        window.destroy()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

# ======================== CONTACT FUNCTION ========================

def contact():
    """Display contact information"""
    mess.showinfo("Contact Support", 
                "For assistance contact:\nEmail: support@skit.ac.in\nPhone: +91 12345 67890")
    

# ======================== MANUAL ENTRY =================================

from tkinter import messagebox, simpledialog

def verify_admin_password():
    password = simpledialog.askstring("Admin Authentication", "Enter Admin Password:", show='*')
    return password == "fer"  # Change to your preferred password

def manual_attendance_entry(root, callback=None):
    if not verify_admin_password():
        messagebox.showerror("Error", "Incorrect Admin Password")
        return
    
    manual_window = tk.Toplevel(root)
    manual_window.title("Manual Attendance Entry")
    
    # Store selected date
    selected_date = tk.StringVar(value=datetime.datetime.now().strftime("%d-%m-%Y"))
    
    # ID Entry
    tk.Label(manual_window, text="Student ID:").grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(manual_window)
    id_entry.grid(row=0, column=1, padx=10, pady=5)
    
    # Name Entry
    tk.Label(manual_window, text="Student Name:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(manual_window)
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    
    # Date Selection Button
    def pick_date():
        def set_date():
            selected_date.set(cal.get_date())
            top.destroy()
        
        top = tk.Toplevel(manual_window)
        cal = Calendar(top, selectmode='day', date_pattern='dd-mm-yyyy')
        cal.pack(padx=10, pady=10)
        tk.Button(top, text="Select Date", command=set_date).pack(pady=10)
    
    tk.Label(manual_window, text="Attendance Date:").grid(row=2, column=0, padx=10, pady=5)
    date_btn = tk.Button(manual_window, 
                        textvariable=selected_date, 
                        command=pick_date,
                        relief=tk.RAISED,
                        padx=10,
                        pady=5)
    date_btn.grid(row=2, column=1, padx=10, pady=5)
    
    # Submit Button
    def submit():
        student_id = id_entry.get()
        name = name_entry.get()
        date_str = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        
        if not all([student_id, name]):
            messagebox.showerror("Error", "Student ID and Name are required!")
            return
        
        try:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            filename = f"attendance/attendance_{date_str}.csv"
            
            os.makedirs("Attendance", exist_ok=True)
            
            try:
                df = pd.read_csv(filename)
            except FileNotFoundError:
                df = pd.DataFrame(columns=['Id', 'Name', 'Date', 'Intime', 'Outtime'])
            
            mask = (df['Id'].astype(str).str.lower() == student_id.lower()) & (df['Date'].astype(str) == date_str)
            
            if any(mask):
                if pd.notna(df.loc[mask, 'Intime'].values[0]):
                    df.loc[mask, 'Outtime'] = current_time
                    message = f"Out time updated for {name} ({student_id})"
                else:
                    df.loc[mask, 'Intime'] = current_time
                    message = f"In time updated for {name} ({student_id})"
            else:
                new_entry = {
                    'Id': student_id,
                    'Name': name,
                    'Date': date_str,
                    'Intime': current_time,
                    'Outtime': current_time
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                message = f"Attendance marked for {name} ({student_id})"
            
            df.to_csv(filename, index=False)
            messagebox.showinfo("Success", message)
            manual_window.destroy()
            if callback:
                callback()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")
            import traceback
            traceback.print_exc()
    
    tk.Button(manual_window, text="Submit", command=submit).grid(row=3, columnspan=2, pady=10)

def generate_report():
    def calculate_attendance():
        # Get user inputs
        selected_month = month_var.get()
        working_days = tsd.askinteger("Working Days", "Enter total working days:", 
                                    parent=report_window, minvalue=1)
        
        if not working_days or working_days < 1 or working_days > 31:
            mess.showerror("Error", "Invalid working days input")
            return

        # Read student details
        students = {}
        try:
            with open('student_details/student_details.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    students[row['ID']] = {
                        'name': row['NAME'],
                        'present_days': 0
                    }
        except FileNotFoundError:
            mess.showerror("Error", "Student database not found!")
            return

        # Process attendance files
        attendance_dir = 'attendance'
        processed_dates = set()
        
        for filename in os.listdir(attendance_dir):
            if filename.startswith('attendance_') and filename.endswith('.csv'):
                try:
                    # Extract date from filename (format: dd-mm-yyyy)
                    date_str = filename.split('_')[1].split('.')[0]
                    file_month = date_str.split('-')[1]
                    
                    if file_month != selected_month.split('-')[1]:
                        continue
                    
                    # Track unique dates to prevent duplicate processing
                    if date_str in processed_dates:
                        continue
                    processed_dates.add(date_str)

                    # Process daily attendance
                    with open(os.path.join(attendance_dir, filename), 'r') as file:
                        reader = csv.DictReader(file)
                        daily_present = set()
                        
                        for row in reader:
                            student_id = row['Id'].strip()
                            if student_id in students:
                                daily_present.add(student_id)

                        # Update present days
                        for student_id in daily_present:
                            students[student_id]['present_days'] += 1

                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    continue

        # Create report window
        result_window = tk.Toplevel(report_window)
        result_window.title(f"Attendance Report - {selected_month}")
        result_window.geometry("780x500")

        # Create treeview with scrollbar
        tree_frame = tk.Frame(result_window)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Present', 'Percentage'), show='headings')
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Configure columns
        tree.heading('ID', text='Student ID', anchor='center')
        tree.heading('Name', text='Name', anchor='w')
        tree.heading('Present', text='Days Present', anchor='center')
        tree.heading('Percentage', text='Attendance %', anchor='center')
        
        tree.column('ID', width=120, anchor='center')
        tree.column('Name', width=250, anchor='w')
        tree.column('Present', width=150, anchor='center')
        tree.column('Percentage', width=150, anchor='center')

        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        # Add data
        for student_id, data in students.items():
            percentage = (data['present_days'] / working_days) * 100 if working_days > 0 else 0
            tree.insert('', 'end', values=(
                student_id,
                data['name'],
                data['present_days'],
                f"{percentage:.2f}%"
            ))

        # Add export button
        export_btn = ttk.Button(result_window, text="Export to CSV", 
                              command=lambda: export_report(students, selected_month, working_days))
        export_btn.pack(pady=10)
        
    def export_report(data, month, working_days):
        # Create directory if it doesn't exist
        os.makedirs('attendance_report', exist_ok=True)
        
        filename = os.path.join('attendance_report', f"Attendance_Report_{month}.csv")
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Student ID', 'Name', 'Days Present', 'Attendance %', 'Working Days'])
            
            for student_id, details in data.items():
                percentage = (details['present_days'] / working_days) * 100 if working_days > 0 else 0
                writer.writerow([
                    student_id,
                    details['name'],
                    details['present_days'],
                    f"{percentage:.2f}%",
                    working_days
                ])
        
        mess.showinfo("Success", f"Report exported as {filename}")

    # Month selection dialog
    report_window = tk.Toplevel()
    report_window.title("Generate Monthly Report")
    
    # Generate valid months from existing attendance files
    months = set()
    for filename in os.listdir('attendance'):
        if filename.startswith('attendance_'):
            date_part = filename.split('_')[1].split('.')[0]
            month_year = f"{date_part.split('-')[2]}-{date_part.split('-')[1]}"  # yyyy-mm format
            months.add(month_year)
    
    if not months:
        mess.showerror("Error", "No attendance records found!")
        report_window.destroy()
        return
    
    # GUI elements
    tk.Label(report_window, text="Select Month (YYYY-MM):", font=('Helvetica', 12)).pack(padx=75, pady=25)
    
    month_var = tk.StringVar()
    month_combo = ttk.Combobox(report_window, 
                             textvariable=month_var, 
                             values=sorted(months),
                             state="readonly",
                             font=('Helvetica', 12))
    month_combo.pack(padx=30, pady=20)
    
    ttk.Button(report_window, text="Generate Report", 
             command=calculate_attendance).pack(pady=20)