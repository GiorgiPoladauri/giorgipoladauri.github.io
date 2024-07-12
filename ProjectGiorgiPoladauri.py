import tkinter as tk
from tkinter import messagebox, PhotoImage, scrolledtext
import sqlite3

# Database setup
def create_database():
    conn = sqlite3.connect('AramiantHospital.db')
    c = conn.cursor()
    
    # Admin table
    c.execute('''CREATE TABLE IF NOT EXISTS Admins (
                 Id INTEGER PRIMARY KEY,
                 Username TEXT NOT NULL,
                 Password TEXT NOT NULL)''')
    
    # Patient table
    c.execute('''CREATE TABLE IF NOT EXISTS Patients (
                 Id INTEGER PRIMARY KEY,
                 Private_Number TEXT NOT NULL UNIQUE,
                 Name TEXT NOT NULL,
                 Surname TEXT NOT NULL,
                 Password TEXT NOT NULL,
                 Birthday TEXT NOT NULL,
                 Health_Info TEXT,
                 Total_Bills REAL,
                 Last_Visit TEXT)''')
    
    # Doctor table
    c.execute('''CREATE TABLE IF NOT EXISTS doctors (
                 Id INTEGER PRIMARY KEY,
                 Name TEXT NOT NULL,
                 Surname TEXT NOT NULL,
                 Profession TEXT NOT NULL,
                 Phone TEXT)''')
    
    # Pre-insert an admin
    c.execute("INSERT OR IGNORE INTO Admins (Id, Username, Password) VALUES (1, 'Admin', 'Adminashvili')")
    
    conn.commit()
    conn.close()

# Function to switch to admin login page
def show_admin_login():
    clear_screen()
    tk.Label(root, text="ადმინის ავტორიზაცია", bg="dodgerblue", fg="white", font=("Helvetica", 24)).pack(pady=20)
    tk.Label(root, text="მომხმარებლის სახელი:", bg="dodgerblue", fg="white", font=("Helvetica", 16)).pack(pady=10)
    
    global admin_username_entry
    admin_username_entry = tk.Entry(root, font=("Helvetica", 16))
    admin_username_entry.pack(pady=10)
    
    tk.Label(root, text="პაროლი:", bg="dodgerblue", fg="white", font=("Helvetica", 16)).pack(pady=10)
    
    global admin_password_entry
    admin_password_entry = tk.Entry(root, show="*", font=("Helvetica", 16))
    admin_password_entry.pack(pady=10)

    admin_login_button = tk.Button(root, text="შესვლა", command=admin_login, bg="limegreen", fg="white", font=("Helvetica", 16))
    admin_login_button.pack(pady=20)

    back_button = tk.Button(root, text="უკან", command=show_choice_page, bg="red", fg="white", font=("Helvetica", 16))
    back_button.pack(pady=10)

# Function to switch to patient login page
def show_patient_login():
    clear_screen()
    tk.Label(root, text="პაციენტის ავტორიზაცია", bg="dodgerblue", fg="white", font=("Helvetica", 24)).pack(pady=20)
    tk.Label(root, text="პირადი ნომერი:", bg="dodgerblue", fg="white", font=("Helvetica", 16)).pack(pady=10)
    
    global patient_private_number_entry
    patient_private_number_entry = tk.Entry(root, font=("Helvetica", 16))
    patient_private_number_entry.pack(pady=10)
    
    tk.Label(root, text="პაროლი:", bg="dodgerblue", fg="white", font=("Helvetica", 16)).pack(pady=10)
    
    global patient_password_entry
    patient_password_entry = tk.Entry(root, show="*", font=("Helvetica", 16))
    patient_password_entry.pack(pady=10)

    patient_login_button = tk.Button(root, text="შესვლა", command=patient_login, bg="limegreen", fg="white", font=("Helvetica", 16))
    patient_login_button.pack(pady=20)

    back_button = tk.Button(root, text="უკან", command=show_choice_page, bg="red", fg="white", font=("Helvetica", 16))
    back_button.pack(pady=10)

# Function to clear all widgets from the screen
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# Function to show the choice page
def show_choice_page():
    clear_screen()
    tk.Label(root, text="Aramiants Hospital Tbilisi", bg="dodgerblue", fg="white", font=("Helvetica", 30)).pack(pady=20)
    tk.Label(root, text="აირჩიეთ ავტორიზაციის ტიპი", bg="dodgerblue", fg="white", font=("Helvetica", 24)).pack(pady=50)
    admin_choice_button = tk.Button(root, text="ადმინის ავტორიზაცია", command=show_admin_login, bg="limegreen", fg="white", font=("Helvetica", 16), width=20)
    admin_choice_button.pack(pady=20)
    patient_choice_button = tk.Button(root, text="პაციენტის ავტორიზაცია", command=show_patient_login, bg="limegreen", fg="white", font=("Helvetica", 16), width=20)
    patient_choice_button.pack(pady=20)

