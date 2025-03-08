import tkinter as tk
import mysql.connector as mc
import tkinter.simpledialog as simpledialog
from tkinter import messagebox
from datetime import datetime
import smtplib
import cv2
from PIL import Image
import random
import os
import string
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
dbCon = mc.connect(host="localhost", user="root", password="Vaibhav@1116", database="notes")
def create_user_table(user):
    cursor = dbCon.cursor()
    table_name = f"{user.lower()}"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, tname VARCHAR(255))")
    dbCon.commit()
    
def drop_user_table(user):
    cursor = dbCon.cursor()
    table_name = f"{user.lower()}"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    dbCon.commit()
def switch_user(*args):
    global current_user
    current_user = variable.get()
    if current_user == "Add new user":
        add_new_user()
    else:
        create_user_table(current_user)
        load_tasks()
def load_tasks():
    task_box.delete(0, tk.END)
    cursor = dbCon.cursor()
    table_name = f"{current_user.lower()}"
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for i, row in enumerate(rows, start=1):
        task_box.insert(tk.END, f"{i}. {row[1]}")
def add_task():
    task = entry_box.get()
    if task:
        cursor = dbCon.cursor()
        table_name = f"{current_user.lower()}"
        cursor.execute(f"INSERT INTO {table_name} (tname) VALUES (%s)", (task,))
        dbCon.commit()
        task_box.insert(tk.END, task)
        entry_box.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Enter a task first")
def delete_task():
    try:
        task_index = task_box.curselection()[0]
        item = task_box.get(task_index)
        cursor = dbCon.cursor()
        table_name = f"{current_user.lower()}"
        cursor.execute(f"DELETE FROM {table_name} WHERE tname = %s", (item,))
        dbCon.commit()
        task_box.delete(task_index)
    except:
        messagebox.showwarning("Error", "Select a task to delete")
def clear_tasks():
    cursor = dbCon.cursor()
    table_name = f"{current_user.lower()}"
    cursor.execute(f"TRUNCATE {table_name}")
    dbCon.commit()
    task_box.delete(0, tk.END)
def save_notes():
    filename = "notes.txt"
    with open(filename, "a") as file:
        file.write(f"\n\n***Task created by {current_user} [{datetime.now()}]:***\n")
        for task in task_box.get(0, tk.END):
            file.write("\t"+task + "\n")
    messagebox.showinfo("Notes Saved", f"Notes saved to {filename}")
def mail():
    # receiptant=current_user
    cur=dbCon.cursor()
    table_name=f"{current_user.lower()}"
    cur.execute("SELECT email FROM credentials WHERE username=%s",(current_user.lower(),))
    TempuserMail=cur.fetchone()
    # print(TempuserMail)
    userMail=TempuserMail[0]
    # print(userMail)
    curS=dbCon.cursor()
    curS.execute(f"SELECT * FROM {table_name}")
    lst=[]
    rows=cursor.fetchall()
    # print(len(rows))
    for row in rows:
        lst.append(row[1])
    # print(lst)
    noAffecRow=len(rows)
    taskNames=f"Hello {current_user}, \nyour {str(noAffecRow)} tasks as follow:"
    
    for j in lst:
        taskNames=taskNames+"\n"+"🔴 "+j+"."

    print(taskNames)
    msg = MIMEMultipart()
    msg['From'] = "vaibhavbhor473@gmail.com"
    msg['To'] = userMail
    msg['Subject'] = "Task notification"
    body = taskNames
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("vaibhavbhor473@gmail.com", "sokburqkxblkepfd")
    text = msg.as_string()
    server.sendmail("Stark industries.", userMail, text)
    server.quit()
    messagebox.showinfo("Done",f"Mail successfully sent to {userMail}.")
def exit_app():
    root.destroy()
# new_user=None
listbox=None
def add_new_user():
    # global new_user
    new_user = simpledialog.askstring("New User", "Enter new user name:")
    pwd=simpledialog.askstring("Password","Enter password:")
    email=simpledialog.askstring("Email","Enter email:")
    # global cloneNewUser
    # cloneNewUser=new_user
    print(new_user)
    if new_user and new_user not in names:
        names.append(new_user)
        cursor=dbCon.cursor()
        cursor.execute("INSERT INTO credentials VALUES(%s,%s,%s)",(new_user,pwd,email))
        dbCon.commit()
        messagebox.showinfo("New User.",f"{new_user} has been added.")
        variable.set(new_user)
        dp["menu"].add_command(label=new_user, command=tk._setit(variable, new_user))
        create_user_table(new_user)
        refresh_listbox()
