import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox, filedialog
import csv
from datetime import datetime
import os

# --------------------------
# Global Variables
# --------------------------
students = []
attendance_vars = []
current_class_file = None  # Stores currently loaded class file

# --------------------------
# Functions
# --------------------------
def load_students():
    """Load student list from user-selected CSV file"""
    global students, current_class_file
    file_path = filedialog.askopenfilename(
        title="Select Student CSV File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )

    if not file_path:
        return  # User cancelled file selection

    current_class_file = os.path.basename(file_path).split(".")[0]  # e.g. 'classA'
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            students = [row for row in reader]
        if not students:
            messagebox.showwarning("Warning", "The selected CSV file is empty.")
        else:
            display_students()
            messagebox.showinfo("Success", f"Loaded student data from {current_class_file}.csv")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")

def display_students():
    """Display student list"""
    for widget in frame_table.winfo_children():
        widget.destroy()
    attendance_vars.clear()

    Label(frame_table, text="Roll No", font=("Arial", 12, "bold"), bg="#E3F2FD").grid(row=0, column=0, padx=10)
    Label(frame_table, text="Name", font=("Arial", 12, "bold"), bg="#E3F2FD").grid(row=0, column=1, padx=10)
    Label(frame_table, text="Present", font=("Arial", 12, "bold"), bg="#E3F2FD").grid(row=0, column=2, padx=10)
    Label(frame_table, text="Absent", font=("Arial", 12, "bold"), bg="#E3F2FD").grid(row=0, column=3, padx=10)

    for i, student in enumerate(students, start=1):
        Label(frame_table, text=student["Roll No"], font=("Arial", 11), bg="#E3F2FD").grid(row=i, column=0, pady=5)
        Label(frame_table, text=student["Name"], font=("Arial", 11), bg="#E3F2FD").grid(row=i, column=1, pady=5)

        var_present = IntVar()
        var_absent = IntVar()

        Checkbutton(frame_table, variable=var_present, bg="#E3F2FD",
                    command=lambda vp=var_present, va=var_absent: mark_present(vp, va)).grid(row=i, column=2)
        Checkbutton(frame_table, variable=var_absent, bg="#E3F2FD",
                    command=lambda va=var_absent, vp=var_present: mark_absent(va, vp)).grid(row=i, column=3)

        attendance_vars.append((var_present, var_absent))

def mark_present(var_present, var_absent):
    if var_present.get() == 1:
        var_absent.set(0)

def mark_absent(var_absent, var_present):
    if var_absent.get() == 1:
        var_present.set(0)

def save_attendance():
    """Save attendance per class and date"""
    if not students or not current_class_file:
        messagebox.showwarning("No Data", "Please load a class file first.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join("AttendanceRecords", current_class_file)
    os.makedirs(folder, exist_ok=True)

    filename = f"attendance_{today}.csv"
    filepath = os.path.join(folder, filename)

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Roll No", "Name", "Status"])
        for i, student in enumerate(students):
            status = "Present" if attendance_vars[i][0].get() == 1 else "Absent"
            writer.writerow([date_time, student["Roll No"], student["Name"], status])

    messagebox.showinfo("Saved",
                        f"Attendance saved for {current_class_file}!\nFile: {filename}\nLocation: {folder}")

def show_graph():
    """Display attendance bar graph"""
    if not students:
        messagebox.showwarning("No Data", "Please load a class first.")
        return

    attendance = np.array([vp.get() for vp, _ in attendance_vars])
    names = np.array([s["Name"] for s in students])

    colors = ['lightgreen' if a == 1 else 'salmon' for a in attendance]
    plt.figure(figsize=(10, 6))
    plt.bar(names, attendance, color=colors, edgecolor='black')
    plt.ylim(0, 1.2)
    plt.ylabel("Attendance", fontsize=12)
    plt.title(f"📊 Attendance Record - {current_class_file}", fontsize=15, fontweight='bold')

    plt.xticks(rotation=45, ha='right', fontsize=10)
    for i, a in enumerate(attendance):
        plt.text(i, a + 0.05, 'P' if a == 1 else 'A', ha='center', fontweight='bold')

    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def clear_all():
    for vp, va in attendance_vars:
        vp.set(0)
        va.set(0)
    messagebox.showinfo("Cleared", "All attendance cleared.")

# --------------------------
# GUI Design
# --------------------------
root = Tk()
root.title("Multi-Class Attendance Management System")
root.geometry("780x620")
root.config(bg="#E3F2FD")

Label(root, text=" Multi-Class Attendance Management System",
      font=("Arial", 18, "bold"), bg="#E3F2FD").pack(pady=15)

# Buttons Frame
btn_frame = Frame(root, bg="#E3F2FD")
btn_frame.pack(pady=10)

Button(btn_frame, text=" Load Class CSV", command=load_students, bg="#1976D2", fg="white",
       font=("Arial", 11, "bold"), width=18).grid(row=0, column=0, padx=10)

Button(btn_frame, text=" Save Attendance", command=save_attendance, bg="#43A047", fg="white",
       font=("Arial", 11, "bold"), width=18).grid(row=0, column=1, padx=10)

Button(btn_frame, text=" Show Graph", command=show_graph, bg="#0288D1", fg="white",
       font=("Arial", 11, "bold"), width=15).grid(row=0, column=2, padx=10)

Button(btn_frame, text=" Clear All", command=clear_all, bg="#E53935", fg="white",
       font=("Arial", 11, "bold"), width=10).grid(row=0, column=3, padx=10)

# Frame for Student Table
frame_table = Frame(root, bg="#E3F2FD")
frame_table.pack(pady=20)

# Run App
root.mainloop()
