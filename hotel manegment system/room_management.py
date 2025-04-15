import tkinter as tk
from tkinter import ttk, messagebox

class RoomManagement(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # Define colors
        self.primary_color = "#3498db"
        self.success_color = "#2ecc71" 
        self.warning_color = "#f39c12"
        self.danger_color = "#e74c3c"
        self.bg_color = "#f5f5f5"
        self.text_color = "#2c3e50"
        
        # Create UI elements
        self._create_widgets()
        
        # Populate room list
        self._populate_room_list()
        
    def _create_widgets(self):
        """Create UI widgets for room management"""
        # Title
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="Room Management", font=("Segoe UI", 16, "bold"), foreground="#3498db")
        title_label.pack(side=tk.LEFT)
        
        # Main content split into two frames with a divider
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        separator = ttk.Separator(content_frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # === Left Frame: Room List ===
        list_label = ttk.Label(left_frame, text="Room List", font=("Segoe UI", 12, "bold"))
        list_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Filter controls
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter by Status:").pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar()
        status_cb = ttk.Combobox(filter_frame, textvariable=self.status_var, width=15, state="readonly")
        status_cb['values'] = ("All", "Available", "Occupied", "Maintenance")
        status_cb.current(0)
        status_cb.pack(side=tk.LEFT, padx=5)
        status_cb.bind("<<ComboboxSelected>>", self._apply_filter)
        
        # Create search icon for modern look
        refresh_btn = ttk.Button(filter_frame, text="🔄 Refresh", command=self._populate_room_list)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Room list with scrollbar - in a frame with border
        list_container = ttk.Frame(left_frame, relief="solid", borderwidth=1)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Room list with scrollbar
        self.room_tree = ttk.Treeview(list_container, columns=("Room Number", "Type", "Rate", "Status"), 
                                     selectmode="browse", show="headings", style="Custom.Treeview")
        self.room_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.room_tree.heading("Room Number", text="Room Number")
        self.room_tree.heading("Type", text="Type")
        self.room_tree.heading("Rate", text="Rate")
        self.room_tree.heading("Status", text="Status")
        
        self.room_tree.column("Room Number", width=100, anchor=tk.CENTER)
        self.room_tree.column("Type", width=100, anchor=tk.CENTER)
        self.room_tree.column("Rate", width=100, anchor=tk.CENTER)
        self.room_tree.column("Status", width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.room_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.room_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.room_tree.bind("<<TreeviewSelect>>", self._on_room_select)
        
        # Add tag configurations for status colors
        self.room_tree.tag_configure('Available', background="#d5f5e3")  # Light green for available
        self.room_tree.tag_configure('Occupied', background="#f5e8d5")   # Light orange for occupied
        self.room_tree.tag_configure('Maintenance', background="#f5d5d5") # Light red for maintenance
        
        # === Right Frame: Room Details & Form ===
        form_label = ttk.Label(right_frame, text="Room Details", font=("Segoe UI", 12, "bold"))
        form_label.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=tk.W)
        
        # Room form fields in a nice frame
        details_frame = ttk.Frame(right_frame, relief="solid", borderwidth=1, padding=15)
        details_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 15))
        
        # Room form fields
        ttk.Label(details_frame, text="Room Number:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.room_number_var = tk.StringVar()
        self.room_number_entry = ttk.Entry(details_frame, textvariable=self.room_number_var, width=25)
        self.room_number_entry.grid(row=0, column=1, sticky=tk.EW, pady=8, padx=5)
        
        ttk.Label(details_frame, text="Room Type:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.room_type_var = tk.StringVar()
        self.room_type_cb = ttk.Combobox(details_frame, textvariable=self.room_type_var, width=25, state="readonly")
        self.room_type_cb['values'] = ("Single", "Double", "Twin", "Suite", "Deluxe")
        self.room_type_cb.grid(row=1, column=1, sticky=tk.EW, pady=8, padx=5)
        
        ttk.Label(details_frame, text="Rate (per night):").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.rate_var = tk.StringVar()
        self.rate_entry = ttk.Entry(details_frame, textvariable=self.rate_var, width=25)
        self.rate_entry.grid(row=2, column=1, sticky=tk.EW, pady=8, padx=5)
        
        ttk.Label(details_frame, text="Status:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.status_var = tk.StringVar()
        self.status_cb = ttk.Combobox(details_frame, textvariable=self.status_var, width=25, state="readonly")
        self.status_cb['values'] = ("Available", "Occupied", "Maintenance")
        self.status_cb.grid(row=3, column=1, sticky=tk.EW, pady=8, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.add_btn = ttk.Button(btn_frame, text="Add Room", command=self._add_room, style="Accent.TButton")
        self.add_btn.grid(row=0, column=0, padx=5)
        
        self.update_btn = ttk.Button(btn_frame, text="Update", command=self._update_room, state=tk.DISABLED)
        self.update_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear Form", command=self._clear_form)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete", command=self._delete_room, state=tk.DISABLED, style="Danger.TButton")
        self.delete_btn.grid(row=0, column=3, padx=5)
        
        # Status card section
        status_label = ttk.Label(right_frame, text="Room Status Overview", font=("Segoe UI", 12, "bold"))
        status_label.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky=tk.W)
        
        status_frame = ttk.Frame(right_frame)
        status_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW)
        
        # Room status overview
        rooms = self.db.get_rooms()
        available = len([r for r in rooms if r[4] == "Available"])
        occupied = len([r for r in rooms if r[4] == "Occupied"])
        maintenance = len([r for r in rooms if r[4] == "Maintenance"])
        
        # Create modern mini-cards for status
        self._create_status_card(status_frame, "Available", available, "#2ecc71")
        self._create_status_card(status_frame, "Occupied", occupied, "#e74c3c")
        self._create_status_card(status_frame, "Maintenance", maintenance, "#f39c12")
        
        # Configure right frame columns
        right_frame.columnconfigure(1, weight=1)
        
        # Selected room data (hidden)
        self.selected_room_id = None
    
    def _create_status_card(self, parent, status, count, color):
        """Create a small status card"""
        frame = tk.Frame(parent, bg=color, width=120, height=80)
        frame.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        frame.pack_propagate(False)
        
        tk.Label(frame, text=status, bg=color, fg="white", font=("Segoe UI", 10)).pack(pady=(10, 0))
        tk.Label(frame, text=str(count), bg=color, fg="white", font=("Segoe UI", 20, "bold")).pack(pady=(5, 0))
    
    def _populate_room_list(self):
        """Fetch rooms from database and populate the treeview"""
        # Clear the treeview
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)
        
        # Get filtered rooms
        status_filter = self.status_var.get()
        if status_filter and status_filter != "All":
            rooms = self.db.get_rooms(status=status_filter)
        else:
            rooms = self.db.get_rooms()
        
        # Insert rooms into treeview
        for room in rooms:
            room_id, room_number, room_type, rate, status = room
            item_id = self.room_tree.insert("", tk.END, values=(room_number, room_type, f"₹{rate:.2f}", status), tags=(room_id, status))
        
        # Clear selection
        self._clear_form()
    
    def _apply_filter(self, event=None):
        """Apply filter to room list"""
        self._populate_room_list()
    
    def _on_room_select(self, event=None):
        """Handle room selection from treeview"""
        selection = self.room_tree.selection()
        if selection:
            item = selection[0]
            room_number, room_type, rate, status = self.room_tree.item(item, "values")
            
            # Get room ID from tags
            room_id = self.room_tree.item(item, "tags")[0]
            self.selected_room_id = room_id
            
            # Update form fields
            self.room_number_var.set(room_number)
            self.room_type_var.set(room_type)
            self.rate_var.set(rate.replace("$", ""))
            self.status_var.set(status)
            
            # Enable update and delete buttons
            self.update_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
    
    def _clear_form(self):
        """Clear form fields and reset selection"""
        self.room_number_var.set("")
        self.room_type_var.set("")
        self.rate_var.set("")
        self.status_var.set("Available")
        
        # Clear selection
        if self.room_tree.selection():
            self.room_tree.selection_remove(self.room_tree.selection()[0])
        
        self.selected_room_id = None
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def _add_room(self):
        """Add a new room to the database"""
        # Validate input
        room_number = self.room_number_var.get().strip()
        room_type = self.room_type_var.get()
        rate_str = self.rate_var.get().strip()
        status = self.status_var.get()
        
        if not room_number or not room_type or not rate_str:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            rate = float(rate_str)
        except ValueError:
            messagebox.showerror("Error", "Rate must be a number")
            return
        
        # Add room to database
        result = self.db.add_room(room_number, room_type, rate, status)
        
        if result:
            messagebox.showinfo("Success", f"Room {room_number} added successfully")
            self._clear_form()
            self._populate_room_list()
        else:
            messagebox.showerror("Error", f"Failed to add room. Room number may already exist.")
    
    def _update_room(self):
        """Update selected room in the database"""
        if not self.selected_room_id:
            return
        
        # Validate input
        room_number = self.room_number_var.get().strip()
        room_type = self.room_type_var.get()
        rate_str = self.rate_var.get().strip().replace("$", "")
        status = self.status_var.get()
        
        if not room_number or not room_type or not rate_str:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            rate = float(rate_str)
        except ValueError:
            messagebox.showerror("Error", "Rate must be a number")
            return
        
        # Update room in database
        result = self.db.update_room(
            self.selected_room_id, 
            room_number=room_number, 
            room_type=room_type, 
            rate=rate, 
            status=status
        )
        
        if result:
            messagebox.showinfo("Success", f"Room {room_number} updated successfully")
            self._clear_form()
            self._populate_room_list()
        else:
            messagebox.showerror("Error", "Failed to update room")
    
    def _delete_room(self):
        """Delete selected room from the database"""
        if not self.selected_room_id:
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this room?"):
            return
        
        # Delete room from database
        result = self.db.delete_room(self.selected_room_id)
        
        if result:
            messagebox.showinfo("Success", "Room deleted successfully")
            self._clear_form()
            self._populate_room_list()
        else:
            messagebox.showerror("Error", "Failed to delete room") 