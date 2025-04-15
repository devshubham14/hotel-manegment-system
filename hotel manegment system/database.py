import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="hotel.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables if they don't exist"""
        # Rooms table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY,
                room_number TEXT UNIQUE,
                room_type TEXT,
                rate REAL,
                status TEXT
            )
        ''')

        # Guests table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS guests (
                guest_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                id_proof TEXT
            )
        ''')

        # Staff table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                staff_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                position TEXT,
                contact TEXT,
                salary REAL
            )
        ''')

        # Bookings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY,
                guest_id INTEGER,
                room_id INTEGER,
                check_in_date TEXT,
                check_out_date TEXT,
                booking_date TEXT,
                total_amount REAL,
                status TEXT,
                FOREIGN KEY (guest_id) REFERENCES guests (guest_id),
                FOREIGN KEY (room_id) REFERENCES rooms (room_id)
            )
        ''')

        # Payments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY,
                booking_id INTEGER,
                amount REAL,
                payment_date TEXT,
                payment_method TEXT,
                FOREIGN KEY (booking_id) REFERENCES bookings (booking_id)
            )
        ''')

        # Commit changes
        self.connection.commit()

    # Room operations
    def add_room(self, room_number, room_type, rate, status="Available"):
        """Add a new room to the database"""
        try:
            self.cursor.execute(
                "INSERT INTO rooms (room_number, room_type, rate, status) VALUES (?, ?, ?, ?)",
                (room_number, room_type, rate, status)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_rooms(self, status=None):
        """Get all rooms or rooms with specific status"""
        if status:
            self.cursor.execute("SELECT * FROM rooms WHERE status = ?", (status,))
        else:
            self.cursor.execute("SELECT * FROM rooms")
        return self.cursor.fetchall()

    def update_room(self, room_id, room_number=None, room_type=None, rate=None, status=None):
        """Update room details"""
        current = self.cursor.execute("SELECT * FROM rooms WHERE room_id = ?", (room_id,)).fetchone()
        if not current:
            return False
        
        room_number = room_number if room_number is not None else current[1]
        room_type = room_type if room_type is not None else current[2]
        rate = rate if rate is not None else current[3]
        status = status if status is not None else current[4]
        
        try:
            self.cursor.execute(
                "UPDATE rooms SET room_number = ?, room_type = ?, rate = ?, status = ? WHERE room_id = ?",
                (room_number, room_type, rate, status, room_id)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_room(self, room_id):
        """Delete a room from the database"""
        try:
            self.cursor.execute("DELETE FROM rooms WHERE room_id = ?", (room_id,))
            self.connection.commit()
            return True
        except:
            return False

    # Guest operations
    def add_guest(self, first_name, last_name, email, phone, address, id_proof):
        """Add a new guest to the database"""
        try:
            self.cursor.execute(
                "INSERT INTO guests (first_name, last_name, email, phone, address, id_proof) VALUES (?, ?, ?, ?, ?, ?)",
                (first_name, last_name, email, phone, address, id_proof)
            )
            self.connection.commit()
            return self.cursor.lastrowid
        except:
            return None

    def get_guests(self, search=None):
        """Get all guests or search for guests"""
        if search:
            self.cursor.execute(
                "SELECT * FROM guests WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR phone LIKE ?",
                (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%")
            )
        else:
            self.cursor.execute("SELECT * FROM guests")
        return self.cursor.fetchall()

    def get_guest(self, guest_id):
        """Get a specific guest by ID"""
        self.cursor.execute("SELECT * FROM guests WHERE guest_id = ?", (guest_id,))
        return self.cursor.fetchone()

    def update_guest(self, guest_id, first_name=None, last_name=None, email=None, phone=None, address=None, id_proof=None):
        """Update guest details"""
        current = self.cursor.execute("SELECT * FROM guests WHERE guest_id = ?", (guest_id,)).fetchone()
        if not current:
            return False
        
        first_name = first_name if first_name is not None else current[1]
        last_name = last_name if last_name is not None else current[2]
        email = email if email is not None else current[3]
        phone = phone if phone is not None else current[4]
        address = address if address is not None else current[5]
        id_proof = id_proof if id_proof is not None else current[6]
        
        try:
            self.cursor.execute(
                "UPDATE guests SET first_name = ?, last_name = ?, email = ?, phone = ?, address = ?, id_proof = ? WHERE guest_id = ?",
                (first_name, last_name, email, phone, address, id_proof, guest_id)
            )
            self.connection.commit()
            return True
        except:
            return False

    # Booking operations
    def add_booking(self, guest_id, room_id, check_in_date, check_out_date, total_amount, status="Confirmed"):
        """Add a new booking"""
        booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(
                "INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date, booking_date, total_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (guest_id, room_id, check_in_date, check_out_date, booking_date, total_amount, status)
            )
            booking_id = self.cursor.lastrowid
            
            # Update room status to booked
            self.cursor.execute("UPDATE rooms SET status = 'Occupied' WHERE room_id = ?", (room_id,))
            
            self.connection.commit()
            return booking_id
        except:
            return None

    def get_bookings(self, status=None):
        """Get all bookings or bookings with specific status"""
        query = """
            SELECT b.booking_id, g.first_name, g.last_name, r.room_number, b.check_in_date, 
            b.check_out_date, b.total_amount, b.status 
            FROM bookings b
            JOIN guests g ON b.guest_id = g.guest_id
            JOIN rooms r ON b.room_id = r.room_id
        """
        
        if status:
            query += " WHERE b.status = ?"
            self.cursor.execute(query, (status,))
        else:
            self.cursor.execute(query)
            
        return self.cursor.fetchall()

    def get_booking(self, booking_id):
        """Get a specific booking details"""
        query = """
            SELECT b.booking_id, g.guest_id, g.first_name, g.last_name, r.room_id, r.room_number, 
            b.check_in_date, b.check_out_date, b.booking_date, b.total_amount, b.status 
            FROM bookings b
            JOIN guests g ON b.guest_id = g.guest_id
            JOIN rooms r ON b.room_id = r.room_id
            WHERE b.booking_id = ?
        """
        self.cursor.execute(query, (booking_id,))
        return self.cursor.fetchone()

    def update_booking_status(self, booking_id, status):
        """Update booking status"""
        try:
            booking = self.get_booking(booking_id)
            if not booking:
                return False
                
            self.cursor.execute("UPDATE bookings SET status = ? WHERE booking_id = ?", (status, booking_id))
            
            # Update room status based on booking status
            room_id = booking[4]  # room_id is at index 4 in get_booking's return value
            if status == "Checked Out":
                self.cursor.execute("UPDATE rooms SET status = 'Available' WHERE room_id = ?", (room_id,))
            elif status == "Cancelled":
                self.cursor.execute("UPDATE rooms SET status = 'Available' WHERE room_id = ?", (room_id,))
            elif status == "Confirmed" or status == "Checked In":
                self.cursor.execute("UPDATE rooms SET status = 'Occupied' WHERE room_id = ?", (room_id,))
                
            self.connection.commit()
            return True
        except:
            return False

    # Staff operations
    def add_staff(self, first_name, last_name, position, contact, salary):
        """Add a new staff member"""
        try:
            self.cursor.execute(
                "INSERT INTO staff (first_name, last_name, position, contact, salary) VALUES (?, ?, ?, ?, ?)",
                (first_name, last_name, position, contact, salary)
            )
            self.connection.commit()
            return self.cursor.lastrowid
        except:
            return None

    def get_staff(self, staff_id=None):
        """Get all staff or a specific staff member"""
        if staff_id:
            self.cursor.execute("SELECT * FROM staff WHERE staff_id = ?", (staff_id,))
            return self.cursor.fetchone()
        else:
            self.cursor.execute("SELECT * FROM staff")
            return self.cursor.fetchall()

    def update_staff(self, staff_id, first_name=None, last_name=None, position=None, contact=None, salary=None):
        """Update staff details"""
        current = self.cursor.execute("SELECT * FROM staff WHERE staff_id = ?", (staff_id,)).fetchone()
        if not current:
            return False
        
        first_name = first_name if first_name is not None else current[1]
        last_name = last_name if last_name is not None else current[2]
        position = position if position is not None else current[3]
        contact = contact if contact is not None else current[4]
        salary = salary if salary is not None else current[5]
        
        try:
            self.cursor.execute(
                "UPDATE staff SET first_name = ?, last_name = ?, position = ?, contact = ?, salary = ? WHERE staff_id = ?",
                (first_name, last_name, position, contact, salary, staff_id)
            )
            self.connection.commit()
            return True
        except:
            return False

    def delete_staff(self, staff_id):
        """Delete a staff member"""
        try:
            self.cursor.execute("DELETE FROM staff WHERE staff_id = ?", (staff_id,))
            self.connection.commit()
            return True
        except:
            return False

    # Payment operations
    def add_payment(self, booking_id, amount, payment_method):
        """Add a payment record"""
        payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(
                "INSERT INTO payments (booking_id, amount, payment_date, payment_method) VALUES (?, ?, ?, ?)",
                (booking_id, amount, payment_date, payment_method)
            )
            self.connection.commit()
            return True
        except:
            return False

    def get_payments(self, booking_id=None):
        """Get all payments or payments for a specific booking"""
        if booking_id:
            self.cursor.execute("SELECT * FROM payments WHERE booking_id = ?", (booking_id,))
        else:
            self.cursor.execute("SELECT * FROM payments")
        return self.cursor.fetchall()

    # Reporting functions
    def get_revenue_report(self, start_date, end_date):
        """Get revenue report between two dates"""
        query = """
            SELECT SUM(amount) as total_revenue, COUNT(*) as payment_count,
            payment_method, strftime('%Y-%m', payment_date) as month
            FROM payments
            WHERE payment_date BETWEEN ? AND ?
            GROUP BY payment_method, month
            ORDER BY month
        """
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()

    def get_occupancy_report(self):
        """Get room occupancy report"""
        query = """
            SELECT room_type, COUNT(*) as total_rooms,
            SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) as available,
            SUM(CASE WHEN status = 'Occupied' THEN 1 ELSE 0 END) as occupied,
            SUM(CASE WHEN status = 'Maintenance' THEN 1 ELSE 0 END) as maintenance
            FROM rooms
            GROUP BY room_type
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close() 