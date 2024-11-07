import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# MySQL Database Connection
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="root",       
            password="Guna@2005",  
            database="user_db"
        )
        return conn
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Helper function to execute a MySQL query with parameters

def execute_query(query, params=()):
    results = None
    conn = None
    cursor = None
    try:
        # Establish a new connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Guna@2005",
            database="user_db"
        )
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Check if the query is a SELECT statement
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()  # Fetch all results if it's a SELECT query
        else:
            conn.commit()  # Commit changes for INSERT, UPDATE, DELETE queries

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor is not None:
            cursor.close()  # Close the cursor if it was created
        if conn is not None:
            conn.close()    # Close the connection if it was created

    return results


# Function to check login credentials
def login():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        username = entry_username.get()
        password = entry_password.get()
        role = role_var.get()
        
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND role = %s", (username, password, role))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            label_message.configure(text="Login Successful!", text_color="green")
            open_role_window(role)  # Open the role-specific window
        else:
            label_message.configure(text="Invalid Username, Password, or Role", text_color="red")
    else:
        label_message.configure(text="Database Connection Failed", text_color="red")

# Function to open role-specific window
def open_role_window(role):
    global content_frame  # Make content_frame accessible globally
    role_window = ctk.CTkToplevel()
    role_window.title(f"{role} Dashboard")
    role_window.geometry("800x600")
    
    # Create sidebar frame with a distinct color
    sidebar_frame = ctk.CTkFrame(role_window, width=180, corner_radius=0, fg_color="#2D2F3A")
    sidebar_frame.pack(side="left", fill="y")
    
    # Create main content frame (right side) with padding
    content_frame = ctk.CTkFrame(role_window, width=600, fg_color="grey")
    content_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
    
    # Function to update content based on the selected option/sub-option
    def display_content(content):
        # Clear existing content
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        # Add Appointments View
        if content == "BILL - ADD APPOINTMENTS":
            add_appointment_view(content_frame)

        # Update Appointments View
        elif content == "BILL - UPDATE APPOINTMENTS":
            update_appointment_view(content_frame)

        # Appointment Detail View
        elif content == "BILL - APPOINTMENT DETAIL":
            appointment_detail_view(content_frame)

        if content == "BILL - ADD DOCTOR":
            add_doctor_view(content_frame)

        # Update Doctors View
        elif content == "BILL - UPDATE DOCTOR":
            update_doctor_view(content_frame)

        # Doctor Detail View
        elif content == "BILL - DOCTOR DETAIL":
            doctor_detail_view(content_frame)

        if content == "BILL - ADD PATIENT":
            add_patient_view(content_frame)

        # Update Doctors View
        elif content == "BILL - UPDATE PATIENT":
            update_patient_view(content_frame)

        # Doctor Detail View
        elif content == "BILL - PATIENT DETAIL":
            patient_detail_view(content_frame)
            
        if content == "BILL - GENERATE BILL":
            generate_bill_view(content_frame)
        
        elif content == "BILL - VIEW BILL":
            view_bill_view(content_frame)
        
        elif content == "BILL - DELETE BILL":
            delete_bill_view(content_frame)
        
        # Define views for Doctors, Patients, and Bill sections here as needed

    # Admin sidebar with sub-options and styled buttons
    if role == "Admin":
        sidebar_options = {
            "APPOINTMENTS": ["ADD APPOINTMENTS", "UPDATE APPOINTMENTS", "APPOINTMENT DETAIL"],
            "DOCTORS": ["ADD DOCTOR", "UPDATE DOCTOR", "DOCTOR DETAIL"],
            "PATIENTS": ["ADD PATIENT", "UPDATE PATIENT", "PATIENT DETAIL"],
            "BILL": ["GENERATE BILL", "VIEW BILL", "DELETE BILL"]
        }
        
        for main_option, sub_options in sidebar_options.items():
            # Main section header (without command, just a label for sub-options)
            main_label = ctk.CTkLabel(sidebar_frame, text=main_option, text_color="#EAEAEA", fg_color="#2D2F3A", font=("Arial", 12, "bold"))
            main_label.pack(pady=(10, 0), padx=10, anchor="w")
            
            for sub_option in sub_options:
                sub_button = ctk.CTkButton(
                    sidebar_frame, 
                    text=sub_option, 
                    command=lambda opt=sub_option: display_content(f"{main_option} - {opt}"),
                    fg_color="#3C3F51", 
                    hover_color="#555A71", 
                    text_color="#FFFFFF"
                )
                sub_button.pack(pady=2, padx=20, anchor="w")

    # Add a label in the content frame to show the initial dashboard text
    initial_label = ctk.CTkLabel(content_frame, text=f"Welcome to {role} Portal", font=("Arial", 24))
    initial_label.pack(pady=40)

