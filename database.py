import sqlite3
import os

DATA_DIR = os.environ.get('ONRENDER_DISK_PATH', '.')
DB_FILE = os.path.join(DATA_DIR, "DB_FILE.db")


def createtables():
    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE Guests (
        GuestID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT UNIQUE,
        Password TEXT NOT NULL,
        ContactNumber TEXT
    );""")

    cursor.execute("""
    CREATE TABLE RoomTypes (
        RoomTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
        RoomType TEXT NOT NULL,
        Caption Text,
        Description Text,
        RatePerNight REAL NOT NULL,
        MaxOccupancy INTEGER,
        BedType TEXT,
        SizeSqFt INTEGER,
        Amenities TEXT,       
        ImagePaths TEXT       
    );
    """)

    cursor.execute("""CREATE TABLE Rooms (
        RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
        RoomNumber TEXT UNIQUE NOT NULL,
        RoomTypeID INTEGER,
        RoomStatus TEXT DEFAULT 'Available',
        FOREIGN KEY (RoomTypeID) REFERENCES RoomTypes(RoomTypeID) ON DELETE CASCADE
    );""")

    cursor.execute("""CREATE TABLE Bookings (
        BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
        GuestID INTEGER,
        RoomID INTEGER,
        CheckInDate DATE NOT NULL,
        CheckOutDate DATE NOT NULL,
        BookingStatus TEXT DEFAULT 'Confirmed',
        FOREIGN KEY (GuestID) REFERENCES Guests(GuestID) ON DELETE CASCADE,
        FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE SET NULL
    );""")


    cursor.execute("""CREATE TABLE Services (
        ServiceID INTEGER PRIMARY KEY AUTOINCREMENT,
        ServiceType TEXT NOT NULL,
        ServiceDetails TEXT,
        ServiceCost REAL NOT NULL
    );""")


    cursor.execute("""CREATE TABLE Billings (
        BillingID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookingID INTEGER,
        TotalAmount REAL NOT NULL,
        PaymentStatus TEXT CHECK(PaymentStatus IN ('Paid', 'Pending')) DEFAULT 'Pending',
        FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE CASCADE
    );""")

    conn.commit()
    conn.close()

def insertvalues():

    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()
    # Standard Room
    cursor.execute("""
    INSERT INTO RoomTypes 
    (RoomType, Caption, Description, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
    """, (
        "Standard Room",
        "A cozy and practical stay option with essential amenities for a comfortable visit.",
        "The Standard Room offers all the essentials in a well-designed space. Perfect for short stays, featuring a double bed, functional furniture, and a clean, modern bathroom.",
        3500,                        # example price
        2,
        "Double Bed",
        300,
        "TV,Wi-Fi,Tea kettle,Bath essentials",
        "new1.jpg,new2.jpg,newbath.jpg"
    ))

    # Deluxe Room
    cursor.execute("""
    INSERT INTO RoomTypes 
    (RoomType, Caption, Description, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
    """, (
        "Deluxe Room",
        "Stylish and spacious room designed for comfort with modern amenities and a relaxing view.",
        "Our Deluxe Room offers refined comfort and smart design. Featuring a queen-size bed, cozy seating corner, and contemporary interiors — ideal for solo travelers, couples, or business stays.",
        5500,
        2,
        "Queen Bed",
        430,
        "TV,Wi-Fi,Tea/Coffee maker,Work desk,Laundry service",
        "deluxer.jpg,deluxue2.jpg,deluxew.jpeg"
    ))

    # Luxury Suite
    cursor.execute("""
    INSERT INTO RoomTypes 
    (RoomType, Caption, Description, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
    """, (
        "Luxury Suite",
        "Elegantly appointed suite with panoramic mountain views and private balcony.",
        "Experience the peak of comfort in our Luxury Suite — expansive living area, plush king-sized bed, curated minibar, and a spa-like ensuite.",
        8500,
        2,
        "King Bed",
        700,
        "TV,Wi-Fi,Espresso machine,Bathtub,Room service",
        "luxury1.jpg,kinfbed1.jpg,hehe.jpg"
    ))

    rooms_data = [
        ('101', 1), ('102', 1), ('103', 1), # Three Standard Rooms
        ('201', 2), ('202', 2),             # Two Deluxe Rooms
        ('301', 3)                          # One Luxury Suite
    ]
    cursor.executemany("INSERT INTO Rooms (RoomNumber, RoomTypeID) VALUES (?, ?)", rooms_data)

    conn.commit()


def login(email,password):
    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Guests WHERE Email = ? AND Password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    conn = sqlite3.connect("DB_FILE.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Guests WHERE Email = ? AND Password = ?", (email, password))
    userdetails = cursor.fetchone()
    conn.close()

    if user:
        return userdetails,1
    else:
        return userdetails,0
    
def signup(username,email,password,phone):
    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Guests (Name, Email,  Password, ContactNumber )VALUES (?,?,?,?);", (username,email,password,phone))
    conn.commit()
    conn.close()

def book_room(guest_id, room_type_id, check_in, check_out):
    """Handles the complete room booking logic."""
    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()

    # Find available rooms of the requested type
    cursor.execute("""
        SELECT R.RoomID FROM Rooms R
        WHERE R.RoomTypeID = ? AND R.RoomID NOT IN (
            SELECT B.RoomID FROM Bookings B
            WHERE (B.CheckInDate < ? AND B.CheckOutDate > ?)
        )
    """, (room_type_id, check_out, check_in))
    
    available_room = cursor.fetchone()

    if not available_room:
        conn.close()
        return "❌ No rooms of this type available for the given dates.",-1

    room_id_to_book = available_room[0]

    # Insert booking
    cursor.execute("""
        INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate)
        VALUES (?, ?, ?, ?)
    """, (guest_id, room_id_to_book, check_in, check_out))
    booking_id = cursor.lastrowid

    # Calculate total bill
    cursor.execute("SELECT RatePerNight FROM RoomTypes WHERE RoomTypeID = ?", (room_type_id,))
    rate = cursor.fetchone()[0]
    cursor.execute("SELECT julianday(?) - julianday(?)", (check_out, check_in))
    nights = int(cursor.fetchone()[0])
    total_amount = rate * nights

    # Insert billing record
    cursor.execute("""
        INSERT INTO Billings (BookingID, TotalAmount, PaymentStatus)
        VALUES (?, ?, 'Pending')
    """, (booking_id, total_amount))
    billing_id = cursor.lastrowid # Get the ID of the new bill

    conn.commit()
    conn.close()
    return "✅ Booking initiated. Please confirm payment.", billing_id

def get_room_details(room_type_id):
    """Fetches details for a specific room type."""
    conn = sqlite3.connect("DB_FILE.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RoomTypes WHERE RoomTypeID=?", (room_type_id,))
    room = cursor.fetchone()
    conn.close()
    return room

# --- ✨ NEW FUNCTION #1: Gathers data for an existing pending booking ✨ ---
def get_pending_booking_details(billing_id):
    """Fetches all details for a specific pending bill to display on the payment page."""
    conn = sqlite3.connect("DB_FILE.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # This query joins all necessary tables to build a complete summary
    cursor.execute("""
        SELECT
            RT.RoomType, RT.RoomTypeID,
            B.CheckInDate, B.CheckOutDate, B.BookingID,
            BL.TotalAmount
        FROM Billings AS BL
        JOIN Bookings AS B ON BL.BookingID = B.BookingID
        JOIN Rooms AS R ON B.RoomID = R.RoomID
        JOIN RoomTypes AS RT ON R.RoomTypeID = RT.RoomTypeID
        WHERE BL.BillingID = ?
    """, (billing_id,))
    
    details = cursor.fetchone()
    conn.close()
    
    if not details:
        return None

    # Calculate nights to display on the summary page
    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()
    cursor.execute("SELECT julianday(?) - julianday(?)", (details['CheckOutDate'], details['CheckInDate']))
    nights = int(cursor.fetchone()[0])
    conn.close()

    return {
        "room_type": {"RoomType": details["RoomType"], "RoomTypeID": details["RoomTypeID"]},
        "check_in": details["CheckInDate"],
        "check_out": details["CheckOutDate"],
        "nights": nights,
        "total_amount": details["TotalAmount"],
        "booking_id": details["BookingID"], # Pass this for the cancel button
        "billing_id": billing_id # Pass this for the pay button
    }

# --- ✨ NEW FUNCTION #2: Updates a bill's status to 'Paid' ✨ ---
def update_bill_to_paid(billing_id):
    """Updates a bill's status from 'Pending' to 'Paid'."""
    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Billings SET PaymentStatus = 'Paid' WHERE BillingID = ?", (billing_id,))
    conn.commit()
    conn.close()
    return "✅ Payment successful! Your booking is confirmed."

# --- ✨ NEW FUNCTION #3: Deletes a pending booking ✨ ---
def cancel_pending_booking(booking_id):
    """Deletes a booking. The CASCADE rule will also delete the associated bill."""
    conn = sqlite3.connect("DB_FILE.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Bookings WHERE BookingID = ?", (booking_id,))
    conn.commit()
    conn.close()
    return "Your booking has been cancelled."

def get_booking_history_for_guest(guest_id):
    """
    Fetches a detailed list of all bookings for a specific guest,
    joining with Billings and RoomTypes to get all necessary info.
    """
    conn = sqlite3.connect("DB_FILE.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # This SQL query joins multiple tables to get a comprehensive view of each booking.
    cursor.execute("""
        SELECT
            RT.RoomType,
            B.CheckInDate,
            B.CheckOutDate,
            BL.PaymentStatus
        FROM Bookings AS B
        JOIN Billings AS BL ON B.BookingID = BL.BookingID
        JOIN Rooms AS R ON B.RoomID = R.RoomID
        JOIN RoomTypes AS RT ON R.RoomTypeID = RT.RoomTypeID
        WHERE B.GuestID = ?
        ORDER BY B.CheckInDate DESC
    """, (guest_id,))
    
    bookings = cursor.fetchall()
    conn.close()
    return bookings


if __name__ == "__main__":
    createtables()
    insertvalues()

