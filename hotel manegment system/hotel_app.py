import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os

from room_management import RoomManagement
from guest_management import GuestManagement
from booking_management import BookingManagement
from staff_management import StaffManagement
from reporting import Reporting

class HotelManagementApp:
    def __init__(self, master, db):
        """Initialize the main application"""
        self.master = master
        self.db = db
        
        # Set up modern colors
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2ecc71"  # Green
        self.bg_color = "#f5f5f5"  # Light gray
        self.accent_color = "#e74c3c"  # Red
        self.text_color = "#2c3e50"  # Dark blue/gray
        self.sidebar_color = "#34495e"  # Dark blue/gray
        
        # Create style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Configure styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TButton", background=self.primary_color, foreground="white", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=self.text_color)
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.primary_color)
        
        # Sidebar style
        self.style.configure("Sidebar.TFrame", background=self.sidebar_color)
        self.style.configure("Sidebar.TButton", 
                          font=("Segoe UI", 11),
                          background=self.sidebar_color, 
                          foreground="white",
                          borderwidth=0)
        self.style.map("Sidebar.TButton",
                    background=[('active', self.primary_color), ('pressed', self.primary_color)],
                    foreground=[('active', 'white'), ('pressed', 'white')])
        
        # Create main frame
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and arrange sections
        self._create_header()
        self._create_sidebar()
        
        # Set up initial view
        self.current_frame = None
        self.show_dashboard()
        
    def _create_header(self):
        """Create the header section of the application"""
        header_frame = ttk.Frame(self.main_frame, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)  # Force height
        
        # App title
        title_label = ttk.Label(header_frame, text="Pandey Ji Ka Hotel", 
                              style="Title.TLabel")
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Current date and time
        date_label = ttk.Label(header_frame, text=datetime.now().strftime("%Y-%m-%d %H:%M"), 
                             font=("Segoe UI", 10))
        date_label.pack(side=tk.RIGHT, padx=20)
        
    def _create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        # Create container for content
        self.content_container = ttk.Frame(self.main_frame)
        self.content_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar frame
        sidebar_frame = ttk.Frame(self.content_container, style="Sidebar.TFrame", width=220)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_frame.pack_propagate(False)
        
        # Create content frame
        self.content_frame = ttk.Frame(self.content_container)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add some space at the top of sidebar
        ttk.Frame(sidebar_frame, height=20, style="Sidebar.TFrame").pack()
        
        # Dashboard button
        btn_dashboard = ttk.Button(sidebar_frame, text="🏠  Dashboard", 
                                command=self.show_dashboard, style="Sidebar.TButton", width=25)
        btn_dashboard.pack(pady=5, padx=10, fill=tk.X)
        
        # Room Management button
        btn_rooms = ttk.Button(sidebar_frame, text="🛏️  Room Management", 
                             command=self.show_room_management, style="Sidebar.TButton", width=25)
        btn_rooms.pack(pady=5, padx=10, fill=tk.X)
        
        # Guest Management button
        btn_guests = ttk.Button(sidebar_frame, text="👥  Guest Management", 
                              command=self.show_guest_management, style="Sidebar.TButton", width=25)
        btn_guests.pack(pady=5, padx=10, fill=tk.X)
        
        # Booking Management button
        btn_bookings = ttk.Button(sidebar_frame, text="📅  Booking Management", 
                                command=self.show_booking_management, style="Sidebar.TButton", width=25)
        btn_bookings.pack(pady=5, padx=10, fill=tk.X)
        
        # Staff Management button
        btn_staff = ttk.Button(sidebar_frame, text="👔  Staff Management", 
                             command=self.show_staff_management, style="Sidebar.TButton", width=25)
        btn_staff.pack(pady=5, padx=10, fill=tk.X)
        
        # Reports button
        btn_reports = ttk.Button(sidebar_frame, text="📊  Reports", 
                               command=self.show_reports, style="Sidebar.TButton", width=25)
        btn_reports.pack(pady=5, padx=10, fill=tk.X)
        
        # Add separator
        ttk.Separator(sidebar_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=10)
        
        # Add hotel info at bottom
        hotel_info_frame = ttk.Frame(sidebar_frame, style="Sidebar.TFrame")
        hotel_info_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=10)
        
        ttk.Label(hotel_info_frame, text="Pandey Ji Ka Hotel", 
                foreground="white", background=self.sidebar_color,
                font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        ttk.Label(hotel_info_frame, text="Premium Service", 
                foreground="white", background=self.sidebar_color,
                font=("Segoe UI", 8)).pack(anchor=tk.W)
        
    def _clear_content_frame(self):
        """Clear the content frame for new content"""
        # Destroy previous frame if exists
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_dashboard(self):
        """Show the dashboard view"""
        self._clear_content_frame()
        
        self.current_frame = ttk.Frame(self.content_frame)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dashboard title
        title_frame = ttk.Frame(self.current_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(title_frame, text="Dashboard", style="Title.TLabel").pack(side=tk.LEFT)
        refresh_btn = ttk.Button(title_frame, text="🔄 Refresh", command=self.show_dashboard)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Create two frames for stats and recent bookings
        top_frame = ttk.Frame(self.current_frame)
        top_frame.pack(fill=tk.X, pady=10)
        
        # Room status summary cards
        rooms = self.db.get_rooms()
        available = len([r for r in rooms if r[4] == "Available"])
        occupied = len([r for r in rooms if r[4] == "Occupied"])
        maintenance = len([r for r in rooms if r[4] == "Maintenance"])
        
        # Create stat cards
        self._create_stat_card(top_frame, "Total Rooms", len(rooms), "🏨", "#3498db")
        self._create_stat_card(top_frame, "Available", available, "✅", "#2ecc71")
        self._create_stat_card(top_frame, "Occupied", occupied, "🔒", "#e74c3c")
        self._create_stat_card(top_frame, "Maintenance", maintenance, "🔧", "#f39c12")
        
        # Recent bookings
        bottom_frame = ttk.Frame(self.current_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Bookings title
        ttk.Label(bottom_frame, text="Recent Bookings", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        # Recent bookings table
        bookings_frame = ttk.Frame(bottom_frame)
        bookings_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for bookings
        columns = ("Guest", "Room", "Check In", "Check Out", "Status")
        booking_tree = ttk.Treeview(bookings_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        for col in columns:
            booking_tree.heading(col, text=col)
            booking_tree.column(col, width=100)
        
        booking_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(bookings_frame, orient=tk.VERTICAL, command=booking_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        booking_tree.configure(yscrollcommand=scrollbar.set)
        
        # Get recent bookings
        recent_bookings = self.db.get_bookings()[:10]  # Get up to 10 most recent bookings
        
        # Insert bookings into treeview
        if not recent_bookings:
            booking_tree.insert("", tk.END, values=("No recent bookings", "", "", "", ""))
        else:
            for booking in recent_bookings:
                booking_id, first_name, last_name, room_number, check_in, check_out, amount, status = booking
                guest_name = f"{first_name} {last_name}"
                booking_tree.insert("", tk.END, values=(guest_name, room_number, check_in, check_out, status))
    
    def _create_stat_card(self, parent, title, value, icon, color):
        """Create a dashboard stat card"""
        card = tk.Frame(parent, bg=color, width=150, height=100)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        card.pack_propagate(False)  # Force dimensions
        
        # Icon and title
        tk.Label(card, text=icon, font=("Segoe UI", 24), bg=color, fg="white").pack(anchor=tk.W, padx=15, pady=(15, 0))
        tk.Label(card, text=title, font=("Segoe UI", 10), bg=color, fg="white").pack(anchor=tk.W, padx=15, pady=(0, 5))
        
        # Value
        tk.Label(card, text=str(value), font=("Segoe UI", 24, "bold"), bg=color, fg="white").pack(anchor=tk.W, padx=15, pady=(0, 15))
        
    def show_room_management(self):
        """Show the room management view"""
        self._clear_content_frame()
        self.current_frame = RoomManagement(self.content_frame, self.db)
        
    def show_guest_management(self):
        """Show the guest management view"""
        self._clear_content_frame()
        self.current_frame = GuestManagement(self.content_frame, self.db)
    
    def show_booking_management(self):
        """Show the booking management view"""
        self._clear_content_frame()
        self.current_frame = BookingManagement(self.content_frame, self.db)
    
    def show_staff_management(self):
        """Show the staff management view"""
        self._clear_content_frame()
        self.current_frame = StaffManagement(self.content_frame, self.db)
    
    def show_reports(self):
        """Show the reports view"""
        self._clear_content_frame()
        self.current_frame = Reporting(self.content_frame, self.db) 