# Function to open registration window
def open_register_window():
    register_window = ctk.CTkToplevel()
    register_window.title("Register")
    register_window.geometry("400x400")

    def register_user():
        conn = create_connection()
        if conn is not None:
            cursor = conn.cursor()
            new_username = entry_new_username.get()
            new_password = entry_new_password.get()
            new_role = register_role_var.get()
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (new_username, new_password, new_role))
                conn.commit()
                label_register_message.configure(text="User Registered!", text_color="green")
                
            except Error as e:
                label_register_message.configure(text="Error: User already exists", text_color="red")
            conn.close()

    # Registration form
    label_register = ctk.CTkLabel(register_window, text="Register", font=("Arial", 24))
    label_register.pack(pady=20)

    label_new_username = ctk.CTkLabel(register_window, text="New Username:")
    label_new_username.pack()
    entry_new_username = ctk.CTkEntry(register_window)
    entry_new_username.pack(pady=5)

    label_new_password = ctk.CTkLabel(register_window, text="New Password:")
    label_new_password.pack()
    entry_new_password = ctk.CTkEntry(register_window, show="*")
    entry_new_password.pack(pady=5)

    label_role = ctk.CTkLabel(register_window, text="Role:")
    label_role.pack()
    register_role_var = ctk.StringVar(value="Admin")
    role_options = ctk.CTkComboBox(register_window, variable=register_role_var, values=["Admin", "Doctor", "Pharmacist"])
    role_options.pack(pady=5)

    button_create_account = ctk.CTkButton(register_window, text="Create Account", command=register_user)
    button_create_account.pack(pady=10)

    label_register_message = ctk.CTkLabel(register_window, text="")
    label_register_message.pack()

# View for Adding an Appointment
def add_appointment_view(parent):
    ctk.CTkLabel(parent, text="Add Appointment", font=("Arial", 18)).pack(pady=10)

    # Input fields for patient name, doctor name, date, and time
    labels = ["Patient Name:", "Doctor Name:", "Date (YYYY-MM-DD):", "Appointment Time (HH:MM):"]
    entries = []
    for label_text in labels:
        ctk.CTkLabel(parent, text=label_text).pack()
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        entries.append(entry)

    # Button to add the appointment to the database
    def add_appointment():
        patient_name, doctor_name, date, time = [e.get() for e in entries]

        # Check if patient exists; if not, display message
        patient_exists = execute_query(
            "SELECT COUNT(*) FROM patients WHERE name = %s", (patient_name,)
        )[0][0]

        if not patient_exists:
            ctk.CTkLabel(parent, text=f"Patient '{patient_name}' does not exist. Please add patient information.", text_color="red").pack()
            return

        # Check if doctor exists; if not, display message
        doctor_exists = execute_query(
            "SELECT COUNT(*) FROM doctors WHERE name = %s", (doctor_name,)
        )[0][0]

        if not doctor_exists:
            ctk.CTkLabel(parent, text=f"Doctor '{doctor_name}' does not exist. Please add doctor information.", text_color="red").pack()
            return

        # Insert the appointment now that patient and doctor exist in the database
        execute_query(
            "INSERT INTO appointments (patient_name, doctor_name, date, time) VALUES (%s, %s, %s, %s)",
            (patient_name, doctor_name, date, time)
        )
        ctk.CTkLabel(parent, text="Appointment added successfully!", text_color="green").pack()


    ctk.CTkButton(parent, text="Add Appointment", command=add_appointment).pack(pady=10)