def manage_users():
    password="Admin"
    toast=simpledialog.askstring("Admin action","Enter credentials :",show="*")
    if toast==password:
        
        global listbox
        user_window = tk.Toplevel(root)
        user_window.title("Manage Users")
        user_window.geometry("350x450")
        user_window.configure(bg="#f0e6d2") 

        tk.Label(user_window, text="User Management", bg="#f0e6d2", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(user_window, bg="#f0e6d2")
        frame.pack(pady=10)

        listbox = tk.Listbox(frame, width=30, height=10, font=("Arial", 11), bg="white", bd=2, relief="groove")
        listbox.pack(side="left", padx=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        for user in names:
            listbox.insert(tk.END, user)
            

        def delete_selected_user():
            try:
                selected_index = listbox.curselection()[0]
                selected_user = listbox.get(selected_index)
                ask = messagebox.askyesno("Warning", f"Do you really want to remove {selected_user}?")
                if ask:
                    choice = simpledialog.askstring("Authentication Required", f"Enter password of {selected_user}:", show="*")
                    anotherCursor = dbCon.cursor()
                    anotherCursor.execute("SELECT password FROM credentials WHERE username = %s", (selected_user,))
                    pwdOfUser = anotherCursor.fetchone()

                    if pwdOfUser and pwdOfUser[0] == choice:
                        cursor = dbCon.cursor()
                        names.remove(selected_user)
                        cursor.execute("DELETE FROM credentials WHERE username = %s", (selected_user,))
                        variable.set(names[0])
                        dp["menu"].delete(selected_user)
                        drop_user_table(selected_user)
                        listbox.delete(selected_index)
                        messagebox.showinfo("Success", f"{selected_user} has been removed.")
                    else:
                        messagebox.showerror("Error", "Incorrect password. Cannot delete user.")
            except IndexError:
                messagebox.showwarning("Error", "Select a user to delete")
        btn_frame = tk.Frame(user_window, bg="#f0e6d2")
        btn_frame.pack(pady=10)
        delete_btn = tk.Button(btn_frame, text="Delete User", command=delete_selected_user, 
                            bg="#d9534f", fg="white", font=("Arial", 11), width=12, relief="raised", bd=3)
        delete_btn.pack(side="left", padx=5)

        add_btn = tk.Button(btn_frame, text="Add User", command=add_new_user, 
                            bg="#5cb85c", fg="white", font=("Arial", 11), width=12, relief="raised", bd=3)
        add_btn.pack(side="left", padx=5)

        close_btn = tk.Button(btn_frame, text="Close", command=user_window.destroy, 
                            bg="#f0ad4e", fg="white", font=("Arial", 11), width=12, relief="raised", bd=3)
        close_btn.pack(side="left", padx=5)
        msg = MIMEMultipart()
        msg['From'] = "vaibhavbhor473@gmail.com"
        msg['To'] = "vaibhavbhor472@gmail.com"
        msg['Subject'] = "Successful login detected"

        body = f"Succesful login detected at {datetime.now()}"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("vaibhavbhor473@gmail.com", "sokburqkxblkepfd")
        text = msg.as_string()
        server.sendmail("Stark industries.", "vaibhavbhor472@gmail.com", text)
        server.quit()
    else:
        messagebox.showerror("Error","Login failed.")
        letters = string.ascii_letters
        numbers = string.digits
        random_name = ''.join(random.choice(letters + numbers) for _ in range(10))
        # print(random_name)
        # Initialize the webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open webcam")
            exit()

        # Capture a frame
        ret, frame = cap.read()

        if ret:
            # Convert OpenCV image (BGR) to RGB for Pillow
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to Pillow Image
            img = Image.fromarray(frame_rgb)

            # Save using Pillow
            img.save(f"{random_name}.jpg")
        else:
            print("Failed to capture image")

        cap.release()
        cv2.destroyAllWindows()
        msg = MIMEMultipart()
        msg['From'] = "vaibhavbhor473@gmail.com"
        msg['To'] = "vaibhavbhor472@gmail.com"
        msg['Subject'] = "Login failed"

        body = f"Failed login attempt at {datetime.now()}"
        msg.attach(MIMEText(body, 'plain'))
        imagePath=f"{random_name}.jpg"
        image = MIMEImage(open(imagePath, "rb").read())
        msg.attach(image)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("vaibhavbhor473@gmail.com", "myPassword")
        text = msg.as_string()
        server.sendmail("Stark industries.", "vaibhavbhor472@gmail.com", text)
        server.quit()
        os.remove(f"C:\\Users\\Vaibhav\\OneDrive\\Desktop\\final Touch\\{random_name}.jpg")
def refresh_listbox():
    global listbox
    listbox.delete(0, tk.END)
    for user in names:  
        listbox.insert(tk.END, user)    
import tkinter as tk
from tkinter import messagebox, simpledialog
root = tk.Tk()
root.title("To-Do List")
root.geometry("500x500")
root.configure(bg="#d3cce8")
cursor = dbCon.cursor()
cursor.execute("SELECT username FROM credentials")
namesList = cursor.fetchall()
names = [row[0] for row in namesList]
current_user = names[0]
task_frame = tk.Frame(root, bg="#d3cce3", bd=2, relief="groove")
task_frame.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(task_frame, text="📝 Tasks", font=("Arial", 14, "bold"), bg="#d3cce3").pack(pady=5)
task_box = tk.Listbox(task_frame, width=50, height=10, font=("Verdana", 11), bg="white", bd=2, relief="solid")
task_box.pack(padx=10, pady=5)
user_frame = tk.Frame(root, bg="#d3cce3", bd=2, relief="groove")
user_frame.pack(pady=10, padx=10, fill="x")
tk.Label(user_frame, text="Current User:", font=("Arial", 12, "bold"), bg="#d3cce3").pack(side=tk.LEFT, padx=5)
variable = tk.StringVar(root)
variable.set(names[0])
variable.trace("w", switch_user)
dp = tk.OptionMenu(user_frame, variable, *names)
dp.config(font=("Arial", 11), bg="white")
dp.pack(side=tk.LEFT, padx=5)
tk.Button(user_frame, text="Manage Users", command=manage_users, bg="#5d6dc5", fg="white", font=("Arial", 11, "bold"), bd=3, relief="raised").pack(side=tk.LEFT, padx=10)
entry_frame = tk.Frame(root, bg="#d3cce3", bd=2, relief="groove")
entry_frame.pack(pady=10, padx=10, fill="x")
entry_box = tk.Entry(entry_frame, width=35, font=("Arial", 12), bg="#fdf5e6", relief="solid", bd=2)
entry_box.pack(pady=10, padx=10, side=tk.LEFT)
tk.Button(entry_frame, text="Add Task", command=add_task, bg="#4caf50", fg="white", font=("Arial", 11, "bold"), bd=3, relief="raised").pack(side=tk.LEFT, padx=5)
btn_frame = tk.Frame(root, bg="#d3cce3", bd=2, relief="groove")
btn_frame.pack(pady=10, padx=10, fill="x")
tk.Button(btn_frame, text="Delete Task", command=delete_task, bg="#ff9800", fg="white", font=("Arial", 11, "bold"), bd=3, relief="raised").pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear Tasks", command=clear_tasks, bg="#f44336", fg="white", font=("Arial", 11, "bold"), bd=3, relief="raised").pack(side="left", padx=5)
tk.Button(btn_frame, text="Save Notes", command=save_notes, bg="#9c27b0", fg="white", font=("Arial", 11, "bold"), bd=3, relief="raised").pack(side="left", padx=5)
tk.Button(btn_frame, text="Send mail", command=mail, bg="#00bcd4", fg="black", font=("Arial", 11, "bold"), bd=3, relief="raised").pack(side="left", padx=5)
tk.Button(btn_frame, text="Exit", command=exit_app, bg="#616161", fg="white", font=("Arial", 11, "bold"), bd=3, relief="raised").pack(side="left", padx=5)
create_user_table(current_user)
load_tasks()
root.mainloop()