# Admin login
def admin_login():
    username = admin_username_entry.get().strip()
    password = admin_password_entry.get().strip()
    
    if not username or not password:
        messagebox.showwarning("შეავსეთ ყველა ველი !")
        return
    
    conn = sqlite3.connect('AramiantHospital.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Admins WHERE Username=? AND Password=?", (username, password))
    admin = c.fetchone()
    conn.close()
    
    if admin:
        show_admin_panel()
    else:
        messagebox.showerror("ავტორიზაცია წარუმატებელია, შეასწორეთ შეყვანილი მონაცემები !")

# Patient login
def patient_login():
    private_number = patient_private_number_entry.get().strip()
    password = patient_password_entry.get().strip()
    
    if not private_number or not password:
        messagebox.showwarning("შეავსეთ ყველა ველი !")
        return
    
    conn = sqlite3.connect('AramiantHospital.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Patients WHERE Private_Number=? AND Password=?", (private_number, password))
    patient = c.fetchone()
    conn.close()
    
    if patient:
        show_patient_panel(patient)
    else:
        messagebox.showerror("ავტორიზაცია წარუმატებელია, შეასწორეთ შეყვანილი მონაცემები !")

# Show Admin Panel
def show_admin_panel():
    clear_screen()
    
    tk.Label(root, text="ადმინისტრატორის პანელი", bg="dodgerblue", fg="white", font=("Helvetica", 24)).pack(pady=20)

    main_frame = tk.Frame(root, bg="dodgerblue")
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Left Frame for Patient tools
    left_frame = tk.Frame(main_frame, bg="dodgerblue")
    left_frame.pack(side=tk.LEFT, padx=18, pady=18, fill=tk.BOTH, expand=True)
    
    tk.Label(left_frame, text="ახალი პაციენტის დამატება", bg="dodgerblue", fg="white", font=("Helvetica", 18)).pack(pady=10)
    
    form_frame = tk.Frame(left_frame, bg="dodgerblue")
    form_frame.pack(pady=18)
    
    tk.Label(form_frame, text="პირადი ნომერი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(form_frame, text="სახელი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=5)
    tk.Label(form_frame, text="გვარი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=2, column=0, padx=10, pady=5)
    tk.Label(form_frame, text="პაროლი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=3, column=0, padx=10, pady=5)
    tk.Label(form_frame, text="დაბადების თარიღი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=4, column=0, padx=10, pady=5)
    tk.Label(form_frame, text="ჯანმრთელობის მდგომარეობა", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=5, column=0, padx=10, pady=5)
    tk.Label(form_frame, text="გადასახადი სულ", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=6, column=0, padx=10, pady=5)
    tk.Label(form_frame, text="ბოლო ვიზიტი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=7, column=0, padx=10, pady=5)

    private_number_entry = tk.Entry(form_frame, font=("Helvetica", 16))
    name_entry = tk.Entry(form_frame, font=("Helvetica", 16))
    surname_entry = tk.Entry(form_frame, font=("Helvetica", 16))
    password_entry = tk.Entry(form_frame, font=("Helvetica", 16))
    birthday_entry = tk.Entry(form_frame, font=("Helvetica", 16))
    health_info_entry = tk.Entry(form_frame, font=("Helvetica", 16))
    total_bills_entry = tk.Entry(form_frame, font=("Helvetica", 16))
    last_visit_entry = tk.Entry(form_frame, font=("Helvetica", 16))

    private_number_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.grid(row=1, column=1, padx=10, pady=5)
    surname_entry.grid(row=2, column=1, padx=10, pady=5)
    password_entry.grid(row=3, column=1, padx=10, pady=5)
    birthday_entry.grid(row=4, column=1, padx=10, pady=5)
    health_info_entry.grid(row=5, column=1, padx=10, pady=5)
    total_bills_entry.grid(row=6, column=1, padx=10, pady=5)
    last_visit_entry.grid(row=7, column=1, padx=10, pady=5)

    def add_patient():
        private_number = private_number_entry.get().strip()
        name = name_entry.get().strip()
        surname = surname_entry.get().strip()
        password = password_entry.get().strip()
        birthday = birthday_entry.get().strip()
        health_info = health_info_entry.get().strip()
        total_bills = total_bills_entry.get().strip()
        last_visit = last_visit_entry.get().strip()
        
        if not private_number or not name or not surname or not password or not birthday:
            messagebox.showwarning("შეავსეთ ყველა ველი !")
            return
        
        if len(password) < 3:
            messagebox.showwarning("შეცდომა, პაროლი უნდა იყოს მინიმუმ 3 სიმბოლიანი !")
            return

        if not total_bills:
            total_bills = 0.0
        else:
            try:
                total_bills = float(total_bills)
            except ValueError:
                messagebox.showwarning("შეცდომა, გადასახადი უნდა იყოს მხოლოდ ციფრებით შეყვანილი !")
                return

        conn = sqlite3.connect('AramiantHospital.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Patients (Private_Number, Name, Surname, Password, Birthday, Health_Info, Total_Bills, Last_Visit) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (private_number, name, surname, password, birthday, health_info, total_bills, last_visit))
            conn.commit()
            messagebox.showinfo("პაციენტი წარმატებულად დაემატა !")
            clear_admin_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("შეყვანილი პირადი ნომერი უკვე არსებობს ბაზაში !")
        conn.close()

    def clear_admin_entries():
        private_number_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        birthday_entry.delete(0, tk.END)
        health_info_entry.delete(0, tk.END)
        total_bills_entry.delete(0, tk.END)
        last_visit_entry.delete(0, tk.END)

    add_patient_button = tk.Button(left_frame, text="პაციენტის დამატება", command=add_patient, bg="limegreen", fg="white", font=("Helvetica", 16))
    add_patient_button.pack(pady=10)

    # Edit patient section
    tk.Label(left_frame, text="პაციენტის მონაცემის შესწორება", bg="dodgerblue", fg="white", font=("Helvetica", 18)).pack(pady=18)
    
    patient_edit_frame = tk.Frame(left_frame, bg="dodgerblue")
    patient_edit_frame.pack(pady=10)

    tk.Label(patient_edit_frame, text="პირადი ნომერი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5)
    edit_patient_private_number_entry = tk.Entry(patient_edit_frame, font=("Helvetica", 16))
    edit_patient_private_number_entry.grid(row=0, column=1, padx=10, pady=5)

    def edit_patient():
        private_number = edit_patient_private_number_entry.get().strip()
        if not private_number:
            messagebox.showwarning("შეიყვანეთ პაციენტის პირადი ნომერი !")
            return

        conn = sqlite3.connect('AramiantHospital.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Patients WHERE Private_Number=?", (private_number,))
        patient = c.fetchone()
        conn.close()

        if not patient:
            messagebox.showerror("ვერ მოიძებნა ამ პირადი ნომრით პაციენტი ბაზაში, გადაამოწმეთ !")
            return

        edit_patient_window = tk.Toplevel(root)
        edit_patient_window.title("Edit Patient")
        edit_patient_window.configure(bg="dodgerblue")

        tk.Label(edit_patient_window, text="სახელი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5)
        edit_name_entry = tk.Entry(edit_patient_window, font=("Helvetica", 16))
        edit_name_entry.grid(row=0, column=1, padx=10, pady=5)
        edit_name_entry.insert(0, patient[2])

        tk.Label(edit_patient_window, text="გვარი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=5)
        edit_surname_entry = tk.Entry(edit_patient_window, font=("Helvetica", 16))
        edit_surname_entry.grid(row=1, column=1, padx=10, pady=5)
        edit_surname_entry.insert(0, patient[3])

        tk.Label(edit_patient_window, text="პაროლი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=2, column=0, padx=10, pady=5)
        edit_password_entry = tk.Entry(edit_patient_window, font=("Helvetica", 16))
        edit_password_entry.grid(row=2, column=1, padx=10, pady=5)
        edit_password_entry.insert(0, patient[4])

        tk.Label(edit_patient_window, text="დაბადების თარიღი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=3, column=0, padx=10, pady=5)
        edit_birthday_entry = tk.Entry(edit_patient_window, font=("Helvetica", 16))
        edit_birthday_entry.grid(row=3, column=1, padx=10, pady=5)
        edit_birthday_entry.insert(0, patient[5])

        tk.Label(edit_patient_window, text="ჯანმრთელობის მდგომარეობა", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=4, column=0, padx=10, pady=5)
        edit_health_info_entry = tk.Entry(edit_patient_window, font=("Helvetica", 16))
        edit_health_info_entry.grid(row=4, column=1, padx=10, pady=5)
        edit_health_info_entry.insert(0, patient[6])

        tk.Label(edit_patient_window, text="გადასახადი სულ", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=5, column=0, padx=10, pady=5)
        edit_total_bills_entry = tk.Entry(edit_patient_window, font=("Helvetica", 16))
        edit_total_bills_entry.grid(row=5, column=1, padx=10, pady=5)
        edit_total_bills_entry.insert(0, patient[7])

        tk.Label(edit_patient_window, text="ბოლო ვიზიტი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=6, column=0, padx=10, pady=5)
        edit_last_visit_entry = tk.Entry(edit_patient_window, font=("Helvetica", 16))
        edit_last_visit_entry.grid(row=6, column=1, padx=10, pady=5)
        edit_last_visit_entry.insert(0, patient[8])

        def update_patient():
            new_name = edit_name_entry.get().strip()
            new_surname = edit_surname_entry.get().strip()
            new_password = edit_password_entry.get().strip()
            new_birthday = edit_birthday_entry.get().strip()
            new_health_info = edit_health_info_entry.get().strip()
            new_total_bills = edit_total_bills_entry.get().strip()
            new_last_visit = edit_last_visit_entry.get().strip()

            if not new_name or not new_surname or not new_password or not new_birthday:
                messagebox.showwarning("შეცდომა, ყველა ველი შეავსეთ !")
                return

            if len(new_password) < 3:
                messagebox.showwarning("შეცდომა, პაროლი უნდა შეიცავდეს მინიმუმ 3 სიმბოლოს !")
                return

            if not new_total_bills:
                new_total_bills = 0.0
            else:
                try:
                    new_total_bills = float(new_total_bills)
                except ValueError:
                    messagebox.showwarning("შეცდომა, გადასახადი უნდა შეიყვნოთ მხოლოდ ციფრებით !")
                    return

            conn = sqlite3.connect('AramiantHospital.db')
            c = conn.cursor()
            c.execute("UPDATE Patients SET Name=?, Surname=?, Password=?, Birthday=?, Health_Info=?, Total_Bills=?, Last_Visit=? WHERE Private_Number=?",
                      (new_name, new_surname, new_password, new_birthday, new_health_info, new_total_bills, new_last_visit, private_number))
            conn.commit()
            conn.close()
            messagebox.showinfo("ინფორმაცია პაციენტზე განახლდა წარმატებულად !")
            edit_patient_window.destroy()

        update_patient_button = tk.Button(edit_patient_window, text="პაციენტის მონაცემების განახლება", command=update_patient, bg="limegreen", fg="white", font=("Helvetica", 16))
        update_patient_button.grid(row=7, column=0, columnspan=2, pady=10)

    edit_patient_button = tk.Button(left_frame, text="პაციენტის მონაცემების შესწორება", command=edit_patient, bg="limegreen", fg="white", font=("Helvetica", 16))
    edit_patient_button.pack(pady=10)

    # Right Frame for Doctor tools
    right_frame = tk.Frame(main_frame, bg="dodgerblue")
    right_frame.pack(side=tk.RIGHT, padx=2, pady=18, fill=tk.BOTH, expand=True)
    
    tk.Label(right_frame, text="ექიმის დამატება", bg="dodgerblue", fg="white", font=("Helvetica", 18)).pack(pady=20)
    
    doctor_frame = tk.Frame(right_frame, bg="dodgerblue")
    doctor_frame.pack(pady=10)
    
    tk.Label(doctor_frame, text="სახელი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(doctor_frame, text="გვარი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=5)
    tk.Label(doctor_frame, text="პროფესია", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=2, column=0, padx=10, pady=5)
    tk.Label(doctor_frame, text="ტელეფონი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=3, column=0, padx=10, pady=5)

    doctor_name_entry = tk.Entry(doctor_frame, font=("Helvetica", 16))
    doctor_surname_entry = tk.Entry(doctor_frame, font=("Helvetica", 16))
    doctor_profession_entry = tk.Entry(doctor_frame, font=("Helvetica", 16))
    doctor_phone_entry = tk.Entry(doctor_frame, font=("Helvetica", 16))

    doctor_name_entry.grid(row=0, column=1, padx=10, pady=5)
    doctor_surname_entry.grid(row=1, column=1, padx=10, pady=5)
    doctor_profession_entry.grid(row=2, column=1, padx=10, pady=5)
    doctor_phone_entry.grid(row=3, column=1, padx=10, pady=5)

    def add_doctor():
        doctor_name = doctor_name_entry.get().strip()
        doctor_surname = doctor_surname_entry.get().strip()
        doctor_profession = doctor_profession_entry.get().strip()
        doctor_phone = doctor_phone_entry.get().strip()
        
        if not doctor_name or not doctor_surname or not doctor_profession:
            messagebox.showwarning("შეიყვანეთ ყველა ველი !")
            return
        
        conn = sqlite3.connect('AramiantHospital.db')
        c = conn.cursor()
        c.execute("INSERT INTO doctors (Name, Surname, Profession, Phone) VALUES (?, ?, ?, ?)", (doctor_name, doctor_surname, doctor_profession, doctor_phone))
        conn.commit()
        messagebox.showinfo("ექიმი წარმატებულად დაემატა !")
        clear_doctor_entries()
        conn.close()

    def clear_doctor_entries():
        doctor_name_entry.delete(0, tk.END)
        doctor_surname_entry.delete(0, tk.END)
        doctor_profession_entry.delete(0, tk.END)
        doctor_phone_entry.delete(0, tk.END)

    add_doctor_button = tk.Button(right_frame, text="ექიმის დამატება", command=add_doctor, bg="limegreen", fg="white", font=("Helvetica", 16))
    add_doctor_button.pack(pady=10)

    # Edit doctor section
    tk.Label(right_frame, text="შეასწორეთ მონაცემები ექიმზე", bg="dodgerblue", fg="white", font=("Helvetica", 20)).pack(pady=20)
    
    doctor_edit_frame = tk.Frame(right_frame, bg="dodgerblue")
    doctor_edit_frame.pack(pady=10)

    tk.Label(doctor_edit_frame, text="ექიმის სახელი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5)
    edit_doctor_name_entry = tk.Entry(doctor_edit_frame, font=("Helvetica", 16))
    edit_doctor_name_entry.grid(row=0, column=1, padx=10, pady=5)

    def edit_doctor():
        doctor_name = edit_doctor_name_entry.get().strip()
        if not doctor_name:
            messagebox.showwarning("შეცდომა, შეიყვანეთ ექიმის სახელი !")
            return

        conn = sqlite3.connect('AramiantHospital.db')
        c = conn.cursor()
        c.execute("SELECT * FROM doctors WHERE Name=?", (doctor_name,))
        doctor = c.fetchone()
        conn.close()

        if not doctor:
            messagebox.showerror("ასეთი სახელით ექიმი ვერ იქნა ნაპოვნი ბაზაში !")
            return

        edit_doctor_window = tk.Toplevel(root)
        edit_doctor_window.title("ექიმის მონაცემთა შესწორება")
        edit_doctor_window.configure(bg="dodgerblue")

        tk.Label(edit_doctor_window, text="სახელი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5)
        edit_name_entry = tk.Entry(edit_doctor_window, font=("Helvetica", 16))
        edit_name_entry.grid(row=0, column=1, padx=10, pady=5)
        edit_name_entry.insert(0, doctor[1])

        tk.Label(edit_doctor_window, text="გვარი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=5)
        edit_surname_entry = tk.Entry(edit_doctor_window, font=("Helvetica", 16))
        edit_surname_entry.grid(row=1, column=1, padx=10, pady=5)
        edit_surname_entry.insert(0, doctor[2])

        tk.Label(edit_doctor_window, text="პროფესია", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=2, column=0, padx=10, pady=5)
        edit_profession_entry = tk.Entry(edit_doctor_window, font=("Helvetica", 16))
        edit_profession_entry.grid(row=2, column=1, padx=10, pady=5)
        edit_profession_entry.insert(0, doctor[3])

        tk.Label(edit_doctor_window, text="ტელეფონი", bg="dodgerblue", fg="white", font=("Helvetica", 16)).grid(row=3, column=0, padx=10, pady=5)
        edit_phone_entry = tk.Entry(edit_doctor_window, font=("Helvetica", 16))
        edit_phone_entry.grid(row=3, column=1, padx=10, pady=5)
        edit_phone_entry.insert(0, doctor[4])

        def update_doctor():
            new_name = edit_name_entry.get().strip()
            new_surname = edit_surname_entry.get().strip()
            new_profession = edit_profession_entry.get().strip()
            new_phone = edit_phone_entry.get().strip()

            if not new_name or not new_surname or not new_profession:
                messagebox.showwarning("შეავსეთ ყველა ველი !")
                return

            conn = sqlite3.connect('AramiantHospital.db')
            c = conn.cursor()
            c.execute("UPDATE doctors SET Name=?, Surname=?, Profession=?, Phone=? WHERE Name=?",
                      (new_name, new_surname, new_profession, new_phone, doctor_name))
            conn.commit()
            conn.close()
            messagebox.showinfo("ექიმის მონაცემები განახლდა წარმატებულად !")
            edit_doctor_window.destroy()

        update_doctor_button = tk.Button(edit_doctor_window, text="ექიმის მონაცემთა განახლება", command=update_doctor, bg="limegreen", fg="white", font=("Helvetica", 16))
        update_doctor_button.grid(row=4, column=0, columnspan=2, pady=10)

    edit_doctor_button = tk.Button(right_frame, text="ექიმის მონაცემთა შესწორება", command=edit_doctor, bg="limegreen", fg="white", font=("Helvetica", 16))
    edit_doctor_button.pack(pady=10)

    # Admin Logout button
    logout_button = tk.Button(root, text="გამოსვლა", command=show_choice_page, bg="red", fg="white", font=("Helvetica", 16))
    logout_button(pady=18)

# Show Patient Panel
def show_patient_panel(patient):
    clear_screen()
    tk.Label(root, text="პაციენტთა პორტალი", bg="lightgreen", fg="black", font=("Helvetica", 24)).pack(pady=20)
    
    tk.Label(root, text="მოგესალმებით, " + patient[2], bg="lightgreen", font=("Helvetica", 20)).pack(pady=10)
    
    info_frame = tk.Frame(root, bg="lightgreen")
    info_frame.pack(pady=10)
    
    tk.Label(info_frame, text="პირადი ნომერი: " + patient[1], bg="lightgreen", font=("Helvetica", 16)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(info_frame, text="დაბადების თარიღი: " + patient[5], bg="lightgreen", font=("Helvetica", 16)).grid(row=1, column=0, padx=10, pady=5)
    tk.Label(info_frame, text="ჯანმრთელობის მდგომარეობა: " + patient[6], bg="lightgreen", font=("Helvetica", 16)).grid(row=2, column=0, padx=10, pady=5)
    tk.Label(info_frame, text="სულ გადასახადი: " + str(patient[7]) + "₾", bg="lightgreen", font=("Helvetica", 16)).grid(row=3, column=0, padx=10, pady=5)
    tk.Label(info_frame, text="ბოლო ვიზიტი: " + patient[8], bg="lightgreen", font=("Helvetica", 16)).grid(row=4, column=0, padx=10, pady=5)

    tk.Label(root, text="ექიმთა ჩამონათვალი : ", bg="lightgreen", font=("Helvetica", 20)).pack(pady=20)

    doctors_listbox = tk.Listbox(root, font=("Helvetica", 16), width=50)
    doctors_listbox.pack(pady=10)

    conn = sqlite3.connect('AramiantHospital.db')
    c = conn.cursor()
    c.execute("SELECT Name, Surname, Profession, Phone FROM doctors")
    doctors = c.fetchall()
    conn.close()
    
    for doctor in doctors:
        doctors_listbox.insert(tk.END, f"{doctor[0]} {doctor[1]}, {doctor[2]}, {doctor[3]}")

    back_button = tk.Button(root, text="გამოსვლა", command=show_choice_page, bg="red", fg="white", font=("Helvetica", 16))
    back_button.pack(pady=18)

# Create the main window
root = tk.Tk()
root.title("AHTbilisi")
root.configure(bg="dodgerblue")

# Set the window icon
# icon = PhotoImage(file="AramiantsHospitalTbilisi-01.png")
# root.iconphoto(True, icon)

# Set bordered fullscreen
root.state('zoomed')

# Minimize and close buttons
def minimize_window():
    root.iconify()

def close_window():
    root.destroy()

minimize_button = tk.Button(root, text="_", command=minimize_window, bg="limegreen", fg="white", font=("Helvetica", 16))
minimize_button.place(x=1260, y=10, width=30, height=30)

close_button = tk.Button(root, text="X", command=close_window, bg="red", fg="white", font=("Helvetica", 16))
close_button.place(x=1300, y=10, width=30, height=30)

# Initialize the database
create_database()

# Show choice page at the start
show_choice_page()

# Run the application
root.mainloop()