# View for Updating an Appointment
def update_appointment_view(parent):
    ctk.CTkLabel(parent, text="Update Appointment", font=("Arial", 18)).pack(pady=10)

    # Search bar to find an appointment
    search_entry = ctk.CTkEntry(parent, placeholder_text="Search Patient Name")
    search_entry.pack(pady=5)

    # Frame for search results
    search_results_frame = ctk.CTkFrame(parent)
    search_results_frame.pack(fill="x", padx=10, pady=5)

    # Fields to update patient name, doctor name, date, and time
    update_labels = ["Appointment ID:", "Patient Name:", "Doctor Name:", "Date (YYYY-MM-DD):", "Appointment Time (HH:MM):"]
    update_entries = []
    for label_text in update_labels:
        ctk.CTkLabel(parent, text=label_text).pack()
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        update_entries.append(entry)

    # Function to search for a patient and display results
    def search_appointment():
        patient_name = search_entry.get()
        results = execute_query("SELECT * FROM appointments WHERE patient_name = %s", (patient_name,))

        # Clear previous results
        for widget in search_results_frame.winfo_children():
            widget.destroy()

        if results:
            for row in results:
                result_label = ctk.CTkLabel(search_results_frame, text=f"Appointment ID: {row[0]}, Patient: {row[1]}, Doctor: {row[2]}, Date: {row[3]}, Time: {row[4]}")
                result_label.pack()
                
                # Adding button to fill fields with selected result
                update_button = ctk.CTkButton(search_results_frame, text="Select", command=lambda appointment=row: fill_update_fields(appointment))
                update_button.pack(pady=5)

        else:
            ctk.CTkLabel(search_results_frame, text="No results found").pack()

    # Function to fill the update fields with selected appointment details
    def fill_update_fields(appointment):
        # Populate fields with current appointment details
        for entry, value in zip(update_entries[1:], appointment[1:]):  # Skip appointment ID
            entry.delete(0, ctk.END)
            entry.insert(0, value)
        
        # Set the appointment ID in the first entry
        update_entries[0].delete(0, ctk.END)
        update_entries[0].insert(0, appointment[0])  # Appointment ID

    ctk.CTkButton(parent, text="Search Appointment", command=search_appointment).pack(pady=5)

    # Button to update the appointment in the database
    def update_appointment():
        appointment_id = update_entries[0].get().strip()  # Get the appointment ID

        # Fetch the current appointment details
        current_appointment = execute_query(
            "SELECT patient_name, doctor_name, date, time FROM appointments WHERE id = %s",
            (appointment_id,)
        )

        if not current_appointment:
            ctk.CTkLabel(parent, text="Appointment ID not found.", text_color="red").pack()
            return

        # Unpack the current appointment details
        current_patient_name, current_doctor_name, current_date, current_time = current_appointment[0]

        # Get new values from the entry fields, or retain current values if the entry is empty
        new_patient_name = update_entries[1].get().strip() or current_patient_name
        new_doctor_name = update_entries[2].get().strip() or current_doctor_name
        new_date = update_entries[3].get().strip() or current_date
        new_time = update_entries[4].get().strip() or current_time

        # Check if new patient name exists in the patients table
        if new_patient_name != current_patient_name:  # Only check if it's a change
            patient_exists = execute_query(
                "SELECT COUNT(*) FROM patients WHERE name = %s",
                (new_patient_name,)
            )[0][0]

            if not patient_exists:
                ctk.CTkLabel(parent, text="New patient name does not exist in the database.", text_color="red").pack()
                return

        # Perform the update
        execute_query(
            "UPDATE appointments SET patient_name=%s, doctor_name=%s, date=%s, time=%s WHERE id=%s",
            (new_patient_name, new_doctor_name, new_date, new_time, appointment_id)
        )

        ctk.CTkLabel(parent, text="Appointment updated successfully!", text_color="green").pack()

    ctk.CTkButton(parent, text="Update Appointment", command=update_appointment).pack(pady=10)

