import tkinter as tk
from tkinter import ttk, messagebox

class StaffManagement(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self._create_widgets()
        
        # Populate staff list
        self._populate_staff_list()
        
    def _create_widgets(self):
        """Create UI widgets for staff management"""
        # Title
        title_label = ttk.Label(self, text="Staff Management", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Main content split into two frames
        left_frame = ttk.Frame(self)
        left_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=(0, 10))
        
        right_frame = ttk.Frame(self)
        right_frame.grid(row=1, column=1, sticky=tk.NSEW)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # === Left Frame: Staff List ===
        list_label = ttk.Label(left_frame, text="Staff List", font=("Arial", 12, "bold"))
        list_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Staff list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.staff_tree = ttk.Treeview(list_frame, columns=("Name", "Position", "Contact", "Salary"), 
                                     selectmode="browse", show="headings")
        self.staff_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.staff_tree.heading("Name", text="Name")
        self.staff_tree.heading("Position", text="Position")
        self.staff_tree.heading("Contact", text="Contact")
        self.staff_tree.heading("Salary", text="Salary")
        
        self.staff_tree.column("Name", width=150)
        self.staff_tree.column("Position", width=120)
        self.staff_tree.column("Contact", width=120)
        self.staff_tree.column("Salary", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.staff_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.staff_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.staff_tree.bind("<<TreeviewSelect>>", self._on_staff_select)
        
        # Position filter controls
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="Filter by Position:").pack(side=tk.LEFT, padx=5)
        self.position_var = tk.StringVar()
        position_cb = ttk.Combobox(filter_frame, textvariable=self.position_var, width=15)
        positions = ["All", "Manager", "Receptionist", "Housekeeper", "Maintenance", "Chef", "Waiter"]
        position_cb['values'] = positions
        position_cb.current(0)
        position_cb.pack(side=tk.LEFT, padx=5)
        position_cb.bind("<<ComboboxSelected>>", self._apply_filter)
        
        refresh_btn = ttk.Button(filter_frame, text="Refresh", command=self._populate_staff_list)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # === Right Frame: Staff Details & Form ===
        form_label = ttk.Label(right_frame, text="Staff Details", font=("Arial", 12, "bold"))
        form_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Staff form fields
        ttk.Label(right_frame, text="First Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(right_frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Last Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(right_frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Position:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.staff_position_var = tk.StringVar()
        self.position_cb = ttk.Combobox(right_frame, textvariable=self.staff_position_var, width=15)
        self.position_cb['values'] = ["Manager", "Receptionist", "Housekeeper", "Maintenance", "Chef", "Waiter"]
        self.position_cb.grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Contact:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.contact_var = tk.StringVar()
        self.contact_entry = ttk.Entry(right_frame, textvariable=self.contact_var)
        self.contact_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Salary:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.salary_var = tk.StringVar()
        self.salary_entry = ttk.Entry(right_frame, textvariable=self.salary_var)
        self.salary_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Staff", command=self._add_staff)
        self.add_btn.grid(row=0, column=0, padx=5)
        
        self.update_btn = ttk.Button(btn_frame, text="Update", command=self._update_staff, state=tk.DISABLED)
        self.update_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear Form", command=self._clear_form)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete", command=self._delete_staff, state=tk.DISABLED)
        self.delete_btn.grid(row=0, column=3, padx=5)
        
        # Configure right frame columns
        right_frame.columnconfigure(1, weight=1)
        
        # Selected staff data (hidden)
        self.selected_staff_id = None
    
    def _populate_staff_list(self):
        """Fetch staff from database and populate the treeview"""
        # Clear the treeview
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)
        
        # Get all staff
        staff_list = self.db.get_staff()
        
        # Filter by position if needed
        position_filter = self.position_var.get()
        if position_filter and position_filter != "All":
            staff_list = [s for s in staff_list if s[3] == position_filter]
        
        # Insert staff into treeview
        for staff in staff_list:
            staff_id, first_name, last_name, position, contact, salary = staff
            full_name = f"{first_name} {last_name}"
            self.staff_tree.insert("", tk.END, values=(full_name, position, contact, f"${salary:.2f}"), tags=(staff_id,))
        
        # Clear selection
        self._clear_form()
    
    def _apply_filter(self, event=None):
        """Apply position filter"""
        self._populate_staff_list()
    
    def _on_staff_select(self, event=None):
        """Handle staff selection from treeview"""
        selection = self.staff_tree.selection()
        if selection:
            item = selection[0]
            
            # Get staff ID from tags
            staff_id = self.staff_tree.item(item, "tags")[0]
            self.selected_staff_id = staff_id
            
            # Get staff details from database
            staff = self.db.get_staff(staff_id)
            if staff:
                _, first_name, last_name, position, contact, salary = staff
                
                # Update form fields
                self.first_name_var.set(first_name)
                self.last_name_var.set(last_name)
                self.staff_position_var.set(position)
                self.contact_var.set(contact)
                self.salary_var.set(f"{salary:.2f}")
                
                # Enable update and delete buttons
                self.update_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)
    
    def _clear_form(self):
        """Clear form fields and reset selection"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.staff_position_var.set("")
        self.contact_var.set("")
        self.salary_var.set("")
        
        # Clear selection
        if self.staff_tree.selection():
            self.staff_tree.selection_remove(self.staff_tree.selection()[0])
        
        self.selected_staff_id = None
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def _add_staff(self):
        """Add a new staff member to the database"""
        # Validate input
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        position = self.staff_position_var.get().strip()
        contact = self.contact_var.get().strip()
        salary_str = self.salary_var.get().strip()
        
        if not first_name or not last_name or not position or not contact or not salary_str:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            salary = float(salary_str)
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number")
            return
        
        # Add staff to database
        result = self.db.add_staff(first_name, last_name, position, contact, salary)
        
        if result:
            messagebox.showinfo("Success", f"Staff {first_name} {last_name} added successfully")
            self._clear_form()
            self._populate_staff_list()
        else:
            messagebox.showerror("Error", "Failed to add staff member")
    
    def _update_staff(self):
        """Update selected staff in the database"""
        if not self.selected_staff_id:
            return
        
        # Validate input
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        position = self.staff_position_var.get().strip()
        contact = self.contact_var.get().strip()
        salary_str = self.salary_var.get().strip().replace("$", "")
        
        if not first_name or not last_name or not position or not contact or not salary_str:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            salary = float(salary_str)
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number")
            return
        
        # Update staff in database
        result = self.db.update_staff(
            self.selected_staff_id, 
            first_name=first_name, 
            last_name=last_name, 
            position=position, 
            contact=contact, 
            salary=salary
        )
        
        if result:
            messagebox.showinfo("Success", f"Staff {first_name} {last_name} updated successfully")
            self._clear_form()
            self._populate_staff_list()
        else:
            messagebox.showerror("Error", "Failed to update staff member")
    
    def _delete_staff(self):
        """Delete selected staff from the database"""
        if not self.selected_staff_id:
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this staff member?"):
            return
        
        # Delete staff from database
        result = self.db.delete_staff(self.selected_staff_id)
        
        if result:
            messagebox.showinfo("Success", "Staff member deleted successfully")
            self._clear_form()
            self._populate_staff_list()
        else:
            messagebox.showerror("Error", "Failed to delete staff member") 