import tkinter as tk
from tkinter import ttk, messagebox

class GuestManagement(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self._create_widgets()
        
        # Populate guest list
        self._populate_guest_list()
        
    def _create_widgets(self):
        """Create UI widgets for guest management"""
        # Title
        title_label = ttk.Label(self, text="Guest Management", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Main content split into two frames
        left_frame = ttk.Frame(self)
        left_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=(0, 10))
        
        right_frame = ttk.Frame(self)
        right_frame.grid(row=1, column=1, sticky=tk.NSEW)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # === Left Frame: Guest List ===
        list_label = ttk.Label(left_frame, text="Guest List", font=("Arial", 12, "bold"))
        list_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Guest list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.guest_tree = ttk.Treeview(list_frame, columns=("Name", "Phone", "Email"), 
                                     selectmode="browse", show="headings")
        self.guest_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.guest_tree.heading("Name", text="Name")
        self.guest_tree.heading("Phone", text="Phone")
        self.guest_tree.heading("Email", text="Email")
        
        self.guest_tree.column("Name", width=150)
        self.guest_tree.column("Phone", width=120)
        self.guest_tree.column("Email", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.guest_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.guest_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.guest_tree.bind("<<TreeviewSelect>>", self._on_guest_select)
        
        # Search controls
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = ttk.Button(search_frame, text="Search", command=self._apply_search)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = ttk.Button(search_frame, text="Show All", command=self._populate_guest_list)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # === Right Frame: Guest Details & Form ===
        form_label = ttk.Label(right_frame, text="Guest Details", font=("Arial", 12, "bold"))
        form_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # Guest form fields
        ttk.Label(right_frame, text="First Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(right_frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Last Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(right_frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(right_frame, textvariable=self.email_var)
        self.email_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Phone:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(right_frame, textvariable=self.phone_var)
        self.phone_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="Address:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(right_frame, textvariable=self.address_var)
        self.address_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(right_frame, text="ID Proof:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.id_proof_var = tk.StringVar()
        self.id_proof_entry = ttk.Entry(right_frame, textvariable=self.id_proof_var)
        self.id_proof_entry.grid(row=6, column=1, sticky=tk.EW, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Guest", command=self._add_guest)
        self.add_btn.grid(row=0, column=0, padx=5)
        
        self.update_btn = ttk.Button(btn_frame, text="Update", command=self._update_guest, state=tk.DISABLED)
        self.update_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear Form", command=self._clear_form)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Configure right frame columns
        right_frame.columnconfigure(1, weight=1)
        
        # Selected guest data (hidden)
        self.selected_guest_id = None
    
    def _populate_guest_list(self):
        """Fetch guests from database and populate the treeview"""
        # Clear the treeview
        for item in self.guest_tree.get_children():
            self.guest_tree.delete(item)
        
        # Get guests
        guests = self.db.get_guests()
        
        # Insert guests into treeview
        for guest in guests:
            guest_id, first_name, last_name, email, phone = guest[0:5]
            full_name = f"{first_name} {last_name}"
            self.guest_tree.insert("", tk.END, values=(full_name, phone, email), tags=(guest_id,))
        
        # Clear selection
        self._clear_form()
    
    def _apply_search(self):
        """Search for guests"""
        search_term = self.search_var.get().strip()
        if not search_term:
            self._populate_guest_list()
            return
        
        # Clear the treeview
        for item in self.guest_tree.get_children():
            self.guest_tree.delete(item)
        
        # Get filtered guests
        guests = self.db.get_guests(search=search_term)
        
        # Insert guests into treeview
        for guest in guests:
            guest_id, first_name, last_name, email, phone = guest[0:5]
            full_name = f"{first_name} {last_name}"
            self.guest_tree.insert("", tk.END, values=(full_name, phone, email), tags=(guest_id,))
    
    def _on_guest_select(self, event=None):
        """Handle guest selection from treeview"""
        selection = self.guest_tree.selection()
        if selection:
            item = selection[0]
            
            # Get guest ID from tags
            guest_id = self.guest_tree.item(item, "tags")[0]
            self.selected_guest_id = guest_id
            
            # Get full guest details from database
            guest = self.db.get_guest(guest_id)
            if guest:
                _, first_name, last_name, email, phone, address, id_proof = guest
                
                # Update form fields
                self.first_name_var.set(first_name)
                self.last_name_var.set(last_name)
                self.email_var.set(email)
                self.phone_var.set(phone)
                self.address_var.set(address)
                self.id_proof_var.set(id_proof)
                
                # Enable update button
                self.update_btn.config(state=tk.NORMAL)
    
    def _clear_form(self):
        """Clear form fields and reset selection"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.id_proof_var.set("")
        
        # Clear selection
        if self.guest_tree.selection():
            self.guest_tree.selection_remove(self.guest_tree.selection()[0])
        
        self.selected_guest_id = None
        
        # Disable update button
        self.update_btn.config(state=tk.DISABLED)
    
    def _add_guest(self):
        """Add a new guest to the database"""
        # Validate input
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        id_proof = self.id_proof_var.get().strip()
        
        if not first_name or not last_name or not email or not phone:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        # Add guest to database
        result = self.db.add_guest(first_name, last_name, email, phone, address, id_proof)
        
        if result:
            messagebox.showinfo("Success", f"Guest {first_name} {last_name} added successfully")
            self._clear_form()
            self._populate_guest_list()
        else:
            messagebox.showerror("Error", "Failed to add guest")
    
    def _update_guest(self):
        """Update selected guest in the database"""
        if not self.selected_guest_id:
            return
        
        # Validate input
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        id_proof = self.id_proof_var.get().strip()
        
        if not first_name or not last_name or not email or not phone:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        # Update guest in database
        result = self.db.update_guest(
            self.selected_guest_id, 
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            phone=phone, 
            address=address, 
            id_proof=id_proof
        )
        
        if result:
            messagebox.showinfo("Success", f"Guest {first_name} {last_name} updated successfully")
            self._clear_form()
            self._populate_guest_list()
        else:
            messagebox.showerror("Error", "Failed to update guest") 