# View for Appointment Detail
def appointment_detail_view(parent):
    ctk.CTkLabel(parent, text="Appointment Detail", font=("Arial", 18)).pack(pady=10)

    # Search bar to find an appointment
    search_entry = ctk.CTkEntry(parent, placeholder_text="Search Patient Name")
    search_entry.pack(pady=5)

    # Frame for displaying appointment details
    detail_frame = ctk.CTkFrame(parent)
    detail_frame.pack(fill="x", padx=10, pady=5)

    # Function to display all appointments
    def display_all_appointments():
        all_appointments = execute_query("SELECT * FROM appointments",)

        # Clear previous details
        for widget in detail_frame.winfo_children():
            widget.destroy()

        if all_appointments:
            for row in all_appointments:
                detail_label = ctk.CTkLabel(detail_frame, text=f"ID: {row[0]}, Patient: {row[1]}, Doctor: {row[2]}, Date: {row[3]}, Time: {row[4]}")
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No appointments found").pack()

    # Function to search for an appointment and display its details
    def search_appointment_detail():
        patient_name = search_entry.get().strip()
        results = execute_query("SELECT * FROM appointments WHERE patient_name = %s", (patient_name,))

        # Clear previous details
        for widget in detail_frame.winfo_children():
            widget.destroy()

        if results:
            for row in results:
                detail_label = ctk.CTkLabel(detail_frame, text=f"ID: {row[0]}, Patient: {row[1]}, Doctor: {row[2]}, Date: {row[3]}, Time: {row[4]}")
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No results found").pack()

    # Button to trigger the search function
    ctk.CTkButton(parent, text="Search Appointment", command=search_appointment_detail).pack(pady=5)

    # Initially display all appointments
    display_all_appointments()

# Add Doctor View
def add_doctor_view(parent):
    ctk.CTkLabel(parent, text="Add Doctor", font=("Arial", 18)).pack(pady=10)

    # Input fields for doctor details
    labels = ["Doctor Name:", "Specialization:", "Phone:", "Email:"]
    entries = []
    for label_text in labels:
        ctk.CTkLabel(parent, text=label_text).pack()
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        entries.append(entry)

    # Button to add the doctor to the database
    def add_doctor():
        doctor_name, specialization, phone, email = [e.get() for e in entries]

        # Insert the doctor into the database
        execute_query(
            "INSERT INTO doctors (name, specialization, phone, email) VALUES (%s, %s, %s, %s)",
            (doctor_name, specialization, phone, email)
        )
        ctk.CTkLabel(parent, text="Doctor added successfully!", text_color="green").pack()

    ctk.CTkButton(parent, text="Add Doctor", command=add_doctor).pack(pady=10)

# Update Doctor View
def update_doctor_view(parent):
    ctk.CTkLabel(parent, text="Update Doctor", font=("Arial", 18)).pack(pady=10)

    # Search bar to find a doctor
    search_entry = ctk.CTkEntry(parent, placeholder_text="Search Doctor Name")
    search_entry.pack(pady=5)

    # Frame for search results
    search_results_frame = ctk.CTkFrame(parent)
    search_results_frame.pack(fill="x", padx=10, pady=5)

    # Fields to update doctor details
    update_labels = ["Doctor ID:", "Doctor Name:", "Specialization:", "Phone:", "Email:"]
    update_entries = []
    for label_text in update_labels:
        ctk.CTkLabel(parent, text=label_text).pack()
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        update_entries.append(entry)

    # Function to search for a doctor and display results
    def search_doctor():
        doctor_name = search_entry.get().strip()
        results = execute_query("SELECT * FROM doctors WHERE name = %s", (doctor_name,))

        # Clear previous results
        for widget in search_results_frame.winfo_children():
            widget.destroy()

        if results:
            for row in results:
                result_label = ctk.CTkLabel(
                    search_results_frame, 
                    text=f"Doctor ID: {row[0]}, Name: {row[1]}, Specialization: {row[2]}, Phone: {row[3]}, Email: {row[4]}"
                )
                result_label.pack()

                # Adding button to fill fields with selected result
                update_button = ctk.CTkButton(search_results_frame, text="Select", command=lambda doctor=row: fill_update_fields(doctor))
                update_button.pack(pady=5)

        else:
            ctk.CTkLabel(search_results_frame, text="No results found").pack()

    # Function to fill the update fields with selected doctor details
    def fill_update_fields(doctor):
        # Populate fields with current doctor details
        for entry, value in zip(update_entries[1:], doctor[1:]):  # Skip doctor ID
            entry.delete(0, ctk.END)
            entry.insert(0, value)

        # Set the doctor ID in the first entry
        update_entries[0].delete(0, ctk.END)
        update_entries[0].insert(0, doctor[0])  # Doctor ID

    ctk.CTkButton(parent, text="Search Doctor", command=search_doctor).pack(pady=5)

    # Button to update the doctor in the database
    def update_doctor():
        doctor_id = update_entries[0].get().strip()  # Get the doctor ID

        # Get new values from the entry fields
        new_doctor_name = update_entries[1].get().strip()
        new_specialization = update_entries[2].get().strip()
        new_phone = update_entries[3].get().strip()
        new_email = update_entries[4].get().strip()

        # Perform the update
        execute_query(
            "UPDATE doctors SET name=%s, specialization=%s, phone=%s, email=%s WHERE id=%s",
            (new_doctor_name, new_specialization, new_phone, new_email, doctor_id)
        )

        ctk.CTkLabel(parent, text="Doctor updated successfully!", text_color="green").pack()

    ctk.CTkButton(parent, text="Update Doctor", command=update_doctor).pack(pady=10)

