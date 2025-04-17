import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import datetime
from database import Database
from login import LoginScreen
class PharmacyApp:
    def __init__(self, ab):
        self.db = None
        self.  akm = ab
        self.  akm.title("Pharmacy Management System")
        self.  akm.geometry("1250x700")
        self.  akm.configure(bg='lightblue')
        self.login_screen()
        
    def login_screen(self):
        LoginScreen(self.  akm, self.on_login_success)

    def on_login_success(self):
    
        self.db = Database()  # Connect to the database when logging in
        self.main_screen()

    def main_screen(self):
        self.main_frame = Frame(self.  akm, bg='gray')
        self.main_frame.pack(fill=BOTH, expand=True)

        title_label = Label(self.main_frame, text="Pharmacy Management System", font=("Arial", 16, "bold"), bg='lightblue', fg='darkblue')
        title_label.pack(pady=20)

        self.tab_control = ttk.Notebook(self.main_frame)

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 12, "bold"), foreground="black")

        # Adding existing and new tabs
        self.doctor_tab = Frame(self.tab_control, bg='#e0e0d1')
        self.patient_tab = Frame(self.tab_control, bg='#e0e0d1')
        self.medicine_tab = Frame(self.tab_control, bg='#e0e0d1')

        self.pharmacy_drugs_tab = Frame(self.tab_control, bg='#e0e0d1')
        self.prescriptions_tab = Frame(self.tab_control, bg='#e0e0d1')
        self.contracts_tab = Frame(self.tab_control, bg='#e0e0d1')
        self.pharmacies_tab = Frame(self.tab_control, bg='#e0e0d1')
        self.drugs_tab = Frame(self.tab_control, bg='#e0e0d1')
        self.pharmaceutical_companies_tab = Frame(self.tab_control, bg='#e0e0d1')

        # Adding tabs to the tab control
        self.tab_control.add(self.doctor_tab, text="Doctor Management")
        self.tab_control.add(self.patient_tab, text="Patient Management")
        self.tab_control.add(self.medicine_tab, text="Medicine Management")
        self.tab_control.add(self.pharmacy_drugs_tab, text="Pharmacy Drugs")
        self.tab_control.add(self.prescriptions_tab, text="Prescriptions")
        self.tab_control.add(self.contracts_tab, text="Contracts")
        self.tab_control.add(self.pharmacies_tab, text="Pharmacies")
        self.tab_control.add(self.drugs_tab, text="Drugs")
        self.tab_control.add(self.pharmaceutical_companies_tab, text="Pharmaceutical Companies")

        self.tab_control.pack(padx=15, fill="both")

        # Setup each tab
        self.setup_doctor_tab()
        self.setup_patient_tab()
        self.setup_medicine_tab()
        self.setup_pharmacy_drugs_tab()
        self.setup_prescriptions_tab()
        self.setup_contracts_tab()
        self.setup_pharmacies_tab()
        self.setup_drugs_tab()
        self.setup_pharmaceutical_companies_tab()

    def setup_doctor_tab(self):
        self.create_form(self.doctor_tab, "Doctor", ["SSN", "Name", "Age", "Speciality", "Years of Experience"],
                         ["ssn", "name", "age", "speciality", "years_experience"], "doctors")

    def setup_patient_tab(self):
        self.create_form(self.patient_tab, "Patient", ["SSN", "Name", "Age", "Address", "Date(YYYY-MM-DD)"],
                         ["ssn", "name", "address","age",  "date"], "patients")

    def setup_medicine_tab(self):
        self.create_form(self.medicine_tab, "Medicine", ["Trade Name", "Formula"],
                         ["trade_name", "formula"], "drugs")

    def setup_pharmacy_drugs_tab(self):
        self.create_form(self.pharmacy_drugs_tab, "Pharmacy Drug", ["Pharmacy Name", "Trade Name", "Price"],
                         ["pharmacy_name", "trade_name", "price"], "pharmacy_drugs")

    def setup_prescriptions_tab(self):
        self.create_form(self.prescriptions_tab, "Prescription", ["Doctor SSN", "Patient SSN", "Trade Name", "Prescription Date(YYYY-MM-DD)", "Quantity"],
                         ["doctor_ssn", "patient_ssn", "trade_name", "prescription_date", "quantity"], "prescriptions")

    def setup_contracts_tab(self):
        self.create_form(self.contracts_tab, "Contract", ["Company Name:", "Pharmacy Name", "Start Date(YYYY-MM-DD)", "End Date(YYYY-MM-DD)", "Contract Text"],
                         ["company_name", "pharmacy_name", "start_date", "end_date", "contract_text"], "contracts")

    def setup_pharmacies_tab(self):
        self.create_form(self.pharmacies_tab, "Pharmacy", ["Name", "Address", "Phone Number"],
                         ["name", "address", "phone_number"], "pharmacies")

    def setup_drugs_tab(self):
        self.create_form(self.drugs_tab, "Drug", ["Trade Name", "Formula", "Company Name"],
                         ["trade_name", "formula", "company_name"], "drugs")

    def setup_pharmaceutical_companies_tab(self):
        self.create_form(self.pharmaceutical_companies_tab, "Pharmaceutical Company", ["Name", "Phone Number"],
                         ["name", "phone_number"], "pharmaceutical_companies")

    def create_form(self, parent, entity_name, labels, db_columns, table_name, patient_tab=False):
        entries = {}
        for i, label in enumerate(labels):
            Label(parent, text=label + ":", font=("Arial", 12, "bold"), fg="darkblue").grid(row=i, column=0, pady=5, padx=10, sticky=W)
            entry = Entry(parent, font=("Arial", 12))
            entry.grid(row=i, column=1, pady=5, padx=10, sticky=W)
            entries[db_columns[i]] = entry
        # Methods for adding, deleting, searching, refreshing, and updating entries
        def add_entity():
            values = tuple(entry.get() for entry in entries.values())
            if not all(values):
                messagebox.showwarning("Input Error", "Please fill all fields")
                return

            # Handling age and address column swapping specifically for the patient management tab
            if patient_tab:
                ssn, name, age, address, date = values
                if not age.isdigit():
                    messagebox.showwarning("Input Error", "Age must be a number")
                    return
                # Correcting age and address input for patients
                values = (ssn, name, int(age), address, date)

            # Insert the data into the database
            columns = ", ".join(entries.keys())
            placeholders = ", ".join(["?" for _ in values])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            try:
                self.db.execute_query(query, values)
                fetch_entities()
                clear_entries()
                messagebox.showinfo(f"Add {entity_name}", f"{entity_name} added successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Duplicate entry or invalid data")

        def fetch_entities():
            query = f"SELECT * FROM {table_name}"
            rows = self.db.fetch_all(query)
            box.delete(*box.get_children())
            for row in rows:
                box.insert("", END, values=row)

        def delete_entity():
            selected = box.selection()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select an item to delete")
                return
            item = box.item(selected)['values']
            confirm = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete {entity_name} with SSN: {item[0]}?")
            if confirm:
                query = f"DELETE FROM {table_name} WHERE {db_columns[0]} = ?"
                self.db.execute_query(query, (item[0],))
                fetch_entities()
                messagebox.showinfo(f"Delete {entity_name}", f"{entity_name} deleted successfully!")

        def search_entity():
            search_id = entries[db_columns[0]].get()
            if not search_id:
                messagebox.showwarning("Input Error", "Please enter a search term")
                return
            query = f"SELECT * FROM {table_name} WHERE {db_columns[0]} = ?"
            rows = self.db.fetch_all(query, (search_id,))
            box.delete(*box.get_children())
            for row in rows:
                box.insert("", END, values=row)

        def update_entity():
            selected = box.selection()
            if not selected:
                messagebox.showwarning("Selection Error", "Please select an item to update")
                return
            item = box.item(selected)['values']
            values = tuple(entry.get() for entry in entries.values())

            if not all(values):
                messagebox.showwarning("Input Error", "Please fill all fields")
                return

            query = f"UPDATE {table_name} SET {', '.join([f'{col} = ?' for col in entries.keys()])} WHERE {db_columns[0]} = ?"
            try:
                self.db.execute_query(query, values + (item[0],))
                fetch_entities()
                messagebox.showinfo(f"Update {entity_name}", f"{entity_name} updated successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Error updating the data")

        def clear_entries():
            for entry in entries.values():
                entry.delete(0, END)

        button_colors = {"Add": "#4CAF50", "Delete": "#f44336", "Search": "#2196F3", "Refresh": "#FF9800", "Clear": "#9E9E9E", "Update": "#FF5722"}
        Button(parent, text=f"Add {entity_name}", command=add_entity, bg=button_colors["Add"], fg='black', font=("Arial", 10, "bold")).grid(row=len(labels), column=0, pady=20)
        Button(parent, text=f"Delete {entity_name}", command=delete_entity, bg=button_colors["Delete"], fg='black', font=("Arial", 10, "bold")).grid(row=len(labels), column=1)
        Button(parent, text=f"Search {entity_name}", command=search_entity, bg=button_colors["Search"], fg='black', font=("Arial", 10, "bold")).grid(row=len(labels)+1, column=0)
        Button(parent, text=f"Refresh {entity_name}", command=fetch_entities, bg=button_colors["Refresh"], fg='black', font=("Arial", 10, "bold")).grid(row=len(labels)+1, column=1)
        Button(parent, text="Clear", command=clear_entries, bg=button_colors["Clear"], fg='black', font=("Arial", 10, "bold")).grid(row=len(labels)+2, column=0, columnspan=2)
        Button(parent, text="Update", command=update_entity, bg=button_colors["Update"], fg='black', font=("Arial", 10, "bold")).grid(row=len(labels)+3, column=0, columnspan=2)

        box = ttk.Treeview(parent, columns=db_columns, show="headings")
        box.grid(row=len(labels)+4, column=0, columnspan=2, pady=10)

        for col in db_columns:
            box.heading(col, text=col.capitalize(), anchor=W)
            box.column(col, width=150, anchor=W)

        fetch_entities()

# Main execution
root = Tk()
app = PharmacyApp(root)
root.mainloop()
