import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from tabulate import tabulate

class Reporting(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.pack(fill=tk.BOTH, expand=True)
        
        # Create UI elements
        self._create_widgets()
        
        # Initialize with default data
        self._generate_occupancy_report()
        
    def _create_widgets(self):
        """Create UI widgets for reporting"""
        # Title
        title_label = ttk.Label(self, text="Reports", font=("Arial", 14, "bold"))
        title_label.pack(pady=10, anchor=tk.W)
        
        # Create notebook with tabs for different reports
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Occupancy Report
        self.occupancy_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.occupancy_frame, text="Occupancy Report")
        
        # Tab 2: Revenue Report
        self.revenue_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.revenue_frame, text="Revenue Report")
        
        # Setup occupancy report frame
        self._setup_occupancy_report()
        
        # Setup revenue report frame
        self._setup_revenue_report()
    
    def _setup_occupancy_report(self):
        """Setup widgets for occupancy report"""
        # Control frame
        control_frame = ttk.Frame(self.occupancy_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        refresh_btn = ttk.Button(control_frame, text="Refresh Report", command=self._generate_occupancy_report)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Report display frame
        report_frame = ttk.LabelFrame(self.occupancy_frame, text="Room Occupancy Report")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for occupancy data
        self.occupancy_tree = ttk.Treeview(report_frame, 
                                         columns=("Room Type", "Total Rooms", "Available", "Occupied", "Maintenance"),
                                         show="headings")
        self.occupancy_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.occupancy_tree.heading("Room Type", text="Room Type")
        self.occupancy_tree.heading("Total Rooms", text="Total Rooms")
        self.occupancy_tree.heading("Available", text="Available")
        self.occupancy_tree.heading("Occupied", text="Occupied")
        self.occupancy_tree.heading("Maintenance", text="Maintenance")
        
        self.occupancy_tree.column("Room Type", width=150)
        self.occupancy_tree.column("Total Rooms", width=100, anchor=tk.CENTER)
        self.occupancy_tree.column("Available", width=100, anchor=tk.CENTER)
        self.occupancy_tree.column("Occupied", width=100, anchor=tk.CENTER)
        self.occupancy_tree.column("Maintenance", width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.occupancy_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.occupancy_tree.configure(yscrollcommand=scrollbar.set)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(self.occupancy_frame, text="Summary")
        summary_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Summary labels
        ttk.Label(summary_frame, text="Total Rooms:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.total_rooms_label = ttk.Label(summary_frame, text="-")
        self.total_rooms_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(summary_frame, text="Occupancy Rate:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.occupancy_rate_label = ttk.Label(summary_frame, text="-")
        self.occupancy_rate_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Export button
        export_btn = ttk.Button(summary_frame, text="Export Report", command=self._export_occupancy_report)
        export_btn.grid(row=0, column=4, padx=5, pady=2)
    
    def _setup_revenue_report(self):
        """Setup widgets for revenue report"""
        # Control frame
        control_frame = ttk.Frame(self.revenue_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Date range selection
        ttk.Label(control_frame, text="Start Date:").pack(side=tk.LEFT, padx=5)
        start_date = datetime.now() - timedelta(days=30)  # Default to last 30 days
        self.start_date = DateEntry(control_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date.set_date(start_date)
        self.start_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="End Date:").pack(side=tk.LEFT, padx=5)
        self.end_date = DateEntry(control_frame, width=12, background='darkblue',
                                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date.pack(side=tk.LEFT, padx=5)
        
        generate_btn = ttk.Button(control_frame, text="Generate Report", command=self._generate_revenue_report)
        generate_btn.pack(side=tk.LEFT, padx=10)
        
        # Report display frame
        report_frame = ttk.LabelFrame(self.revenue_frame, text="Revenue Report")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for revenue data
        self.revenue_tree = ttk.Treeview(report_frame, 
                                       columns=("Month", "Payment Method", "Total Revenue", "Payment Count"),
                                       show="headings")
        self.revenue_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure columns
        self.revenue_tree.heading("Month", text="Month")
        self.revenue_tree.heading("Payment Method", text="Payment Method")
        self.revenue_tree.heading("Total Revenue", text="Total Revenue")
        self.revenue_tree.heading("Payment Count", text="Number of Payments")
        
        self.revenue_tree.column("Month", width=100)
        self.revenue_tree.column("Payment Method", width=150)
        self.revenue_tree.column("Total Revenue", width=150, anchor=tk.E)
        self.revenue_tree.column("Payment Count", width=150, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.revenue_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.revenue_tree.configure(yscrollcommand=scrollbar.set)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(self.revenue_frame, text="Summary")
        summary_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Summary labels
        ttk.Label(summary_frame, text="Total Revenue:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.total_revenue_label = ttk.Label(summary_frame, text="-")
        self.total_revenue_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(summary_frame, text="Total Payments:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.total_payments_label = ttk.Label(summary_frame, text="-")
        self.total_payments_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Export button
        export_btn = ttk.Button(summary_frame, text="Export Report", command=self._export_revenue_report)
        export_btn.grid(row=0, column=4, padx=5, pady=2)
    
    def _generate_occupancy_report(self):
        """Generate and display occupancy report"""
        # Clear the treeview
        for item in self.occupancy_tree.get_children():
            self.occupancy_tree.delete(item)
        
        # Get occupancy data from database
        occupancy_data = self.db.get_occupancy_report()
        
        # Insert data into treeview
        total_rooms = 0
        total_occupied = 0
        
        for data in occupancy_data:
            room_type, count, available, occupied, maintenance = data
            self.occupancy_tree.insert("", tk.END, values=(room_type, count, available, occupied, maintenance))
            
            total_rooms += count
            total_occupied += occupied
        
        # Update summary
        self.total_rooms_label.config(text=str(total_rooms))
        
        # Calculate occupancy rate
        if total_rooms > 0:
            occupancy_rate = (total_occupied / total_rooms) * 100
            self.occupancy_rate_label.config(text=f"{occupancy_rate:.2f}%")
        else:
            self.occupancy_rate_label.config(text="0.00%")
    
    def _generate_revenue_report(self):
        """Generate and display revenue report"""
        # Clear the treeview
        for item in self.revenue_tree.get_children():
            self.revenue_tree.delete(item)
        
        # Get start and end dates
        start_date = self.start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date.get_date().strftime("%Y-%m-%d")
        
        # Validate date range
        if self.start_date.get_date() > self.end_date.get_date():
            messagebox.showerror("Error", "Start date must be before end date")
            return
        
        # Get revenue data from database
        revenue_data = self.db.get_revenue_report(start_date, end_date)
        
        # Insert data into treeview
        total_revenue = 0
        total_payments = 0
        
        # Check if there's data
        if not revenue_data:
            messagebox.showinfo("No Data", "No payment data found for the selected date range")
            self.total_revenue_label.config(text="₹0.00")
            self.total_payments_label.config(text="0")
            return
        
        for data in revenue_data:
            rev, count, method, month = data
            
            # Format month for display
            try:
                display_month = datetime.strptime(month, "%Y-%m").strftime("%b %Y")
            except:
                display_month = month
            
            self.revenue_tree.insert("", tk.END, values=(display_month, method, f"₹{rev:.2f}", count))
            
            total_revenue += rev
            total_payments += count
        
        # Update summary
        self.total_revenue_label.config(text=f"₹{total_revenue:.2f}")
        self.total_payments_label.config(text=str(total_payments))
    
    def _export_occupancy_report(self):
        """Export occupancy report to a text file"""
        try:
            # Get data from treeview
            data = []
            headers = ["Room Type", "Total Rooms", "Available", "Occupied", "Maintenance"]
            
            for item in self.occupancy_tree.get_children():
                values = self.occupancy_tree.item(item, "values")
                data.append(values)
            
            # Generate report text
            report_text = f"Hotel Occupancy Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            report_text += tabulate(data, headers=headers, tablefmt="grid")
            
            # Add summary
            report_text += f"\n\nTotal Rooms: {self.total_rooms_label.cget('text')}"
            report_text += f"\nOccupancy Rate: {self.occupancy_rate_label.cget('text')}"
            
            # Write to file
            filename = f"occupancy_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, 'w') as f:
                f.write(report_text)
            
            messagebox.showinfo("Export Successful", f"Report exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export report: {str(e)}")
    
    def _export_revenue_report(self):
        """Export revenue report to a text file"""
        try:
            # Check if report has been generated
            if not self.revenue_tree.get_children():
                messagebox.showinfo("No Data", "Please generate a report first")
                return
            
            # Get data from treeview
            data = []
            headers = ["Month", "Payment Method", "Total Revenue", "Payment Count"]
            
            for item in self.revenue_tree.get_children():
                values = self.revenue_tree.item(item, "values")
                data.append(values)
            
            # Get date range
            start_date = self.start_date.get_date().strftime("%Y-%m-%d")
            end_date = self.end_date.get_date().strftime("%Y-%m-%d")
            
            # Generate report text
            report_text = f"Hotel Revenue Report ({start_date} to {end_date})\n"
            report_text += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            report_text += tabulate(data, headers=headers, tablefmt="grid")
            
            # Add summary
            report_text += f"\n\nTotal Revenue: {self.total_revenue_label.cget('text')}"
            report_text += f"\nTotal Payments: {self.total_payments_label.cget('text')}"
            
            # Write to file
            filename = f"revenue_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, 'w') as f:
                f.write(report_text)
            
            messagebox.showinfo("Export Successful", f"Report exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export report: {str(e)}") 