# Doctor Details View
def doctor_detail_view(parent):
    ctk.CTkLabel(parent, text="Doctor Detail", font=("Arial", 18)).pack(pady=10)

    # Search bar to find a doctor
    search_entry = ctk.CTkEntry(parent, placeholder_text="Search Doctor Name")
    search_entry.pack(pady=5)

    # Frame for displaying doctor details
    detail_frame = ctk.CTkFrame(parent)
    detail_frame.pack(fill="x", padx=10, pady=5)

    # Function to display all doctors
    def display_all_doctors():
        all_doctors = execute_query("SELECT * FROM doctors")

        # Clear previous details
        for widget in detail_frame.winfo_children():
            widget.destroy()

        if all_doctors:
            for row in all_doctors:
                detail_label = ctk.CTkLabel(
                    detail_frame, 
                    text=f"ID: {row[0]}, Name: {row[1]}, Specialization: {row[2]}, Phone: {row[3]}, Email: {row[4]}"
                )
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No doctors found").pack()

    # Function to search for a doctor and display its details
    def search_doctor_detail():
        doctor_name = search_entry.get().strip()
        results = execute_query("SELECT * FROM doctors WHERE name = %s", (doctor_name,))

        # Clear previous details
        for widget in detail_frame.winfo_children():
            widget.destroy()

        if results:
            for row in results:
                detail_label = ctk.CTkLabel(
                    detail_frame, 
                    text=f"ID: {row[0]}, Name: {row[1]}, Specialization: {row[2]}, Phone: {row[3]}, Email: {row[4]}"
                )
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No results found").pack()

    # Button to trigger the search function
    ctk.CTkButton(parent, text="Search Doctor", command=search_doctor_detail).pack(pady=5)

    # Initially display all doctors
    display_all_doctors()

# Add Patient View
def add_patient_view(parent):
    ctk.CTkLabel(parent, text="Add Patient", font=("Arial", 18)).pack(pady=10)
    
    labels = ["Name:", "Date of Birth (YYYY-MM-DD):", "Gender:", "Phone:", "Email:"]
    entries = []
    for label_text in labels:
        ctk.CTkLabel(parent, text=label_text).pack()
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        entries.append(entry)

    def add_patient():
        name, dob, gender, phone, email = [e.get().strip() for e in entries]
        
        if not all([name, dob, gender, phone, email]):
            ctk.CTkLabel(parent, text="Please fill in all fields.", text_color="red").pack()
            return

        # Insert patient into the database
        query = "INSERT INTO patients (name, date_of_birth, gender, phone, email) VALUES (%s, %s, %s, %s, %s)"
        execute_query(query, (name, dob, gender, phone, email))
        ctk.CTkLabel(parent, text="Patient added successfully!", text_color="green").pack()

    ctk.CTkButton(parent, text="Add Patient", command=add_patient).pack(pady=10)

