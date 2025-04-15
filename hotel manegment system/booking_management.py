import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

class BookingManagement(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self._create_widgets()
        
        # Populate booking list
        self._populate_booking_list()
        
    def _create_widgets(self):
        """Create UI widgets for booking management"""
        # Title
        title_label = ttk.Label(self, text="Booking Management", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        # Main content split into two frames
        left_frame = ttk.Frame(self)
        left_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=(0, 10))
        
        right_frame = ttk.Frame(self)
        right_frame.grid(row=1, column=1, sticky=tk.NSEW)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # === Left Frame: Booking List ===
        list_label = ttk.Label(left_frame, text="Current Bookings", font=("Arial", 12, "bold"))
        list_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Booking list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.booking_tree = ttk.Treeview(list_frame, 
                                      columns=("Guest", "Room", "Check In", "Check Out", "Status"), 
                                      selectmode="browse", show="headings")
        self.booking_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.booking_tree.heading("Guest", text="Guest")
        self.booking_tree.heading("Room", text="Room")
        self.booking_tree.heading("Check In", text="Check In")
        self.booking_tree.heading("Check Out", text="Check Out")
        self.booking_tree.heading("Status", text="Status")
        
        self.booking_tree.column("Guest", width=150)
        self.booking_tree.column("Room", width=70)
        self.booking_tree.column("Check In", width=100)
        self.booking_tree.column("Check Out", width=100)
        self.booking_tree.column("Status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.booking_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.booking_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.booking_tree.bind("<<TreeviewSelect>>", self._on_booking_select)
        
        # Filter controls
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="Status Filter:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar()
        status_cb = ttk.Combobox(filter_frame, textvariable=self.filter_var, width=15)
        status_cb['values'] = ("All", "Confirmed", "Checked In", "Checked Out", "Cancelled")
        status_cb.current(0)
        status_cb.pack(side=tk.LEFT, padx=5)
        status_cb.bind("<<ComboboxSelected>>", self._apply_filter)
        
        refresh_btn = ttk.Button(filter_frame, text="Refresh", command=self._populate_booking_list)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # === Right Frame: Booking Details & Actions ===
        # Right frame has two sections: Details and New Booking
        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # First tab: Booking Details
        details_frame = ttk.Frame(notebook)
        notebook.add(details_frame, text="Booking Details")
        
        # Second tab: New Booking
        new_booking_frame = ttk.Frame(notebook)
        notebook.add(new_booking_frame, text="New Booking")
        
        # === Details Frame ===
        # Selected booking details
        info_frame = ttk.LabelFrame(details_frame, text="Booking Information")
        info_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Guest info
        ttk.Label(info_frame, text="Guest:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.guest_label = ttk.Label(info_frame, text="-")
        self.guest_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Room info
        ttk.Label(info_frame, text="Room:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.room_label = ttk.Label(info_frame, text="-")
        self.room_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Check-in date
        ttk.Label(info_frame, text="Check-in:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.check_in_label = ttk.Label(info_frame, text="-")
        self.check_in_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Check-out date
        ttk.Label(info_frame, text="Check-out:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.check_out_label = ttk.Label(info_frame, text="-")
        self.check_out_label.grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Total amount
        ttk.Label(info_frame, text="Total Amount:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.amount_label = ttk.Label(info_frame, text="-")
        self.amount_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Status
        ttk.Label(info_frame, text="Status:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.status_label = ttk.Label(info_frame, text="-")
        self.status_label.grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Booking date
        ttk.Label(info_frame, text="Booking Date:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        self.booking_date_label = ttk.Label(info_frame, text="-")
        self.booking_date_label.grid(row=6, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Configure columns
        info_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        action_frame = ttk.Frame(details_frame)
        action_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.checkin_btn = ttk.Button(action_frame, text="Check In", command=self._check_in, state=tk.DISABLED)
        self.checkin_btn.pack(side=tk.LEFT, padx=5)
        
        self.checkout_btn = ttk.Button(action_frame, text="Check Out", command=self._check_out, state=tk.DISABLED)
        self.checkout_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(action_frame, text="Cancel Booking", command=self._cancel_booking, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Payment entry
        payment_frame = ttk.LabelFrame(details_frame, text="Add Payment")
        payment_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Label(payment_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.payment_amount_var = tk.StringVar()
        self.payment_amount_entry = ttk.Entry(payment_frame, textvariable=self.payment_amount_var, width=15)
        self.payment_amount_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(payment_frame, text="Method:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.payment_method_var = tk.StringVar()
        method_cb = ttk.Combobox(payment_frame, textvariable=self.payment_method_var, width=15)
        method_cb['values'] = ("Cash", "Credit Card", "Debit Card", "Bank Transfer")
        method_cb.current(0)
        method_cb.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        self.add_payment_btn = ttk.Button(payment_frame, text="Add Payment", command=self._add_payment, state=tk.DISABLED)
        self.add_payment_btn.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        
        # === New Booking Frame ===
        form_frame = ttk.Frame(new_booking_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        # Guest selection
        ttk.Label(form_frame, text="Select Guest:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.guest_id_var = tk.StringVar()
        self.guest_cb = ttk.Combobox(form_frame, textvariable=self.guest_id_var, width=30)
        self.guest_cb.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Room selection
        ttk.Label(form_frame, text="Select Room:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.room_id_var = tk.StringVar()
        self.room_cb = ttk.Combobox(form_frame, textvariable=self.room_id_var, width=30)
        self.room_cb.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Check-in date
        ttk.Label(form_frame, text="Check-in Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.check_in_date = DateEntry(form_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.check_in_date.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Check-out date
        ttk.Label(form_frame, text="Check-out Date:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.check_out_date = DateEntry(form_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        # Set default to check-in + 1 day
        tomorrow = datetime.now() + timedelta(days=1)
        self.check_out_date.set_date(tomorrow)
        self.check_out_date.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Total amount
        ttk.Label(form_frame, text="Total Amount:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.total_amount_var = tk.StringVar()
        self.total_amount_entry = ttk.Entry(form_frame, textvariable=self.total_amount_var)
        self.total_amount_entry.grid(row=4, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Calculate button
        calculate_btn = ttk.Button(form_frame, text="Calculate Total", command=self._calculate_total)
        calculate_btn.grid(row=4, column=2, sticky=tk.W, pady=5)
        
        # Create booking button
        create_btn = ttk.Button(form_frame, text="Create Booking", command=self._create_booking)
        create_btn.grid(row=5, column=1, sticky=tk.E, pady=10, padx=5)
        
        # Configure grid
        form_frame.columnconfigure(1, weight=1)
        
        # Populate dropdowns
        self._populate_dropdowns()
        
        # Selected booking data (hidden)
        self.selected_booking_id = None
    
    def _populate_booking_list(self):
        """Fetch bookings from database and populate the treeview"""
        # Clear the treeview
        for item in self.booking_tree.get_children():
            self.booking_tree.delete(item)
        
        # Get filtered bookings
        status_filter = self.filter_var.get()
        if status_filter and status_filter != "All":
            bookings = self.db.get_bookings(status=status_filter)
        else:
            bookings = self.db.get_bookings()
        
        # Insert bookings into treeview
        for booking in bookings:
            booking_id, first_name, last_name, room_number, check_in, check_out, amount, status = booking
            guest_name = f"{first_name} {last_name}"
            self.booking_tree.insert("", tk.END, values=(guest_name, room_number, check_in, check_out, status), tags=(booking_id,))
        
        # Clear selection and details
        self._clear_selection()
    
    def _apply_filter(self, event=None):
        """Apply filter to booking list"""
        self._populate_booking_list()
    
    def _on_booking_select(self, event=None):
        """Handle booking selection from treeview"""
        selection = self.booking_tree.selection()
        if selection:
            item = selection[0]
            
            # Get booking ID from tags
            booking_id = self.booking_tree.item(item, "tags")[0]
            self.selected_booking_id = booking_id
            
            # Get full booking details from database
            booking = self.db.get_booking(booking_id)
            if booking:
                _, guest_id, first_name, last_name, room_id, room_number, check_in, check_out, booking_date, amount, status = booking
                
                # Update detail labels
                self.guest_label.config(text=f"{first_name} {last_name}")
                self.room_label.config(text=room_number)
                self.check_in_label.config(text=check_in)
                self.check_out_label.config(text=check_out)
                self.amount_label.config(text=f"₹{amount:.2f}")
                self.status_label.config(text=status)
                self.booking_date_label.config(text=booking_date)
                
                # Enable/disable action buttons based on status
                if status == "Confirmed":
                    self.checkin_btn.config(state=tk.NORMAL)
                    self.checkout_btn.config(state=tk.DISABLED)
                    self.cancel_btn.config(state=tk.NORMAL)
                elif status == "Checked In":
                    self.checkin_btn.config(state=tk.DISABLED)
                    self.checkout_btn.config(state=tk.NORMAL)
                    self.cancel_btn.config(state=tk.NORMAL)
                else:
                    self.checkin_btn.config(state=tk.DISABLED)
                    self.checkout_btn.config(state=tk.DISABLED)
                    self.cancel_btn.config(state=tk.DISABLED)
                
                # Enable payment button
                self.add_payment_btn.config(state=tk.NORMAL)
    
    def _clear_selection(self):
        """Clear booking selection and details"""
        # Clear tree selection
        if self.booking_tree.selection():
            self.booking_tree.selection_remove(self.booking_tree.selection()[0])
        
        # Clear detail labels
        self.guest_label.config(text="-")
        self.room_label.config(text="-")
        self.check_in_label.config(text="-")
        self.check_out_label.config(text="-")
        self.amount_label.config(text="-")
        self.status_label.config(text="-")
        self.booking_date_label.config(text="-")
        
        # Disable action buttons
        self.checkin_btn.config(state=tk.DISABLED)
        self.checkout_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.DISABLED)
        self.add_payment_btn.config(state=tk.DISABLED)
        
        # Clear payment fields
        self.payment_amount_var.set("")
        self.payment_method_var.set("Cash")
        
        self.selected_booking_id = None
    
    def _populate_dropdowns(self):
        """Populate guest and room dropdown lists"""
        # Populate guest dropdown
        guests = self.db.get_guests()
        guest_list = []
        self.guest_map = {}  # Map display names to IDs
        
        for guest in guests:
            guest_id, first_name, last_name = guest[0:3]
            display_name = f"{first_name} {last_name}"
            guest_list.append(display_name)
            self.guest_map[display_name] = guest_id
        
        self.guest_cb['values'] = guest_list
        
        # Auto-select first guest if available
        if guest_list:
            self.guest_cb.current(0)
        
        # Populate room dropdown (only available rooms)
        rooms = self.db.get_rooms(status="Available")
        room_list = []
        self.room_map = {}  # Map display names to IDs
        
        for room in rooms:
            room_id, room_number, room_type, rate = room[0:4]
            display_name = f"{room_number} - {room_type} (₹{rate:.2f}/night)"
            room_list.append(display_name)
            self.room_map[display_name] = (room_id, rate)
        
        self.room_cb['values'] = room_list
        
        # Auto-select first room if available
        if room_list:
            self.room_cb.current(0)
            
        # If we have both a room and a guest selected, calculate the total automatically
        if guest_list and room_list:
            self._calculate_total()
    
    def _calculate_total(self):
        """Calculate total amount based on selected room and dates"""
        try:
            # Get selected room
            room_display = self.room_id_var.get()
            if not room_display or room_display not in self.room_map:
                messagebox.showerror("Error", "Please select a room")
                return
            
            room_id, rate = self.room_map[room_display]
            
            # Get dates
            check_in = self.check_in_date.get_date()
            check_out = self.check_out_date.get_date()
            
            # Calculate number of nights
            nights = (check_out - check_in).days
            if nights <= 0:
                messagebox.showerror("Error", "Check-out date must be after check-in date")
                return
            
            # Calculate total
            total = nights * rate
            
            # Update total field
            self.total_amount_var.set(f"{total:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate total: {str(e)}")
    
    def _create_booking(self):
        """Create a new booking"""
        try:
            # Get selected guest
            guest_display = self.guest_id_var.get()
            if not guest_display:
                messagebox.showerror("Error", "Please select a guest")
                return
                
            # Check if guest is in map (only if we have a selection)
            if guest_display and guest_display not in self.guest_map:
                # If no guests exist yet, show a helpful message
                if not self.guest_map:
                    messagebox.showerror("Error", "No guests available. Please add a guest first in Guest Management.")
                    return
                messagebox.showerror("Error", "Please select a valid guest from the dropdown")
                return
            
            guest_id = self.guest_map[guest_display]
            
            # Get selected room
            room_display = self.room_id_var.get()
            if not room_display:
                messagebox.showerror("Error", "Please select a room")
                return
                
            # Check if room is in map (only if we have a selection)
            if room_display and room_display not in self.room_map:
                # If no rooms are available
                if not self.room_map:
                    messagebox.showerror("Error", "No rooms available for booking.")
                    return
                messagebox.showerror("Error", "Please select a valid room from the dropdown")
                return
            
            room_id, _ = self.room_map[room_display]
            
            # Get dates
            check_in = self.check_in_date.get_date().strftime("%Y-%m-%d")
            check_out = self.check_out_date.get_date().strftime("%Y-%m-%d")
            
            # Get total amount
            total_str = self.total_amount_var.get().strip()
            if not total_str:
                messagebox.showerror("Error", "Please calculate the total amount")
                return
            
            try:
                total = float(total_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid total amount")
                return
            
            # Create booking
            booking_id = self.db.add_booking(guest_id, room_id, check_in, check_out, total)
            
            if booking_id:
                messagebox.showinfo("Success", "Booking created successfully")
                self._populate_booking_list()
                self._populate_dropdowns()  # Refresh room list
                
                # Clear form
                self.guest_id_var.set("")
                self.room_id_var.set("")
                self.total_amount_var.set("")
            else:
                messagebox.showerror("Error", "Failed to create booking")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create booking: {str(e)}")
    
    def _check_in(self):
        """Check in a guest for selected booking"""
        if not self.selected_booking_id:
            return
        
        result = self.db.update_booking_status(self.selected_booking_id, "Checked In")
        
        if result:
            messagebox.showinfo("Success", "Guest checked in successfully")
            self._populate_booking_list()
        else:
            messagebox.showerror("Error", "Failed to check in guest")
    
    def _check_out(self):
        """Check out a guest for selected booking"""
        if not self.selected_booking_id:
            return
        
        result = self.db.update_booking_status(self.selected_booking_id, "Checked Out")
        
        if result:
            messagebox.showinfo("Success", "Guest checked out successfully")
            self._populate_booking_list()
            self._populate_dropdowns()  # Refresh room list
        else:
            messagebox.showerror("Error", "Failed to check out guest")
    
    def _cancel_booking(self):
        """Cancel selected booking"""
        if not self.selected_booking_id:
            return
        
        # Confirm cancellation
        if not messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
            return
        
        result = self.db.update_booking_status(self.selected_booking_id, "Cancelled")
        
        if result:
            messagebox.showinfo("Success", "Booking cancelled successfully")
            self._populate_booking_list()
            self._populate_dropdowns()  # Refresh room list
        else:
            messagebox.showerror("Error", "Failed to cancel booking")
    
    def _add_payment(self):
        """Add payment for selected booking"""
        if not self.selected_booking_id:
            return
        
        # Validate payment amount
        amount_str = self.payment_amount_var.get().strip()
        method = self.payment_method_var.get()
        
        if not amount_str:
            messagebox.showerror("Error", "Please enter payment amount")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Error", "Invalid payment amount")
            return
        
        # Add payment
        result = self.db.add_payment(self.selected_booking_id, amount, method)
        
        if result:
            messagebox.showinfo("Success", f"Payment of ₹{amount:.2f} added successfully")
            self.payment_amount_var.set("")  # Clear payment field
        else:
            messagebox.showerror("Error", "Failed to add payment") 