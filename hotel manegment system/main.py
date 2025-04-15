import tkinter as tk
from tkinter import ttk, messagebox
import os
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from datetime import datetime
from tabulate import tabulate

from database import Database
from hotel_app import HotelManagementApp

def main():
    """Main function to initialize and run the hotel management application"""
    # Create database instance
    db = Database()
    
    # Add some initial data if database is empty
    add_initial_data(db)
    
    # Create the main application window
    root = ThemedTk(theme="equilux")  # Use a dark modern theme
    root.title("Pandey Ji Ka Hotel - Management System")
    root.geometry("1280x720")
    root.minsize(1000, 600)
    
    # Configure custom styles
    style = ttk.Style()
    
    # Define colors
    primary_color = "#3498db"  # Blue
    secondary_color = "#2ecc71"  # Green
    bg_color = "#f5f5f5"  # Light gray
    accent_color = "#e74c3c"  # Red
    text_color = "#2c3e50"  # Dark blue/gray
    
    # Button styles
    style.configure("Accent.TButton", background=primary_color, foreground="white")
    style.map("Accent.TButton",
              background=[('active', '#2980b9'), ('pressed', '#2980b9')],
              foreground=[('active', 'white'), ('pressed', 'white')])
    
    style.configure("Success.TButton", background=secondary_color, foreground="white")
    style.map("Success.TButton",
              background=[('active', '#27ae60'), ('pressed', '#27ae60')],
              foreground=[('active', 'white'), ('pressed', 'white')])
    
    style.configure("Danger.TButton", background=accent_color, foreground="white")
    style.map("Danger.TButton",
              background=[('active', '#c0392b'), ('pressed', '#c0392b')],
              foreground=[('active', 'white'), ('pressed', 'white')])
    
    # Treeview styles
    style.configure("Custom.Treeview", 
                  background=bg_color, 
                  foreground=text_color, 
                  rowheight=30,
                  fieldbackground=bg_color)
    style.map("Custom.Treeview",
            background=[('selected', primary_color)],
            foreground=[('selected', 'white')])
    
    # Set window icon if available
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "hotel_icon.png")
        if os.path.exists(icon_path):
            icon = ImageTk.PhotoImage(Image.open(icon_path))
            root.iconphoto(True, icon)
    except:
        pass  # If icon loading fails, just continue
    
    # Initialize the app
    app = HotelManagementApp(root, db)
    
    # Center window on screen
    center_window(root)
    
    # Start the main loop
    root.mainloop()
    
    # Close database connection when application exits
    db.close()

def center_window(window):
    """Center window on the screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def add_initial_data(db):
    """Add some initial data to database if it's empty"""
    # Check if rooms table is empty
    if not db.get_rooms():
        # Add some room types
        room_types = [
            ("101", "Single", 100.0),
            ("102", "Single", 100.0),
            ("201", "Double", 150.0),
            ("202", "Double", 150.0),
            ("301", "Suite", 250.0),
            ("302", "Suite", 250.0),
            ("401", "Deluxe", 350.0),
            ("402", "Deluxe", 350.0)
        ]
        
        for room_num, room_type, rate in room_types:
            db.add_room(room_num, room_type, rate)
            
    # Check if staff table is empty
    if not db.get_staff():
        # Add some staff members
        staff_data = [
            ("John", "Doe", "Manager", "555-1234", 5000.0),
            ("Jane", "Smith", "Receptionist", "555-5678", 2500.0),
            ("Mike", "Johnson", "Maintenance", "555-9012", 2000.0),
            ("Sarah", "Williams", "Housekeeper", "555-3456", 1800.0),
            ("David", "Brown", "Chef", "555-7890", 3500.0)
        ]
        
        for first_name, last_name, position, contact, salary in staff_data:
            db.add_staff(first_name, last_name, position, contact, salary)

if __name__ == "__main__":
    main() 