# Update Patient View
def update_patient_view(parent):
    ctk.CTkLabel(parent, text="Update Patient", font=("Arial", 18)).pack(pady=10)

    search_entry = ctk.CTkEntry(parent, placeholder_text="Enter Patient Name to Search")
    search_entry.pack(pady=5)
    
    update_labels = ["Patient ID:", "Name:", "Date of Birth (YYYY-MM-DD):", "Gender:", "Phone:", "Email:"]
    update_entries = []
    for label_text in update_labels:
        ctk.CTkLabel(parent, text=label_text).pack()
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        update_entries.append(entry)
    update_entries[0].configure(state=ctk.DISABLED)  # Disable ID field

    def search_patient():
        name = search_entry.get().strip()
        result = execute_query("SELECT * FROM patients WHERE name = %s", (name,))
        
        if result:
            patient = result[0]
            for entry, value in zip(update_entries, patient):
                entry.configure(state=ctk.NORMAL)
                entry.delete(0, ctk.END)
                entry.insert(0, value)
            update_entries[0].configure(state=ctk.DISABLED)
        else:
            ctk.CTkLabel(parent, text="No patient found.", text_color="red").pack()

    ctk.CTkButton(parent, text="Search Patient", command=search_patient).pack(pady=5)

    def update_patient():
        patient_id = update_entries[0].get().strip()
        name, dob, gender, phone, email = [e.get().strip() for e in update_entries[1:]]

        if not patient_id:
            ctk.CTkLabel(parent, text="No patient selected for update.", text_color="red").pack()
            return

        query = "UPDATE patients SET name=%s, date_of_birth=%s, gender=%s, phone=%s, email=%s WHERE id=%s"
        execute_query(query, (name, dob, gender, phone, email, patient_id))
        ctk.CTkLabel(parent, text="Patient updated successfully!", text_color="green").pack()

    ctk.CTkButton(parent, text="Update Patient", command=update_patient).pack(pady=10)

# Patient Details View
def patient_detail_view(parent):
    ctk.CTkLabel(parent, text="Patient Details", font=("Arial", 18)).pack(pady=10)

    search_entry = ctk.CTkEntry(parent, placeholder_text="Search Patient Name")
    search_entry.pack(pady=5)
    
    detail_frame = ctk.CTkFrame(parent)
    detail_frame.pack(fill="x", padx=10, pady=5)

    def display_all_patients():
        all_patients = execute_query("SELECT * FROM patients")
        for widget in detail_frame.winfo_children():
            widget.destroy()
        if all_patients:
            for patient in all_patients:
                detail_label = ctk.CTkLabel(detail_frame, text=f"ID: {patient[0]}, Name: {patient[1]}, DOB: {patient[2]}, Gender: {patient[3]}, Phone: {patient[4]}, Email: {patient[5]}")
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No patients found.").pack()

    def search_patient_detail():
        name = search_entry.get().strip()
        results = execute_query("SELECT * FROM patients WHERE name LIKE %s", ('%' + name + '%',))
        
        for widget in detail_frame.winfo_children():
            widget.destroy()
        
        if results:
            for patient in results:
                detail_label = ctk.CTkLabel(detail_frame, text=f"ID: {patient[0]}, Name: {patient[1]}, DOB: {patient[2]}, Gender: {patient[3]}, Phone: {patient[4]}, Email: {patient[5]}")
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No results found.", text_color="red").pack()

    ctk.CTkButton(parent, text="Search Patient", command=search_patient_detail).pack(pady=5)
    display_all_patients()



# Generate Bill View
def generate_bill_view(parent):
    ctk.CTkLabel(parent, text="Generate Bill", font=("Arial", 18)).pack(pady=10)
    
    # Input fields for bill details
    labels = ["Patient Name:", "Appointment ID:", "Amount:", "Date (YYYY-MM-DD):"]
    entries = []
    for label_text in labels:
        ctk.CTkLabel(parent, text=label_text).pack()
        entry = ctk.CTkEntry(parent)
        entry.pack(pady=5)
        entries.append(entry)
    
    # Dropdown for Payment Status (replacing the entry)
    ctk.CTkLabel(parent, text="Payment Status:").pack()
    payment_status_dropdown = ctk.CTkComboBox(parent, values=["Paid", "Unpaid"])
    payment_status_dropdown.pack(pady=5)

    # Button to generate the bill
    def generate_bill():
        patient_name, appointment_id, amount, date = [e.get().strip() for e in entries]
        payment_status = payment_status_dropdown.get().strip()

        if not all([patient_name, appointment_id, amount, payment_status, date]):
            ctk.CTkLabel(parent, text="Please fill in all fields.", text_color="red").pack()
            return

        # Insert bill into the database
        query = "INSERT INTO bills (patient_name, appointment_id, amount, payment_status, date) VALUES (%s, %s, %s, %s, %s)"
        execute_query(query, (patient_name, appointment_id, amount, payment_status, date))
        ctk.CTkLabel(parent, text="Bill generated successfully!", text_color="green").pack()

    ctk.CTkButton(parent, text="Generate Bill", command=generate_bill).pack(pady=10)

# View Bill View
def view_bill_view(parent):
    ctk.CTkLabel(parent, text="View Bill", font=("Arial", 18)).pack(pady=10)
    
    search_entry = ctk.CTkEntry(parent, placeholder_text="Enter Patient Name to Search")
    search_entry.pack(pady=5)
    
    detail_frame = ctk.CTkFrame(parent)
    detail_frame.pack(fill="x", padx=10, pady=5)

    # Function to display all bills
    def display_all_bills():
        all_bills = execute_query("SELECT * FROM bills")
        for widget in detail_frame.winfo_children():
            widget.destroy()
        if all_bills:
            for bill in all_bills:
                detail_label = ctk.CTkLabel(detail_frame, text=f"ID: {bill[0]}, Patient: {bill[1]}, Appointment ID: {bill[2]}, Amount: ${bill[3]:.2f}, Status: {bill[4]}, Date: {bill[5]}")
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No bills found.").pack()

    # Function to search bills by patient name
    def search_bill():
        patient_name = search_entry.get().strip()
        results = execute_query("SELECT * FROM bills WHERE patient_name LIKE %s", ('%' + patient_name + '%',))

        for widget in detail_frame.winfo_children():
            widget.destroy()

        if results:
            for bill in results:
                detail_label = ctk.CTkLabel(detail_frame, text=f"ID: {bill[0]}, Patient: {bill[1]}, Appointment ID: {bill[2]}, Amount: ${bill[3]:.2f}, Status: {bill[4]}, Date: {bill[5]}")
                detail_label.pack()
        else:
            ctk.CTkLabel(detail_frame, text="No results found.", text_color="red").pack()

    ctk.CTkButton(parent, text="Search Bill", command=search_bill).pack(pady=5)
    display_all_bills()

# Delete Bill View
def delete_bill_view(parent):
    ctk.CTkLabel(parent, text="Delete Bill", font=("Arial", 18)).pack(pady=10)
    
    # Search field to enter Bill ID for deletion
    delete_entry = ctk.CTkEntry(parent, placeholder_text="Enter Bill ID to Delete")
    delete_entry.pack(pady=5)

    # Function to delete a bill
    def delete_bill():
        bill_id = delete_entry.get().strip()
        
        if not bill_id:
            ctk.CTkLabel(parent, text="Please enter a Bill ID.", text_color="red").pack()
            return

        # Execute delete query
        query = "DELETE FROM bills WHERE id = %s"
        execute_query(query, (bill_id,))
        ctk.CTkLabel(parent, text="Bill deleted successfully!", text_color="green").pack()

    ctk.CTkButton(parent, text="Delete Bill", command=delete_bill).pack(pady=5)



# Main application window
app = ctk.CTk()
app.title("Login System")
app.geometry("400x400")

# Login frame
label_title = ctk.CTkLabel(app, text="Login", font=("Arial", 24))
label_title.pack(pady=20)

label_username = ctk.CTkLabel(app, text="Username:")
label_username.pack()
entry_username = ctk.CTkEntry(app)
entry_username.pack(pady=5)

label_password = ctk.CTkLabel(app, text="Password:")
label_password.pack()
entry_password = ctk.CTkEntry(app, show="*")
entry_password.pack(pady=5)

label_role = ctk.CTkLabel(app, text="Role:")
label_role.pack()
role_var = ctk.StringVar(value="Admin")
role_options = ctk.CTkComboBox(app, variable=role_var, values=["Admin", "Doctor", "Pharmacist"])
role_options.pack(pady=5)

label_message = ctk.CTkLabel(app, text="")
label_message.pack()

button_login = ctk.CTkButton(app, text="Login", command=login)
button_login.pack(pady=10)

button_register = ctk.CTkButton(app, text="Register", command=open_register_window)
button_register.pack(pady=10)

app.mainloop()